import tensorflow as tf
import tensorflow_probability as tfp # For distributions
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Dense, Input
import numpy as np
import pandas as pd # Added import
from sklearn.preprocessing import MinMaxScaler # Added import
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import time


#change the file path to /home/lserfilippi/tiniMLVM/dreaming_monkey/

os.chdir('/home/lserfilippi/tiniMLVM/dreaming_monkey/')

# --- Device Configuration ---
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# --- Hyperparameters ---
N_STEPS_IN = 24
N_FEATURES = 1
LSTM_UNITS = 32
GAMMA = 1.0  # Discount factor (set to 1 as requested)
LAMBDA_GAE = 1.0
CLIP_EPSILON = 0.2
CRITIC_LOSS_COEF = 1.0
ENTROPY_COEF = 0.0
REGULARIZATION_COEF = 1.5 # lambda_reg
SAMPLING_SIGMA = 0.01# Fixed stddev for sampling policy N(mu, sigma)

# Training loop HPs
EPOCHS = 100
TRAJECTORY_BATCH_SIZE = 16 # Number of initial sequences to generate trajectories from in one go
NUM_STEPS_TO_GENERATE = 24 # Length of each generated trajectory/sequence (1 week)
PPO_UPDATE_EPOCHS = 4 # Number of PPO update epochs per trajectory
PPO_MINIBATCH_SIZE =  int(TRAJECTORY_BATCH_SIZE* NUM_STEPS_TO_GENERATE / 6) # Must be <= TRAJECTORY_BATCH_SIZE * NUM_STEPS_TO_GENERATE
                    # Adjust logic if PPO_MINIBATCH_SIZE spans multiple trajectories

LEARNING_RATE_ACTOR = 1e-4
LEARNING_RATE_CRITIC = 1e-3

SEED = 42
tf.keras.utils.set_random_seed(SEED)
np.random.seed(SEED)

# Eager execution enabled by user (easier debugging, slower execution)
# tf.config.run_functions_eagerly(True)


# --- Data Loading and Preprocessing (Integrated from user code) ---
print("Loading and preprocessing data...")

# Make sure the path is correct
df = pd.read_csv("./sensor_data/spire_5_[44.4901162203284, 11.3398356513878].csv", header=None) # Assume no header if just numbers
# Assuming the first column contains the vehicle counts
df = df[[0]] # Select only the first column
df.columns = ['vehicles'] # Name the column


# Ensure data is float for scaler
df['vehicles'] = df['vehicles'].astype(float)

# Using N_STEPS_IN for previous_values
previous_values = N_STEPS_IN

X_data_list = []
y_data_list = []

for i in range(previous_values, len(df)):
    X_data_list.append(df.iloc[i - N_STEPS_IN:i, 0].values)
    y_data_list.append(df.iloc[i, 0])

X_data, y_data = np.array(X_data_list), np.array(y_data_list)

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
# Scale X features (assuming each time step is a feature - might need adjustment if scaling differently)
# Here, we scale the whole dataset column first, then create sequences
scaled_values = scaler.fit_transform(df['vehicles'].values.reshape(-1, 1))

X_data_scaled_list = []
y_data_scaled_list = []
for i in range(previous_values, len(scaled_values)):
    X_data_scaled_list.append(scaled_values[i - N_STEPS_IN:i, 0])
    y_data_scaled_list.append(scaled_values[i, 0])

X_data = np.array(X_data_scaled_list)
y_data = np.array(y_data_scaled_list)


# Define train/test split index (e.g., last week for test)
test_split_idx = len(X_data) - (24*7) if len(X_data) > 24*7 else int(len(X_data) * 0.8) # Fallback split
if test_split_idx <= 0: # Ensure training data exists
    test_split_idx = int(len(X_data) * 0.8)

X_train = X_data[:test_split_idx]
y_train = y_data[:test_split_idx]
X_test = X_data[test_split_idx:]
y_test = y_data[test_split_idx:]

