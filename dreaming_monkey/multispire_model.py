import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F

# Check if PyG is installed and import GCNConv
try:
    from torch_geometric.nn import GCNConv
    from torch_geometric.utils import dense_to_sparse
except ImportError:
    print("PyTorch Geometric not found. Install with: pip install torch-geometric")
    # Fallback or raise error if needed
    GCNConv = None # Or define a dummy class

import numpy as np
from sklearn.metrics.pairwise import haversine_distances
from sklearn.preprocessing import  MinMaxScaler
import argparse
import math
import time
import os # For saving models
import pandas as pd
import joblib

generated_data_folder = f"./multispire_generated_data/{time.strftime('%Y-%m-%d_%H-%M-%S')}/"
if not os.path.exists(generated_data_folder):
    os.makedirs(generated_data_folder)
    print(f"Created directory: {generated_data_folder}")


# --- 1. Graph Construction ---
def create_graph_data(locations, threshold=None, k=None):
    """
    Creates graph connectivity data (edge_index and edge_weight).

    Args:
        locations (np.ndarray): Array of shape (num_spires, 2) with lat/lon.
        threshold (float, optional): Distance threshold for connecting nodes.
        k (int, optional): Number of nearest neighbors to connect (KNN).
                           Use either threshold or k, not both.

    Returns:
        tuple: (edge_index, edge_weight) suitable for PyG layers.
               edge_index: Tensor shape (2, num_edges)
               edge_weight: Tensor shape (num_edges,)
    """
    num_spires = locations.shape[0]
    dist_mx = haversine_distances(locations, locations)

    if threshold is not None:
        adj_matrix = np.where(dist_mx <= threshold, 1, 0)
        # Optional: Weight edges by inverse distance (closer = higher weight)
        # Use a small epsilon to avoid division by zero for self-loops if included
        # weight_matrix = np.exp(-dist_mx**2 / np.std(dist_mx)**2)
        # adj_matrix = adj_matrix * weight_matrix
    elif k is not None:
        adj_matrix = np.zeros((num_spires, num_spires), dtype=np.float32)
        for i in range(num_spires):
            # Get indices of k nearest neighbors (excluding self)
            neighbor_idxs = np.argsort(dist_mx[i, :])[1:k+1]
            adj_matrix[i, neighbor_idxs] = 1
            # Optional: Make symmetric if desired (A or A.T)
            adj_matrix[neighbor_idxs, i] = 1 # Make symmetric
    else:
        raise ValueError("Must provide either distance 'threshold' or 'k' for KNN.")

    # Ensure no self-loops if not desired, or add them explicitly
    np.fill_diagonal(adj_matrix, 0) # No self-loops for standard GCN here
    # Or add self-loops: np.fill_diagonal(adj_matrix, 1)

    # Convert adjacency matrix to edge_index format for PyG
    adj_matrix_torch = torch.tensor(adj_matrix, dtype=torch.float32)
    edge_index, edge_weight = dense_to_sparse(adj_matrix_torch) # edge_weight will be 1.0 where connection exists

    # If you want distance-based weights instead of binary:
    # Find pairs corresponding to edge_index
    # src, dest = edge_index[0].numpy(), edge_index[1].numpy()
    # distances = dist_mx[src, dest]
    # edge_weight = torch.tensor(np.exp(-distances**2 / np.std(dist_mx[dist_mx > 0])**2), dtype=torch.float32)

    print(f"Graph created with {edge_index.shape[1]} edges.")
    return edge_index, edge_weight

# --- 2. Dataset Preparation ---
class SpireTimeSeriesDataset(Dataset):
    """Dataset for Spatio-Temporal Graph Neural Networks."""
    def __init__(self, data, seq_len, pred_len):
        """
        Args:
            data (np.ndarray): Shape (num_spires, total_timesteps, num_features).
                               Assumes data is already scaled/normalized.
            seq_len (int): Length of the input sequence (history).
            pred_len (int): Length of the prediction sequence (future).
        """
        super().__init__()
        self.data = torch.tensor(data, dtype=torch.float32)
        self.seq_len = seq_len
        self.pred_len = pred_len
        self.num_nodes, self.total_timesteps, self.num_features = data.shape

        # Calculate number of possible samples
        self.num_samples = self.total_timesteps - self.seq_len - self.pred_len + 1

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        """
        Returns one sample sequence pair.

        Args:
            idx (int): Index of the sample.

        Returns:
            tuple: (input_sequence, target_sequence)
                   input_sequence: Tensor shape (num_nodes, seq_len, num_features)
                   target_sequence: Tensor shape (num_nodes, pred_len, num_features)
        """
        start_idx = idx
        end_idx_input = start_idx + self.seq_len
        end_idx_target = end_idx_input + self.pred_len

        input_seq = self.data[:, start_idx:end_idx_input, :]
        target_seq = self.data[:, end_idx_input:end_idx_target, :]

        return input_seq, target_seq

