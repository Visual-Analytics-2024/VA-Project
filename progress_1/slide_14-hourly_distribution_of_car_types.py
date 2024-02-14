import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_path = 'data/lekagul_sensor_data.csv'
data = pd.read_csv(data_path)
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data['Hour'] = data['Timestamp'].dt.hour
hourly_distribution = data.groupby(['car-type', 'Hour']).size().unstack(fill_value=0)
max_count = hourly_distribution.max().max()

labels = np.array(hourly_distribution.columns)
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
colors = plt.cm.viridis(np.linspace(0, 1, len(hourly_distribution)))

for index, (car_type, stats) in enumerate(hourly_distribution.iterrows()):
    stats = stats.values
    stats = np.concatenate((stats, [stats[0]]))
    ax.plot(angles, stats, color=colors[index], linewidth=2, label=f"Car Type {car_type}")
    ax.fill(angles, stats, color=colors[index], alpha=0.25)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_yticks(np.linspace(0, max_count, num=5))
ax.set_yticklabels(np.linspace(0, max_count, num=5).astype(int))

plt.title('Hourly Distribution of Car Types', size=20, color='black', y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
plt.savefig('output/hourly_distribution_of_car_types.png', bbox_inches='tight')
plt.show()