# Shuffle the training data (optional, but generally good practice for supervised training)
# Not strictly necessary for initializing the RL agent, but good if pre-training was done
# seed = 42
# tf.keras.utils.set_random_seed(seed) # Seed set later
# np.random.seed(seed)
# shuffle_indices = np.random.permutation(len(X_train))
# X_train = X_train[shuffle_indices]
# y_train = y_train[shuffle_indices]


X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

print(f"Data loaded. Train shape: {X_train.shape}, Test shape: {X_test.shape}")
# all_initial_sequences = np.reshape(X_test[0],(1,N_STEPS_IN,N_FEATURES)) # Use training data as pool of initial sequences
all_initial_sequences = X_train # Use training data as pool of initial sequences

print(f"Initial sequences shape: {all_initial_sequences.shape}")
if len(all_initial_sequences) == 0:
    print("Warning: No training data after split. Using random initial sequences.")
    all_initial_sequences = np.random.rand(100, N_STEPS_IN, N_FEATURES).astype(np.float32)

# --- Models ---
print("Loading models...")
try:
    # Ensure correct model names and paths
    actor_model = tf.keras.models.load_model('best_model.keras')
    pretrained_model = tf.keras.models.load_model('best_model.keras')
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading Keras models: {e}")
    print("Creating new models instead.")
    # Fallback: Create new models if loading fails
    actor_model = Sequential([
        LSTM(units=LSTM_UNITS, activation='relu', input_shape=(N_STEPS_IN, N_FEATURES), name='lstm_actor'),
        Dense(units=N_FEATURES, name='dense_actor_mu')
    ], name="Actor")
    pretrained_model = Sequential([
        LSTM(units=LSTM_UNITS, activation='relu', input_shape=(N_STEPS_IN, N_FEATURES), name='lstm_pretrained'),
        Dense(units=N_FEATURES, name='dense_pretrained')
    ])
    # Set random weights if creating new models
    pretrained_model.build(input_shape=(None, N_STEPS_IN, N_FEATURES))
    pretrained_model.set_weights([np.random.randn(*w.shape) for w in pretrained_model.get_weights()])

# Freeze the pre-trained model's weights
for layer in pretrained_model.layers:
    layer.trainable = False

# Critic Model
critic_input = Input(shape=(N_STEPS_IN, N_FEATURES), name='critic_input')
lstm_critic = LSTM(units=LSTM_UNITS, activation='relu', name='lstm_critic')(critic_input)
value_output = Dense(units=1, name='dense_critic_value')(lstm_critic)
critic_model = Model(inputs=critic_input, outputs=value_output, name="Critic")

# --- Optimizers ---
actor_optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE_ACTOR)
critic_optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE_CRITIC)


# --- Probability Distribution Helper ---
@tf.function
def get_policy_distribution(mu, sigma=SAMPLING_SIGMA):
    sigma_tensor = tf.ones_like(mu) * sigma
    # Clip mu to avoid extreme values if data is scaled [0, 1] ? Maybe not needed.
    # mu = tf.clip_by_value(mu, 1e-6, 1.0 - 1e-6) # Example clipping if needed
    return tfp.distributions.Normal(loc=mu, scale=sigma_tensor)

