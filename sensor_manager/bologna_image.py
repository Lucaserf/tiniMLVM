import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import osmnx as ox

# Ensure the directory for sensor data exists
os.makedirs("sensor_manager/sensor_data", exist_ok=True)
os.makedirs(
    "sensor_manager/manager_data", exist_ok=True
)  # Assuming this might be needed too


# Helper function to calculate distance (from notebook cell 8bae912e)
def get_distance(lat1, lon1, lat2, lon2):
    r = 6371  # Radius of the earth in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = r * c  # Distance in km
    return distance


# Function to get spire key values and save data (from notebook cell 8bae912e)
def get_spire_key_values(key, position_range, distance_max, df_sensors):
    spire_key_data = df_sensors[df_sensors["chiave"] == key]
    if spire_key_data.empty:
        return 0, None

    position_str = spire_key_data["geopoint"].values[0]
    position = [float(i) for i in position_str.split(",")]

    distance = get_distance(
        position[0], position[1], position_range[0], position_range[1]
    )
    if distance > distance_max:
        return 0, None

    columns_keep = [
        df_sensors.columns[i] for i in range(2, 26)
    ]  # Assuming columns 2 to 25 are relevant
    spire_key_data_filtered = spire_key_data[columns_keep]
    spire_key_stacked = spire_key_data_filtered.stack()

    if len(spire_key_stacked) < 8000:  # Condition from notebook
        return 0, None

    # Use a string representation of position that's filename-friendly
    position_filename_str = f"{position[0]:.6f}_{position[1]:.6f}".replace(".", "_")
    file_path = f"sensor_manager/sensor_data/spire_{key}_{position_filename_str}.csv"

    try:
        spire_key_stacked.to_csv(file_path, index=False, header=False)
        return (
            1,
            position,
        )  # Return position for use if needed, though original didn't explicitly
    except Exception as e:
        print(f"Error writing file for key {key}: {e}")
        return 0, None


# Load main sensor data (from notebook cell fe09a636)
home = os.environ.get("HOME", ".")
# os.chdir(f"{home}/tiniMLVM") # Assuming script is run from tiniMLVM root
sensor_data_path = "smart_city/spire_2024.csv"
try:
    df = pd.read_csv(sensor_data_path, sep=";")
except FileNotFoundError:
    print(f"Error: Main sensor data file not found at {sensor_data_path}")
    print(
        "Please ensure the path is correct and the script is run from the project root (/home/lucaserf/tiniMLVM)."
    )
    exit()

max_value = df["chiave"].max()

# Generate list_keys (from notebook cell 8bae912e)
list_keys_initial = []
count = 0
number_of_spires_to_process = 160  # As in notebook
bologna_position_center = [44.494887, 11.342616]  # As in notebook
max_distance_from_center = 1  # km, as in notebook

print(
    f"Processing up to {max_value} keys to find {number_of_spires_to_process} spires within {max_distance_from_center}km of {bologna_position_center}..."
)
key_iter = 0
while count < number_of_spires_to_process and key_iter < int(max_value):
    key_iter += 1
    if key_iter == 3:  # Skip key 3 as in notebook
        continue
    adding, _ = get_spire_key_values(
        key_iter, bologna_position_center, max_distance_from_center, df
    )
    if adding:
        list_keys_initial.append(key_iter)
        count += 1
print(f"Found {count} initial spires: {list_keys_initial}")

# Filter list_keys to keep only connected spires (from notebook cell c9fb76ee)
radius_connectivity = 150  # meters, as in notebook
connected_spires = set([])
if not list_keys_initial:
    print("No initial spires found to check for connectivity.")
    list_keys = []
