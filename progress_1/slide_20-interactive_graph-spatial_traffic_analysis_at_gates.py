import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

file_path = 'data/lekagul_sensor_data.csv'
data = pd.read_csv(file_path)

node_positions_path = 'data/gate_positions.csv'
node_positions = pd.read_csv(node_positions_path).set_index('gate_name')

filtered_data = data.dropna(subset=['gate-name'])
filtered_data_sorted = filtered_data.sort_values(by=['car-id', 'Timestamp'])
trip_counts = defaultdict(int)

for (_, group) in filtered_data_sorted.groupby('car-id'):
    origins = group['gate-name'].iloc[:-1].reset_index(drop=True)
    destinations = group['gate-name'].iloc[1:].reset_index(drop=True)
    for origin, destination in zip(origins, destinations):
        # Sort the origin and destination to remove direction
        sorted_gates = tuple(sorted([origin, destination]))
        trip_counts[sorted_gates] += 1

categories = sorted(set([key[0] for key in trip_counts.keys()] + [key[1] for key in trip_counts.keys()]))

labels = categories
category_indices = {category: i for i, category in enumerate(categories)}
source = [category_indices[origin] for origin, _ in trip_counts]
target = [category_indices[destination] for _, destination in trip_counts]
value = [count for count in trip_counts.values()]

x_positions = [node_positions.loc[category, 'x_coordinate'] for category in categories]
y_positions = [node_positions.loc[category, 'y_coordinate'] for category in categories]

# Create the Sankey diagram with positions
fig = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        label=labels,
        x=x_positions,
        y=y_positions,
        pad=10,
        thickness=20,
        line=dict(color="black", width=0.5),
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    )
))

fig.update_layout(title_text="Spatial Traffic Analysis at Gates", font_size=10)
fig.show()