# --- Autoregressive Generation (Sampling) - Unchanged ---
@tf.function
def generate_sequence_sampling(model, initial_sequence, num_steps_to_generate, sampling_stddev=0.0):
    current_sequence = tf.identity(initial_sequence)
    generated_output = []
    for _ in range(num_steps_to_generate):
        mu = model(current_sequence)
        if sampling_stddev > 0.0:
            dist = get_policy_distribution(mu, sampling_stddev)
            sampled_value = dist.sample()
        else:
            sampled_value = mu
        # --- Clip generated values to be within reasonable range (e.g., 0-1 if scaled) ---
        # This is important for vehicle counts which cannot be negative.
        # Adjust clipping range if scaler is different or counts are large.
        sampled_value = tf.clip_by_value(sampled_value, 0.0, 1.5) # Clip to [0, 1.5] (allowing slight overshoot)
        # ---------------------------------------------------------------------------
        generated_output.append(sampled_value)
        next_step_reshaped = tf.reshape(sampled_value, [1, 1, N_FEATURES])
        current_sequence = tf.concat([current_sequence[:, 1:, :], next_step_reshaped], axis=1)

    # generated_output.append(tf.constant([[END_TOKEN]], dtype=tf.float32)) # Append END_TOKEN
    return tf.concat(generated_output, axis=0)


# --- Final Reward Function (Episodic Reward) ---
# ** CRUCIAL: Define reward for the *completed* sequence **
# This dummy example rewards sequences whose average value is high. Replace it!
@tf.function
def calculate_final_reward(generated_sequence_sampled, pretrained_sequence):

    reward = - tf.reduce_mean(generated_sequence_sampled)
    #add regularization term
    mae_loss = tf.reduce_mean(tf.abs(generated_sequence_sampled - pretrained_sequence))

    return reward - mae_loss * REGULARIZATION_COEF, reward, -mae_loss # Return the final reward


# --- GAE Calculation - Corrected for Batch Size > 1 ---
@tf.function
def calculate_gae(rewards, values, dones, gamma=GAMMA, lambda_gae=LAMBDA_GAE):
    advantages = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
    future_advantage = tf.zeros_like(rewards[:, 0], dtype=tf.float32)  # Initialize for the batch
    last_value = values[:, -1]
    rewards = tf.cast(rewards, dtype=tf.float32)
    values = tf.cast(values, dtype=tf.float32)

    for t in tf.range(tf.shape(rewards)[1] - 1, -1, -1):
        next_value_bootstrap = values[:, t + 1] if t < tf.shape(rewards)[1] - 1 else last_value
        mask = 1.0 - tf.cast(dones[:, t], tf.float32)
        delta = rewards[:, t] + gamma * next_value_bootstrap * mask - values[:, t]
        future_advantage = delta + gamma * lambda_gae * future_advantage * mask
        advantages = advantages.write(t, future_advantage)

    advantages = advantages.stack()  # Shape: (time_steps, batch_size)
    advantages = tf.transpose(advantages, perm=[1, 0])  # Transpose to (batch_size, time_steps)
    returns = advantages + values[:, :-1]  # Shape: (batch_size, time_steps)

    # Normalize advantages
    advantages = (advantages - tf.reduce_mean(advantages)) / (tf.math.reduce_std(advantages) + 1e-8)
    return advantages, returns