else:
    print(f"Filtering spires by connectivity (radius: {radius_connectivity}m)...")
    for i in range(len(list_keys_initial)):
        for j in range(i + 1, len(list_keys_initial)):
            spire_key1_data = df[df["chiave"] == list_keys_initial[i]]
            spire_key2_data = df[df["chiave"] == list_keys_initial[j]]

            if spire_key1_data.empty or spire_key2_data.empty:
                continue

            pos1_str = spire_key1_data["geopoint"].values[0]
            pos1 = [float(k) for k in pos1_str.split(",")]
            pos2_str = spire_key2_data["geopoint"].values[0]
            pos2 = [float(k) for k in pos2_str.split(",")]

            distance_between_spires = get_distance(pos1[0], pos1[1], pos2[0], pos2[1])

            if distance_between_spires < (
                radius_connectivity * 1e-3
            ):  # Convert radius to km
                connected_spires.add(list_keys_initial[i])
                connected_spires.add(list_keys_initial[j])

    list_keys = list(connected_spires)
    print(f"Found {len(list_keys)} connected spires: {list_keys}")

    # Optional: Remove files of non-connected spires (as in notebook)
    # all_spires_in_data_dir = set()
    # if os.path.exists("sensor_manager/sensor_data"):
    #     for filename in os.listdir("sensor_manager/sensor_data"):
    #         if filename.startswith("spire_"):
    #             try:
    #                 key_from_file = int(filename.split("_")[1])
    #                 all_spires_in_data_dir.add(key_from_file)
    #             except (IndexError, ValueError):
    #                 continue
    # non_connected_spires_to_remove_files_for = all_spires_in_data_dir - connected_spires
    # for spire_key_to_remove in non_connected_spires_to_remove_files_for:
    #     # This part needs careful construction of filename to match what get_spire_key_values created
    #     # For simplicity, skipping exact file removal here as filename format can vary.
    #     pass


if not list_keys:
    print("No connected spires to plot. Exiting.")
    exit()

# --- OSMnx and Matplotlib plotting ---
label_attack = "no_attack"  # From notebook cell 421d06f5
period = 2  # From notebook cell 421d06f5
data_manager_folder = "sensor_manager/manager_data/"

print("Downloading road network for Bologna...")
# Use center from armir_code.py for consistency if desired, or keep existing graph_from_place
# center_coords = (44.49381, 11.33875) # As in armir_code.py
# G = ox.graph_from_point(center_coords, dist=3000, network_type="drive")
G = ox.graph_from_place("Bologna, Italy", network_type="drive")  # Current method
nodes, edges = ox.graph_to_gdfs(G)  # Get both nodes and edges


# Style: assign grayscale color + visual width based on road type (from armir_code.py)
def style_road(highway):
    if isinstance(highway, list):
        highway = highway[0]
    styles = {
        "motorway": {"color": "#111111", "width": 3.0},
        "trunk": {"color": "#222222", "width": 2.6},
        "primary": {"color": "#333333", "width": 2.2},
        "secondary": {"color": "#555555", "width": 1.8},
        "tertiary": {"color": "#777777", "width": 1.4},
        "residential": {"color": "#999999", "width": 1.0},
        "service": {"color": "#BBBBBB", "width": 0.8},
        "unclassified": {"color": "#CCCCCC", "width": 0.8},
    }
    default = {"color": "#DDDDDD", "width": 0.6}
    return pd.Series(styles.get(highway, default))


# Apply styles to edges
edges[["color", "width"]] = edges["highway"].apply(style_road)


fig, ax = plt.subplots(figsize=(12, 12))
# Plot with styled roads
edges.plot(ax=ax, color=edges["color"], linewidth=edges["width"], zorder=1)
print("Plotting sensor data...")

plotted_lons = []
plotted_lats = []

