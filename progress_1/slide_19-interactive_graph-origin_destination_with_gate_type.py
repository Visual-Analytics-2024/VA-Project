import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

file_path = 'data/lekagul_sensor_data.csv'
data = pd.read_csv(file_path)


def map_gate_to_category(gate_name):
    for prefix in ['camping', 'entrance', 'gate', 'general-gate', 'ranger-base', 'ranger-stop']:
        if gate_name.startswith(prefix):
            return prefix
    return None


data['gate-category'] = data['gate-name'].apply(map_gate_to_category)
filtered_data = data.dropna(subset=['gate-category'])
filtered_data_sorted = filtered_data.sort_values(by=['car-id', 'Timestamp'])
trip_counts = defaultdict(int)
for (_, group) in filtered_data_sorted.groupby('car-id'):
    origins = group['gate-category'].iloc[:-1].reset_index(drop=True)
    destinations = group['gate-category'].iloc[1:].reset_index(drop=True)
    for origin, destination in zip(origins, destinations):
        trip_counts[(origin, destination)] += 1

categories = sorted(set([key[0] for key in trip_counts.keys()] + [key[1] for key in trip_counts.keys()]))
labels = [f'{category} (Origin)' for category in categories] + [f'{category} (Destination)' for category in categories]
category_indices = {category: i for i, category in enumerate(categories)}
source = []
target = []
value = []
colors = ['#e88693', '#bb9ab1', '#dab68e', '#ffca7a', '#7fecd8', '#c7e4b9']
node_colors = [colors[i % len(colors)] for i in range(len(categories))] * 2
link_colors = [colors[category_indices[origin] % len(colors)] for origin, _ in trip_counts]

source = [category_indices[origin] for origin, _ in trip_counts]
target = [len(categories) + category_indices[destination] for _, destination in trip_counts]
value = [count for count in trip_counts.values()]

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

fig.update_layout(title_text="Origin Destination with Gate Type", font_size=10)
fig.show()