# --- Data Collection Function (Modified for Sparse Rewards and Batching) ---
def collect_trajectories_sparse(initial_states_batch, actor, critic, num_steps, sigma):
    all_states = []
    all_actions = []
    all_log_probs = []
    all_rewards = []
    all_values = []
    all_dones = []
    all_external_rewards = []
    all_internal_rewards = []
    all_full_sampled_sequences = []
    all_seq_pretrained = []
    final_rewards = []

    for initial_state in initial_states_batch:
        states, actions, log_probs, values, dones = [], [], [], [], []
        rewards = [0.0] * num_steps
        current_sequence = tf.expand_dims(initial_state, 0)
        current_generated = []

        seq_pre = generate_sequence_sampling(pretrained_model, current_sequence, num_steps, 0.0)
        all_seq_pretrained.append(seq_pre)

        for t in range(num_steps):
            state_input = tf.identity(current_sequence)
            value_t = critic(state_input)
            mu_t = actor(state_input)
            dist_t = get_policy_distribution(mu_t, sigma)
            action_t = dist_t.sample()
            action_t = tf.clip_by_value(action_t, 0.0, 1.5)
            log_prob_t = dist_t.log_prob(action_t)

            states.append(tf.squeeze(state_input, axis=0).numpy())
            actions.append(tf.squeeze(action_t, axis=0).numpy())
            log_probs.append(tf.squeeze(log_prob_t, axis=0).numpy())
            values.append(tf.squeeze(value_t).numpy())
            dones.append(False)

            current_generated.append(tf.identity(action_t))
            next_step_reshaped = tf.reshape(action_t, [1, 1, N_FEATURES])
            current_sequence = tf.concat([current_sequence[:, 1:, :], next_step_reshaped], axis=1)

        full_sampled_seq = tf.concat(current_generated, axis=0)
        final_reward, external_reward, internal_reward = calculate_final_reward(full_sampled_seq, seq_pre)
        rewards[-1] = final_reward.numpy()
        final_rewards.append(rewards[-1])

        last_value = critic(current_sequence)
        values.append(tf.squeeze(last_value).numpy())
        dones[-1] = True

        all_states.extend(states)
        all_actions.extend(actions)
        all_log_probs.extend(log_probs)
        all_rewards.extend(rewards)
        all_values.extend(values)
        all_dones.extend(dones)
        all_external_rewards.append(external_reward)
        all_internal_rewards.append(internal_reward)
        all_full_sampled_sequences.append(full_sampled_seq)

    batch_states = tf.convert_to_tensor(np.array(all_states), dtype=tf.float32)
    batch_actions = tf.convert_to_tensor(np.array(all_actions), dtype=tf.float32)
    batch_log_probs = tf.convert_to_tensor(np.array(all_log_probs), dtype=tf.float32)
    batch_rewards = tf.convert_to_tensor(np.array(all_rewards), dtype=tf.float32)
    batch_values = tf.convert_to_tensor(np.array(all_values), dtype=tf.float32)
    batch_dones = tf.convert_to_tensor(np.array(all_dones), dtype=tf.bool)
    try:
        batch_full_sampled_sequences = tf.stack(all_full_sampled_sequences)
        batch_seq_pretrained = tf.stack(all_seq_pretrained)
    except tf.errors.InvalidArgumentError as e:
        print(f"Error stacking full sequences or pretrained sequences: {e}")
        return None

    batch_advantages, batch_returns = calculate_gae(
        tf.reshape(batch_rewards, (TRAJECTORY_BATCH_SIZE, NUM_STEPS_TO_GENERATE)),
        tf.reshape(batch_values, (TRAJECTORY_BATCH_SIZE, NUM_STEPS_TO_GENERATE + 1)),
        tf.reshape(batch_dones, (TRAJECTORY_BATCH_SIZE, NUM_STEPS_TO_GENERATE)),
    )
    average_final_rewards = tf.reduce_mean(final_rewards)
    average_external_rewards = tf.reduce_mean(all_external_rewards)
    average_internal_rewards = tf.reduce_mean(all_internal_rewards)

    return (batch_states, batch_actions, batch_log_probs, batch_advantages, batch_returns,
            batch_full_sampled_sequences, batch_seq_pretrained, average_final_rewards, average_external_rewards, average_internal_rewards)


# --- MAE Sequence Regularization - Unchanged ---
@tf.function
def mae_sequence_regularization(seq_true_deterministic, seq_pred_sampled):
    # Ensure sequences have same length before calculating MAE
    len_true = tf.shape(seq_true_deterministic)[1] # Dim 1 is time steps after stacking
    len_pred = tf.shape(seq_pred_sampled)[1]
    min_len = tf.minimum(len_true, len_pred)
    # Compare only up to the minimum length if they somehow differ (shouldn't if collected correctly)
    return tf.reduce_mean(tf.abs(seq_true_deterministic[:,:min_len,:] - seq_pred_sampled[:,:min_len,:]))

