import pandas as pd
import matplotlib.pyplot as plt

file_path = 'data/lekagul_sensor_data.csv'
data = pd.read_csv(file_path)

data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data['Day of the Week'] = data['Timestamp'].dt.day_name()

prefixes = ['gate', 'entrance', 'camping', 'general-gate', 'ranger-base', 'ranger-stop']
prefix_labels = ['Gate', 'Entrance', 'Camping', 'General-Gate', 'Ranger-Base', 'Ranger-Stop']

combined_data_expanded_corrected = pd.DataFrame()

all_car_types = data['car-type'].unique()
all_car_types.sort()
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

for prefix, label in zip(prefixes, prefix_labels):
    prefix_filtered_data = data[data['gate-name'].str.startswith(prefix)]
    prefix_grouped_data = prefix_filtered_data.groupby(['Day of the Week', 'car-type']).size().unstack(fill_value=0)
    prefix_grouped_data = prefix_grouped_data.reindex(columns=all_car_types, fill_value=0)
    prefix_grouped_data = prefix_grouped_data.reindex(order)
    prefix_grouped_data.index = pd.MultiIndex.from_product([[label], prefix_grouped_data.index],
                                                           names=['Entry Type', 'Day of the Week'])
    combined_data_expanded_corrected = pd.concat([combined_data_expanded_corrected, prefix_grouped_data])

combined_data_expanded_corrected.index = ['{}-{}'.format(*idx) for idx in combined_data_expanded_corrected.index]

color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

fig, ax = plt.subplots(figsize=(24, 10))
combined_data_expanded_corrected.plot(kind='bar', stacked=True, ax=ax, width=0.8, color=color_palette)
plt.title('Vehicle count by Gate type and Day of the Week', pad=40, fontsize=20, fontweight='bold')
plt.xlabel('Day of the Week and Gate Type', fontweight='bold')
plt.ylabel('Number of Entries', fontweight='bold')
plt.xticks(rotation=90)
plt.legend(title='Car Type', bbox_to_anchor=(1.01, 1), loc='upper left')

ylim = ax.get_ylim()
y_pos_for_text = ylim[1] + (ylim[1] - ylim[0]) * 0.01

for prefix in prefix_labels[:-1]:
    indices = [i for i, label in enumerate(combined_data_expanded_corrected.index) if label.startswith(prefix)]
    if indices:
        end_index = indices[-1]
        ax.axvline(x=end_index + 0.5, color='grey', linestyle='--')

for prefix in prefix_labels:
    indices = [i for i, label in enumerate(combined_data_expanded_corrected.index) if label.startswith(prefix)]
    if indices:
        start_index = indices[0]
        end_index = indices[-1]
        middle_index = (start_index + end_index) / 2
        ax.text(middle_index, y_pos_for_text, prefix, ha='center', va='bottom', fontsize=10, transform=ax.transData)

plt.subplots_adjust(top=0.88)
plt.tight_layout()
plt.savefig('output/vehicle_count_by_gate_type_and_day_of_week.png')
plt.show()
