import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

file_path = 'data/lekagul_sensor_data.csv'
data = pd.read_csv(file_path)

filtered_data = data.dropna(subset=['gate-name'])
filtered_data_sorted = filtered_data.sort_values(by=['car-id', 'Timestamp'])
trip_counts = defaultdict(int)

for (_, group) in filtered_data_sorted.groupby('car-id'):
    origins = group['gate-name'].iloc[:-1].reset_index(drop=True)
    destinations = group['gate-name'].iloc[1:].reset_index(drop=True)
    for origin, destination in zip(origins, destinations):
        trip_counts[(origin, destination)] += 1

categories = sorted(set([key[0] for key in trip_counts.keys()] + [key[1] for key in trip_counts.keys()]))
labels = [category for category in categories] + [category for category in categories]
category_indices = {category: i for i, category in enumerate(categories)}
source = [category_indices[origin] for origin, _ in trip_counts]
target = [len(categories) + category_indices[destination] for _, destination in trip_counts]
value = [count for count in trip_counts.values()]

colors = [
    '#d67f7f', '#fd858f', '#eba093', '#dc9494', '#e27da2',
    '#fd9394', '#e7a195', '#e38485', '#c5a494', '#c094a1',
    '#d4acac', '#c4a79d', '#dab68e', '#bab4ae', '#bbabb2',
    '#bcb0b1', '#ebaa93', '#f0d080', '#faae8e', '#ecab96',
    '#ffd07a', '#fdc56f', '#f9cd7b', '#ffb573', '#7aced6',
    '#80eee1', '#83def6', '#8bd9e0', '#89cff6', '#74e9d8',
    '#92caf7', '#96e7d6', '#d8e8d6', '#cbe4af', '#c0f2b1',
    '#d8fecd', '#b9edd2', '#caecca', '#c4dcd3', '#c0f1ba'
]

node_colors = [colors[i % len(colors)] for i in range(len(categories))] * 2
link_colors = [colors[category_indices[origin] % len(colors)] for origin, _ in trip_counts]

link = {
    'source': source,
    'target': target,
    'value': value,
    'color': link_colors
}

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=node_colors
    ),
    link=link
)])

fig.update_layout(title_text="Origin Destination with All Gates", font_size=10)
fig.show()