# --- PPO Training Step - Unchanged Structurally ---
@tf.function
def train_step_ppo(states, actions, old_log_probs, advantages, returns,
                    full_sampled_sequences, seq_pretrained,
                    lambda_reg):

    """Performs one PPO update step on a batch of data."""

    with tf.GradientTape() as actor_tape, tf.GradientTape() as critic_tape:
        # Actor Loss
        current_mu = actor_model(states) # Use actor_model here
        current_dist = get_policy_distribution(current_mu, SAMPLING_SIGMA)
        current_log_probs = current_dist.log_prob(actions)
        ratios = tf.exp(current_log_probs - old_log_probs)
        ratios = tf.reshape(ratios, [-1])
        advantages = tf.reshape(advantages, [-1])
        surr1 = ratios * advantages
        surr2 = tf.clip_by_value(ratios, 1.0 - CLIP_EPSILON, 1.0 + CLIP_EPSILON) * advantages
        actor_loss = -tf.reduce_mean(tf.minimum(surr1, surr2))
        entropy = tf.reduce_mean(current_dist.entropy())
        actor_loss -= ENTROPY_COEF * entropy

        # Critic Loss
        current_values = critic_model(states)
        current_values = tf.reshape(current_values, [-1])
        returns = tf.reshape(returns, [-1])
        critic_loss = tf.reduce_mean(tf.square(returns - current_values))

        # Regularization Loss
        reg_loss = mae_sequence_regularization(tf.stop_gradient(seq_pretrained), full_sampled_sequences)

        # Total Loss
        total_actor_loss = actor_loss #+ lambda_reg * reg_loss
        total_critic_loss = critic_loss * CRITIC_LOSS_COEF # Apply critic coef here

    # Apply gradients
    actor_grads = actor_tape.gradient(total_actor_loss, actor_model.trainable_variables) # Use actor_model
    critic_grads = critic_tape.gradient(total_critic_loss, critic_model.trainable_variables)

    # Optional gradient clipping
    # actor_grads, _ = tf.clip_by_global_norm(actor_grads, 0.5)
    # critic_grads, _ = tf.clip_by_global_norm(critic_grads, 0.5)

    actor_optimizer.apply_gradients(zip(actor_grads, actor_model.trainable_variables)) # Use actor_model
    critic_optimizer.apply_gradients(zip(critic_grads, critic_model.trainable_variables))

    return total_actor_loss, total_critic_loss, reg_loss, entropy


# --- Main Training Loop ---
print("Starting Fine-tuning with PPO (Sparse Rewards) + MAE Regularization...")
# Set seed for reproducibility before training loop if needed


visualization_initial_seq = tf.convert_to_tensor(all_initial_sequences[0:1], dtype=tf.float32)
stored_generated_sequences_ppo = []
actor_loss_history = []
critic_loss_history = []
regularization_loss_history = []
entropy_history = []
external_reward_history = []
internal_reward_history = []
reward_history = []



# Ensure PPO_MINIBATCH_SIZE is valid
ppo_batch_size = min(PPO_MINIBATCH_SIZE, TRAJECTORY_BATCH_SIZE * NUM_STEPS_TO_GENERATE)
if ppo_batch_size <= 0:
    ppo_batch_size = 1 # Ensure batch size is at least 1