# --- 3. Model Definition (STGNN) ---
class STGNN(nn.Module):
    """
    Simple Spatio-Temporal Graph Neural Network using GCN and GRU.
    Predicts `pred_len` steps ahead for all nodes.
    """
    def __init__(self, num_nodes, num_features, seq_len, pred_len,
                 gcn_hidden_dim, gru_hidden_dim, dropout=0.1):
        super().__init__()
        self.num_nodes = num_nodes
        self.num_features = num_features
        self.seq_len = seq_len
        self.pred_len = pred_len
        self.gcn_hidden_dim = gcn_hidden_dim
        self.gru_hidden_dim = gru_hidden_dim

        if GCNConv is None:
             raise ImportError("GCNConv not available. Install torch-geometric.")

        # Spatial Layer
        self.gcn = GCNConv(num_features, gcn_hidden_dim)

        # Temporal Layer
        # Input to GRU will be the spatially processed features
        self.gru = nn.GRU(gcn_hidden_dim, gru_hidden_dim, batch_first=True) # batch_first = True helps

        self.dropout = nn.Dropout(p=dropout)

        # Output Layer: Predicts pred_len steps for each node's feature
        self.output_fc = nn.Linear(gru_hidden_dim, pred_len * num_features)


    def forward(self, x, edge_index, edge_weight=None):
        """
        Forward pass of the STGNN.

        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, num_nodes, seq_len, num_features).
            edge_index (torch.Tensor): Graph edge index, shape (2, num_edges).
            edge_weight (torch.Tensor, optional): Edge weights, shape (num_edges,).

        Returns:
            torch.Tensor: Prediction tensor of shape (batch_size, num_nodes, pred_len).
                          (Assuming num_features=1 for prediction)
        """
        batch_size, _, _, _ = x.shape
        device = x.device

        # Process sequence step-by-step to apply GCN
        gru_inputs = []
        for t in range(self.seq_len):
            # Get features for all nodes at time step t: shape (batch_size, num_nodes, num_features)
            xt = x[:, :, t, :]

            # Reshape for GCN: (batch_size * num_nodes, num_features)
            xt_reshaped = xt.reshape(-1, self.num_features)

            # Adapt edge_index for batch processing (if not using PyG DataLoader)
            # This replicates the graph structure for each item in the batch
            batch_edge_index = edge_index.repeat(1, batch_size)
            edge_index_offsets = torch.arange(0, batch_size, device=device) * self.num_nodes
            batch_edge_index = batch_edge_index + edge_index_offsets.repeat_interleave(edge_index.shape[1])

            # Adapt edge_weight for batch processing (if provided)
            batch_edge_weight = edge_weight.repeat(batch_size) if edge_weight is not None else None

            # Apply GCN
            gcn_out = self.gcn(xt_reshaped, batch_edge_index, batch_edge_weight)
            gcn_out = F.relu(gcn_out) # Activation after GCN

            # Reshape back: (batch_size, num_nodes, gcn_hidden_dim)
            gcn_out = gcn_out.view(batch_size, self.num_nodes, self.gcn_hidden_dim)
            gru_inputs.append(gcn_out)

        # Stack outputs along the sequence dimension: (batch_size, seq_len, num_nodes, gcn_hidden_dim)
        gru_input_sequence = torch.stack(gru_inputs, dim=1)

        # Flatten nodes dimension for GRU processing
        # GRU expects input: (batch_size * num_nodes, seq_len, input_size)
        gru_input_sequence = gru_input_sequence.permute(0, 2, 1, 3) # -> (batch, node, seq, hidden)
        gru_input_sequence = gru_input_sequence.reshape(batch_size * self.num_nodes, self.seq_len, self.gcn_hidden_dim)

        # Apply GRU
        # Initialize hidden state: (D*num_layers, N, Hout) = (1, batch*nodes, gru_hidden)
        # h0 = torch.zeros(1, batch_size * self.num_nodes, self.gru_hidden_dim).to(device)
        # gru_output shape: (batch*nodes, seq_len, gru_hidden)
        # hidden state shape: (1, batch*nodes, gru_hidden)
        gru_output, hidden = self.gru(gru_input_sequence) # Pass h0=h0 if needed

        # Take the output corresponding to the *last* time step from the GRU sequence output
        # gru_output shape: (batch*nodes, seq_len, gru_hidden) -> select last step
        last_step_output = gru_output[:, -1, :] # Shape: (batch*nodes, gru_hidden)

        # Apply dropout
        last_step_output = self.dropout(last_step_output)

        # Apply Output Layer
        # Input shape: (batch*nodes, gru_hidden)
        # Output shape: (batch*nodes, pred_len * num_features)
        predictions = self.output_fc(last_step_output)

        # Reshape predictions back to (batch_size, num_nodes, pred_len, num_features)
        predictions = predictions.view(batch_size, self.num_nodes, self.pred_len, self.num_features)

        # If predicting only one feature (e.g., car count), squeeze the last dim
        if self.num_features == 1:
           predictions = predictions.squeeze(-1) # -> (batch_size, num_nodes, pred_len)

        return predictions
    