for spire_id in list_keys:
    spire_data_row = df[df["chiave"] == spire_id]
    if spire_data_row.empty:
        print(f"Warning: Spire ID {spire_id} not found in main DataFrame. Skipping.")
        continue

    position_str = spire_data_row["geopoint"].values[0]
    lat, lon = [float(i) for i in position_str.split(",")]

    marker_color = "grey"  # Default
    label_text = str(spire_id)

    output_file_path = f"{data_manager_folder}output_{spire_id}.txt"
    try:
        with open(output_file_path, "r") as f:
            lines = f.readlines()
        if len(lines) > period:  # Check if period index exists
            line_content = lines[period]
            if "No" in line_content:
                marker_color = "blue"
            elif "Local" in line_content:
                marker_color = "red"
            elif "Systematic" in line_content:
                marker_color = "orange"
        else:
            print(
                f"Warning: Not enough lines in {output_file_path} for period {period}. Using default color for spire {spire_id}."
            )

    except FileNotFoundError:
        print(
            f"Warning: Output file {output_file_path} not found. Using default color for spire {spire_id}."
        )
    except Exception as e:
        print(
            f"Error reading {output_file_path}: {e}. Using default color for spire {spire_id}."
        )

    if marker_color == "grey":  # Skip plotting for "Unknown/No File"
        continue

    plotted_lons.append(lon)
    plotted_lats.append(lat)

    # Create 3D pin effect with shadow and offset
    # Shadow (slightly offset to bottom-right)
    shadow_offset_x = 0.0001
    shadow_offset_y = -0.0001
    ax.scatter(
        lon + shadow_offset_x,
        lat + shadow_offset_y,
        color="black",
        s=120,
        alpha=0.3,
        zorder=1,
        marker="o",
    )

    # Main pin body (larger circle)
    ax.scatter(
        lon,
        lat,
        color=marker_color,
        s=150,
        zorder=3,
        edgecolors="black",
        linewidth=2,
        marker="o",
    )

    # Pin top (smaller circle for 3D effect)
    ax.scatter(
        lon,
        lat + 0.00008,
        color=marker_color,
        s=80,
        zorder=4,
        edgecolors="white",
        linewidth=1,
        marker="o",
        alpha=0.9,
    )

    # Pin needle (vertical line)
    ax.plot(
        [lon, lon],
        [lat - 0.0003, lat],
        color="darkgray",
        linewidth=3,
        zorder=2,
        alpha=0.8,
    )
    # ax.text(
    #     lon + 0.00015,
    #     lat + 0.00015,
    #     label_text,
    #     fontsize=8,
    #     color="red",
    #     zorder=3,
    #     path_effects=[pe.withStroke(linewidth=1, foreground="white")],
    # )

# Zoom closer to the plotted sensors
if plotted_lons and plotted_lats:
    min_lon, max_lon = min(plotted_lons), max(plotted_lons)
    min_lat, max_lat = min(plotted_lats), max(plotted_lats)

    # Add a buffer for better visualization
    lon_buffer = (max_lon - min_lon) * 0.30  # 30% buffer
    lat_buffer = (max_lat - min_lat) * 0.30  # 30% buffer

    # Handle cases where there's only one sensor or all sensors are at the same point
    if lon_buffer == 0:
        lon_buffer = 0.005  # Default buffer in degrees
    if lat_buffer == 0:
        lat_buffer = 0.005  # Default buffer in degrees

    ax.set_xlim(min_lon - lon_buffer, max_lon + lon_buffer)
    ax.set_ylim(min_lat - lat_buffer, max_lat + lat_buffer)

# Tilt the view by changing the aspect ratio (from armir_code.py)
ax.set_aspect(0.8)  # smaller = flatter perspective
ax.set_axis_off()

# Create a legend
legend_elements = [
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        label="No Drift",
        markersize=12,
        markerfacecolor="blue",
        markeredgecolor="black",
    ),
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        label="Anomalous Drift",
        markersize=12,
        markerfacecolor="red",
        markeredgecolor="black",
    ),
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        label="Systematic Drift",
        markersize=12,
        markerfacecolor="orange",
        markeredgecolor="black",
    ),
    # Removed "Unknown/No File" from legend
]
ax.legend(handles=legend_elements, loc="lower left", fontsize=20)


output_image_path = (
    f"sensor_manager/map_osmnx_styled_{period}_{label_attack}.png"  # Changed filename
)
plt.savefig(output_image_path, dpi=300, bbox_inches="tight")
print(f"Saved OSMnx map to {output_image_path}")

# plt.show() # Uncomment to display the plot interactively
print("Script finished.")