for epoch in range(EPOCHS):
    print(f"--- Epoch {epoch+1}/{EPOCHS} ---")

    # --- Data Collection Phase ---
    indices = np.random.choice(len(all_initial_sequences), size=TRAJECTORY_BATCH_SIZE, replace=False) # Avoid duplicates if pool large enough
    initial_states_batch_np = all_initial_sequences[indices]
    initial_states_batch = tf.convert_to_tensor(initial_states_batch_np, dtype=tf.float32)


    print(f"  Collecting {TRAJECTORY_BATCH_SIZE} trajectories of length {NUM_STEPS_TO_GENERATE}...")
    trajectory_data = collect_trajectories_sparse(
        initial_states_batch, actor_model, critic_model, NUM_STEPS_TO_GENERATE, SAMPLING_SIGMA
    )

    if trajectory_data is None:
        print("  Skipping epoch due to error during trajectory collection.")
        continue # Skip to next epoch

    (states, actions, old_log_probs, advantages, returns,
     full_sequences_sampled,seq_pretrained_collected,average_final_rewards, average_external_rewards, average_internal_rewards) = trajectory_data

    print(f"  Collected {states.shape[0]} total steps.")

    # Prepare dataset for PPO updates
    # Need to align sequence-level data (full_sequences, initial_states) with step-level data
    # Repeat sequence-level data for each step within its trajectory
    num_traj = TRAJECTORY_BATCH_SIZE
    steps_per_traj = NUM_STEPS_TO_GENERATE

    # Check if dimensions match before repeating
    if full_sequences_sampled.shape[0] != num_traj or seq_pretrained_collected.shape[0] != num_traj:
        print(f"  Warning: Dimension mismatch in full_sequences or pretrained sequences. Skipping PPO updates for epoch {epoch+1}.")
        continue

    full_sequences_repeated = tf.repeat(full_sequences_sampled, repeats=steps_per_traj, axis=0)
    seq_pretrained_repeated = tf.repeat(seq_pretrained_collected, repeats=steps_per_traj, axis=0)


    # Make sure PPO_MINIBATCH_SIZE is valid
    ppo_batch_size = min(PPO_MINIBATCH_SIZE, states.shape[0])
    if ppo_batch_size <= 0:
        print("  Warning: No data steps collected. Skipping PPO updates.")
        continue

    dataset = tf.data.Dataset.from_tensor_slices((
        states, actions, old_log_probs, tf.reshape(advantages, [-1]), tf.reshape(returns, [-1]),
        full_sequences_repeated, # Pass sampled actor sequences
        seq_pretrained_repeated # Pass deterministic pretrained sequences
    ))
    # --- Optimization: Add prefetch ---
    dataset = dataset.shuffle(buffer_size=states.shape[0]).batch(ppo_batch_size).prefetch(tf.data.AUTOTUNE)
    # ----------------------------------


    # --- PPO Update Phase ---
    print(f"  Performing {PPO_UPDATE_EPOCHS} PPO update epochs with batch size {ppo_batch_size}...")
    actor_loss_epoch, critic_loss_epoch, reg_loss_epoch, entropy_epoch = 0, 0, 0, 0
    n_updates = 0
    for ppo_ep in range(PPO_UPDATE_EPOCHS):
        for batch in dataset:
            b_states, b_actions, b_old_logs, b_adv, b_returns, b_full_sampled, b_initials = batch

            # Check batch shape consistency
            if b_states.shape[0] == 0: continue # Skip empty batches

            # Pass the initial states corresponding to this minibatch for reg target gen
            # The initial states are repeated, so just pass b_initials
            actor_loss, critic_loss, reg_loss, entropy = train_step_ppo(
                b_states, b_actions, b_old_logs, b_adv, b_returns,
                b_full_sampled, b_initials, # Pass repeated initial states
                REGULARIZATION_COEF
            )
            if tf.math.is_nan(actor_loss) or tf.math.is_nan(critic_loss):
                print("  Warning: NaN loss detected. Skipping update.")
                continue

            actor_loss_epoch += actor_loss.numpy()
            critic_loss_epoch += critic_loss.numpy()
            reg_loss_epoch += reg_loss.numpy() # Reg loss is already per-batch mean
            entropy_epoch += entropy.numpy()
            n_updates += 1

    if n_updates > 0:
        print(f"  Avg Actor Loss: {actor_loss_epoch/n_updates:.4f}, Critic Loss: {critic_loss_epoch/n_updates:.4f}, Reg Loss: {reg_loss_epoch/n_updates:.4f}, Entropy: {entropy_epoch/n_updates:.4f}")
        actor_loss_history.append(actor_loss_epoch / n_updates)
        critic_loss_history.append(critic_loss_epoch / n_updates)
        regularization_loss_history.append(reg_loss_epoch / n_updates)
        entropy_history.append(entropy_epoch / n_updates)
        external_reward_history.append(average_external_rewards.numpy())
        internal_reward_history.append(average_internal_rewards.numpy())
        reward_history.append(average_final_rewards.numpy())
    else:
        print("  No PPO updates performed in this epoch.")


    # --- Store sequence for GIF ---
    seq_for_viz = generate_sequence_sampling(actor_model, visualization_initial_seq, NUM_STEPS_TO_GENERATE, SAMPLING_SIGMA)
    # tf.config.run_functions_eagerly(False) # Turn back off if needed
    stored_generated_sequences_ppo.append(seq_for_viz.numpy())