def calculate_distance(lat1, lon1, lat2, lon2):
        # Haversine formula to calculate the distance between two points on the Earth
        R = 6371e3  # Radius of the Earth in meters
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)

        a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return R * c


# --- 4. Training Setup ---
def run_training(args, device):
    """Main training loop."""

    #select spires to train on

    rsu = [44.4901162203284, 11.3398356513878]

    radius = 1000 #m

    folder_path_spires = "./sensor_data/"
    spires_list = []

    #load all spires in the radius
    for file in os.listdir(folder_path_spires):
        if file.endswith(".csv"):
            #get the coordinates from the filename
            coordinates = file.split("_")[2].split("[")[1].split("]")[0].split(",")
            lat = float(coordinates[0])
            lon = float(coordinates[1])
            #calculate the distance
            distance = calculate_distance(rsu[0], rsu[1], lat, lon)
            print(f"Distance from RSU to {file}: {distance} m")
            if distance <= radius:
                spires_list.append(file)

    # --- Dummy Data & Graph ---
    # Replace with your actual data loading
    print("Loading data...")
    num_spires = len(spires_list)
    num_features = 1      # Just car counts

    data_spires = []
    locations_spires = []
    for spire in spires_list:
        df = pd.read_csv(os.path.join(folder_path_spires, spire))
        data_spires.append(df.values)
        coordinates = spire.split("_")[2].split("[")[1].split("]")[0].split(",")

        lat = float(coordinates[0])
        lon = float(coordinates[1])
        locations_spires.append([lat, lon])

    total_timesteps = df.shape[0] # Assuming all spires have the same number of timesteps
    
    #transform the data to a numpy array
    locations = np.array(locations_spires)
    raw_data = np.array(data_spires)

    #save spires list
    np.save(generated_data_folder+"spires_list.npy", np.array(spires_list))
    #save locations

    # --- Preprocessing ---
    #scale the data from 0 to 1
    Scaler = MinMaxScaler(feature_range=(0, 1))
    # Fit scaler on the entire dataset
    scaled_data = Scaler.fit_transform(raw_data.reshape(-1, num_features)).reshape(num_spires, total_timesteps, num_features)

    #save scaler 
    joblib.dump(Scaler, generated_data_folder+"minmax_scaler.joblib")


    # --- Create Graph ---
    print("Creating graph structure...")
    # Use a distance threshold (adjust value based on your location scale)
    edge_index, edge_weight = create_graph_data(locations, threshold=args.dist_threshold, k=args.knn)
    edge_index = edge_index.to(device)
    edge_weight = edge_weight.to(device) # Pass weights if calculated and meaningful

    train_dataset = SpireTimeSeriesDataset(scaled_data, args.seq_len, args.pred_len)

    # train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, drop_last=True)

    #val split
    val_size = int(0.2 * len(train_dataset))
    train_size = len(train_dataset) - val_size
    train_dataset, val_dataset = torch.utils.data.random_split(train_dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, drop_last=True)

    print(f"Train size: {len(train_loader)}, Validation size: {len(val_loader)}")

    # --- Model, Loss, Optimizer ---
    print("Initializing model...")
    model = STGNN(
        num_nodes=num_spires,
        num_features=num_features,
        seq_len=args.seq_len,
        pred_len=args.pred_len,
        gcn_hidden_dim=args.gcn_dim,
        gru_hidden_dim=args.gru_dim,
        dropout=args.dropout
    ).to(device)

    criterion = nn.MSELoss() # Mean Squared Error is common for regression
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    # Optional: Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, factor=0.5)

    print(f"Model:\n{model}")
    num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Number of trainable parameters: {num_params}")

    # --- Training Loop ---
    print("Starting training...")
    best_val_loss = float('inf')
    patience_counter = 0

    for epoch in range(args.epochs):
        model.train()
        epoch_train_loss = 0.0
        start_time = time.time()

        for i, (batch_x, batch_y) in enumerate(train_loader):
            # batch_x shape: (batch_size, num_nodes, seq_len, num_features)
            # batch_y shape: (batch_size, num_nodes, pred_len, num_features) -> squeeze if features=1
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            # If features=1, target might need squeezing if loss expects (batch, node, pred)
            if num_features == 1:
                batch_y = batch_y.squeeze(-1) # -> (batch, node, pred)

            optimizer.zero_grad()
            outputs = model(batch_x, edge_index, edge_weight) # Pass graph info
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_train_loss += loss.item()

        epoch_train_loss /= len(train_loader)
        epoch_time = time.time() - start_time

        # --- Validation ---
        model.eval()
        epoch_val_loss = 0.0
        with torch.no_grad():
            for batch_x_val, batch_y_val in val_loader:
                batch_x_val, batch_y_val = batch_x_val.to(device), batch_y_val.to(device)
                if num_features == 1:
                    batch_y_val = batch_y_val.squeeze(-1)

                outputs_val = model(batch_x_val, edge_index, edge_weight)
                loss_val = criterion(outputs_val, batch_y_val)
                epoch_val_loss += loss_val.item()

        epoch_val_loss /= len(val_loader)

        print(f"Epoch {epoch+1}/{args.epochs} | "
              f"Time: {epoch_time:.2f}s | "
              f"Train Loss: {epoch_train_loss:.6f} | "
              f"Val Loss: {epoch_val_loss:.6f}")

        # Learning rate scheduling and Early stopping
        scheduler.step(epoch_val_loss)

        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            patience_counter = 0
            # Save the best model
            if args.save_path:
                #concatenate save_path with data folder
                save_path = os.path.join(generated_data_folder, args.save_path)
                if not os.path.exists(os.path.dirname(save_path)):
                    os.makedirs(os.path.dirname(save_path))
                torch.save(model.state_dict(), save_path)
                print(f"--- Best model saved to {save_path} ---")
        else:
            patience_counter += 1
            if patience_counter >= args.patience:
                print(f"Early stopping triggered after {args.patience} epochs without improvement.")
                break

    print("Pre-training finished.")
    # Load the best model state for potential later use
    if args.save_path and os.path.exists(args.save_path):
        model.load_state_dict(torch.load(args.save_path))
        print(f"Loaded best model from {args.save_path}")

    # Remember to potentially use the scalers to inverse_transform predictions if needed
    # Example: prediction_real_scale = scalers[spire_index].inverse_transform(prediction_scaled)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STGNN Pre-training for Spire Counts")
    parser.add_argument('--epochs', type=int, default=200, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--seq_len', type=int, default=24, help='Input sequence length (e.g., 12 hours)')
    parser.add_argument('--pred_len', type=int, default=1, help='Prediction horizon (e.g., 3 hours)')
    parser.add_argument('--gcn_dim', type=int, default=32, help='Hidden dimension for GCN layers')
    parser.add_argument('--gru_dim', type=int, default=64, help='Hidden dimension for GRU layers')
    parser.add_argument('--dist_threshold', type=float, default=None, help='Distance threshold for graph edges (adjust based on location scale)')
    parser.add_argument('--knn', type=int, default=5, help='Number of nearest neighbors for graph edges (use instead of threshold)')
    parser.add_argument('--dropout', type=float, default=0.0, help='Dropout rate')
    parser.add_argument('--patience', type=int, default=10, help='Patience for early stopping')
    parser.add_argument('--save_path', type=str, default='./pretrained_stgnn.pth', help='Path to save the best model')
    parser.add_argument('--gpu', type=int, default=0, help='GPU ID to use, -1 for CPU')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')

    args = parser.parse_args()


    if args.gpu >= 0 and torch.cuda.is_available():
        device = torch.device(f"cuda:{args.gpu}")
        print(f"Using GPU: {torch.cuda.get_device_name(args.gpu)}")
    else:
        device = torch.device("cpu")
        print("Using CPU")

    # Set random seeds for reproducibility
    seed = args.seed        
    np.random.seed(seed)       # Numpy module
    torch.manual_seed(seed)    # PyTorch CPU operations

    # If you are using CUDA (GPU)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)         # Current GPU
        torch.cuda.manual_seed_all(seed) 

    #save all parameters in a yaml
    import yaml
    with open(generated_data_folder+"params.yaml", 'w') as file:
        yaml.dump(vars(args), file)

    run_training(args, device)