print("Fine-tuning complete.")



#save data with time

data_folder = f'./generated_data/{time.strftime("%Y%m%d_%H%M%S")}'
os.makedirs(data_folder, exist_ok=True) # Create directory if it doesn't exist

#save parameters in yaml format
import yaml
params = {
    'N_STEPS_IN': N_STEPS_IN,
    'N_FEATURES': N_FEATURES,
    'LSTM_UNITS': LSTM_UNITS,
    'GAMMA': GAMMA,
    'LAMBDA_GAE': LAMBDA_GAE,
    'CLIP_EPSILON': CLIP_EPSILON,
    'CRITIC_LOSS_COEF': CRITIC_LOSS_COEF,
    'ENTROPY_COEF': ENTROPY_COEF,
    'REGULARIZATION_COEF': REGULARIZATION_COEF,
    'SAMPLING_SIGMA': SAMPLING_SIGMA,
    'EPOCHS': EPOCHS,
    'TRAJECTORY_BATCH_SIZE': TRAJECTORY_BATCH_SIZE,
    'NUM_STEPS_TO_GENERATE': NUM_STEPS_TO_GENERATE,
    'PPO_UPDATE_EPOCHS': PPO_UPDATE_EPOCHS,
    'PPO_MINIBATCH_SIZE': PPO_MINIBATCH_SIZE,
    'LEARNING_RATE_ACTOR': LEARNING_RATE_ACTOR,
    'LEARNING_RATE_CRITIC': LEARNING_RATE_CRITIC,
    'SEED': SEED,
    'DATA_FOLDER': data_folder,
    'DATA_FILE': './sensor_data/spire_5_[44.4901162203284, 11.3398356513878].csv',
    'MODEL_PATH': 'best_model.keras',
}

with open(f"{data_folder}/params.yaml", 'w') as file:
    yaml.dump(params, file)


#save original sequence with pretrained
for i, seq in enumerate(seq_pretrained_collected):
    # Convert to original scale
    seq_original_scale = scaler.inverse_transform(seq)
    # Save each sequence as a CSV file
    np.savetxt(f"{data_folder}/pretrained_sequence_{i}.csv", seq_original_scale, delimiter=',')


# Save the generated sequences
for i, seq in enumerate(stored_generated_sequences_ppo):
    # Convert to original scale
    seq_original_scale = scaler.inverse_transform(seq)
    # Save each sequence as a CSV file
    np.savetxt(f"{data_folder}/generated_sequence_{i}.csv", seq_original_scale, delimiter=',')

#save learning curves
history_df = pd.DataFrame({
    'Epoch': np.arange(1, len(actor_loss_history) + 1),
    'Actor_Loss': actor_loss_history,
    'Critic_Loss': critic_loss_history,
    'Regularization_Loss': regularization_loss_history,
    'Reward': reward_history,
    'External_Reward': external_reward_history,
    'Internal_Reward': internal_reward_history,
    'Entropy': entropy_history
})
history_df.to_csv(f"{data_folder}/training_history.csv", index=False)