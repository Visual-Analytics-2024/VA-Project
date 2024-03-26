import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
from collections import defaultdict
import pandas as pd
from dash.dependencies import Input, Output
from scipy.stats import norm

pd.set_option('display.max_columns', 8)

gate_positions = pd.read_csv('gate_positions.csv')
trips_data = pd.read_csv('all_trips_data.csv')
trips_data['start-time'] = pd.to_datetime(trips_data['start-time'])
trips_data = trips_data[trips_data['start-gate'] != trips_data['end-gate']]  # Filter out self-loops
points = [(row['gate_name'], row['x_coordinate'], row['y_coordinate']) for index, row in gate_positions.iterrows()]
initial_trip_counts = trips_data.groupby(['start-gate', 'end-gate']).size().reset_index(name='trips_count')
initial_od_counts = [(row['start-gate'], row['end-gate'], row['trips_count']) for index, row in
                     initial_trip_counts.iterrows()]

prefixes = ['gate', 'entrance', 'camping', 'general-gate', 'ranger-base', 'ranger-stop']
color_palette = ['#e88693', '#bb9ab1', '#dab68e', '#ffca7a', '#7fecd8', '#c7e4b9']

# Month range for the slider
month_marks = {
    0: '2015-05',
    1: '2015-06',
    2: '2015-07',
    3: '2015-08',
    4: '2015-09',
    5: '2015-10',
    6: '2015-11',
    7: '2015-12',
    8: '2016-01',
    9: '2016-02',
    10: '2016-03',
    11: '2016-04',
    12: '2016-05',
}

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server
application = server


def get_point_color(point_name, prefixes, color_palette):
    for index, prefix in enumerate(prefixes):
        if point_name.startswith(prefix):
            return color_palette[index % len(color_palette)]
    return '#7f7f7f'


point_colors = {p[0]: get_point_color(p[0], prefixes, color_palette) for p in points}


# Generate bezier points with control points
def generate_bezier_points(p0, p1, t=np.linspace(0, 1, 100), offset=1, upwards=True):
    mid_x = (p0[0] + p1[0]) / 2
    mid_y = (p0[1] + p1[1]) / 2
    dx = abs(p1[0] - p0[0])
    dy = abs(p1[1] - p0[1])

    if dx > dy:
        ctrl_point = (mid_x, mid_y + offset if upwards else mid_y - offset)
    else:
        ctrl_point = (mid_x + offset if upwards else mid_x - offset, mid_y)

    x, y = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * ctrl_point[0] + t ** 2 * p1[0], \
           (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * ctrl_point[1] + t ** 2 * p1[1]

    return x, y


def scale_value(value, min_val, max_val, min_scale, max_scale):
    try:
        value_scaled = (value - min_val) / (max_val - min_val) * (max_scale - min_scale) + min_scale
    except ZeroDivisionError:
        if value == min_val:
            value_scaled = max_scale
        else:
            value_scaled = min_scale
    return value_scaled


def create_figure(filtered_od_counts):
    fig = go.Figure()

    if len(filtered_od_counts) > 0:
        point_index = {p[0]: (p[1], p[2]) for p in points}

        # Process filtered od counts to group them by points
        line_groups = defaultdict(list)
        for from_point, to_point, count in filtered_od_counts:
            sorted_points = tuple(sorted([from_point, to_point]))
            line_groups[sorted_points].append((from_point, to_point, count))

        # Calculate total traffic for each point
        total_traffic = defaultdict(int)
        for from_point, to_point, count in filtered_od_counts:
            total_traffic[from_point] += count
            total_traffic[to_point] += count

        # Find min and max for scaling
        min_count = min(count for _, _, count in filtered_od_counts)
        max_count = max(count for _, _, count in filtered_od_counts)
        min_traffic = min(total_traffic.values())
        max_traffic = max(total_traffic.values())

        # Generate and add Bezier curves for each line
        for (point_a, point_b), trips in line_groups.items():
            for from_point, to_point, count in trips:
                start_point = point_index[from_point]
                end_point = point_index[to_point]

                # Determine curve direction and offset
                upwards = from_point < to_point
                distance = np.sqrt((end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2)
                offset = distance / 35

                x_bezier, y_bezier = generate_bezier_points(start_point, end_point, offset=offset, upwards=upwards)
                line_thickness = scale_value(count, min_count, max_count, 1, 10)  # Scale line thickness

                fig.add_trace(go.Scatter(x=x_bezier, y=y_bezier, mode='lines', line_shape='spline',
                                         line=dict(width=line_thickness, color='#d0cccc'),
                                         hoverinfo='text', text=f'From {from_point} to {to_point}<br>Trips: {count}',
                                         showlegend=False))

        for p in points:
            p_name, p_x, p_y = p
            traffic = total_traffic[p_name]
            point_size = scale_value(traffic, min_traffic, max_traffic, 10, 40)  # Scale point size
            point_color = point_colors[p_name]

            fig.add_trace(go.Scatter(x=[p_x], y=[p_y], mode='markers',
                                     marker=dict(size=max(point_size, 0), color=point_color),
                                     hoverinfo='text', text=f'{p_name}<br>Total Traffic: {traffic}', showlegend=False))

    fig.update_layout(
        xaxis_visible=False, yaxis_visible=False, plot_bgcolor='white',
        # legend_title="Gate Types",
        # legend=dict(
        #     yanchor="top",
        #     y=0.99,
        #     xanchor="right",
        #     x=0.01
        # ),
        margin=dict(l=300, r=300, t=0, b=0),
        # width=600,
        # height=600,
    )

    # Display the figure with the updated layout
    # fig.show(config={'scrollZoom': True})
    return fig

prefixes_colors = {
    'gate': '#e88693',
    'entrance': '#bb9ab1',
    'camping': '#dab68e',
    'general-gate': '#ffca7a',
    'ranger-base': '#7fecd8',
    'ranger-stop': '#c7e4b9'
}

app.layout = html.Div([
    html.H1("Filter-Driven Anomaly Detection Based on Trip Time",
            style={
                'padding-left': '16px',
                'fontSize': '24px'
            }),

    dcc.Graph(
        id='map-visualization',
        figure=create_figure(initial_od_counts),
        config={
            'scrollZoom': True
        },
        style={'margin-top': '150px'}
    ),

    html.Div([
        dcc.RangeSlider(
            id='time-period-slider',
            min=0,
            max=12,
            value=[0, 12],
            marks=month_marks,
            step=1,
        ),
    ], style={
        # 'padding-top': '10px',
        # 'padding-left': '300px',
        # 'padding-right': '300px'
        'position': 'absolute',
        'top': '70px',
        'left': '300px',
        'right': '300px'
    }),

    html.H1("Car Type:",
            style={
                'position': 'absolute',
                'padding-left': '16px',
                'top': '48px',
                'fontSize': '16px'
            }),

    html.Div([
        dcc.Checklist(
            id='car-type-selection',
            options=[
                {'label': 'All', 'value': 'ALL'},
                {'label': 'Car Type: 1', 'value': '1'},
                {'label': 'Car Type: 2', 'value': '2'},
                {'label': 'Car Type: 2p', 'value': '2P'},
                {'label': 'Car Type: 3', 'value': '3'},
                {'label': 'Car Type: 4', 'value': '4'},
                {'label': 'Car Type: 5', 'value': '5'},
                {'label': 'Car Type: 6', 'value': '6'},
            ],
            value=['ALL'],
            labelStyle={'display': 'block'}
        ),
    ], style={
        'position': 'absolute',
        'left': '20px',
        'top': '80px',
    }),

    html.H1("Start Gate Type:",
            style={
                'position': 'absolute',
                'padding-left': '16px',
                'top': '248px',
                'fontSize': '16px'
            }),

    html.Div([
        dcc.Checklist(
            id='start-gate-type-selection',
            options=[
                {'label': 'All', 'value': 'ALL'},
                {'label': 'Gate', 'value': 'gate'},
                {'label': 'Entrance', 'value': 'entrance'},
                {'label': 'Camping', 'value': 'camping'},
                {'label': 'General-Gate', 'value': 'general-gate'},
                {'label': 'Ranger-Base', 'value': 'ranger-base'},
                {'label': 'Ranger-Stop', 'value': 'ranger-stop'}
            ],
            value=['ALL'],
            labelStyle={'display': 'block'}
        ),
    ], style={
        'position': 'absolute',
        'left': '20px',
        'top': '280px',
    }),

    html.H1("End Gate Type:",
            style={
                'position': 'absolute',
                'padding-left': '16px',
                'top': '448px',
                'fontSize': '16px'
            }),

    html.Div([
        dcc.Checklist(
            id='end-gate-type-selection',
            options=[
                {'label': 'All', 'value': 'ALL'},
                {'label': 'Gate', 'value': 'gate'},
                {'label': 'Entrance', 'value': 'entrance'},
                {'label': 'Camping', 'value': 'camping'},
                {'label': 'General-Gate', 'value': 'general-gate'},
                {'label': 'Ranger-Base', 'value': 'ranger-base'},
                {'label': 'Ranger-Stop', 'value': 'ranger-stop'}
            ],
            value=['ALL'],
            labelStyle={'display': 'block'}
        ),
    ], style={
        'position': 'absolute',
        'left': '20px',
        'top': '480px',
    }),

    html.Div([
        dcc.RadioItems(
            id='anomaly-selection',
            options=[
                {'label': 'Normal', 'value': 'NORMAL'},
                {'label': 'Anomaly', 'value': 'ANOMALY'}
            ],
            value='NORMAL',
            labelStyle={'display': 'block'}
        )
    ], style={
        # 'paddingTop': '5px',
        # 'padding-left': '20px'
        'position': 'absolute',
        'top': '130px',
        'left': '600px',
    }),

    html.Div([
        html.Label('Confidence Level: ', style={'color': 'red'}),
        dcc.Input(id='confidence-interval-input',
                  type='number',
                  value=95,
                  min=1,
                  max=100,
                  style={'width': '40px'})
    ], style={
        'position': 'absolute',
        'top': '152px',
        'left': '700px',
    }),
])


@app.callback(
    Output('map-visualization', 'figure'),
    [Input('car-type-selection', 'value'),
     Input('start-gate-type-selection', 'value'),
     Input('end-gate-type-selection', 'value'),
     Input('time-period-slider', 'value'),
     Input('anomaly-selection', 'value'),
     Input('confidence-interval-input', 'value')]
)
def update_graph(selected_car_types, selected_start_gate_types, selected_end_gate_types, selected_time_period,
                 selected_anomaly_type, confidence_interval):
    # Filter trips_data based on the selected car types
    if 'ALL' in selected_car_types:
        filtered_trips_data = trips_data
    elif len(selected_car_types) != 0:
        filtered_trips_data = trips_data[trips_data['car-type'].isin(selected_car_types)]
    else:
        filtered_trips_data = []

    # Filter trips_data based on the selected time period
    if len(filtered_trips_data) > 0:
        start_month = month_marks[selected_time_period[0]]
        end_month = month_marks[selected_time_period[1]]
        start_date = pd.to_datetime(start_month, format='%Y-%m')
        end_date = pd.to_datetime(end_month, format='%Y-%m') + pd.offsets.MonthEnd(1)

        # Filter based on the selected time period
        filtered_trips_data = filtered_trips_data[
            (filtered_trips_data['start-time'] >= start_date) &
            (filtered_trips_data['start-time'] <= end_date)
            ]

    # Filter by start-gate type, if 'All' is not selected
    if 'ALL' not in selected_start_gate_types and len(filtered_trips_data) > 0:
        start_gate_type_filter = filtered_trips_data['start-gate'].apply(
            lambda x: any(x.startswith(gate_type) for gate_type in selected_start_gate_types))
        filtered_trips_data = filtered_trips_data[start_gate_type_filter]

    # Filter by end-gate type, if 'All' is not selected
    if 'ALL' not in selected_end_gate_types and len(filtered_trips_data) > 0:
        end_gate_type_filter = filtered_trips_data['end-gate'].apply(
            lambda x: any(x.startswith(gate_type) for gate_type in selected_end_gate_types))
        filtered_trips_data = filtered_trips_data[end_gate_type_filter]

    # Filter by anomaly
    if selected_anomaly_type == 'ANOMALY' and len(filtered_trips_data) > 0:
        if 'ALL' not in selected_start_gate_types and 'ALL' not in selected_end_gate_types and 'ALL' not in selected_car_types:
            confidence_fraction = confidence_interval / 100.0
            z_value = norm.ppf((1 + confidence_fraction) / 2)  # Calculate the z-value

            # Group by the unique combinations of 'start-gate' and 'end-gate'
            grouped_data = filtered_trips_data.groupby(['start-gate', 'end-gate'])
            anomalies_data_list = pd.DataFrame()

            for (start_gate, end_gate), group in grouped_data:
                # Calculate mean and standard deviation of 'time-taken' for the group
                mean_time_taken = group['time-taken'].mean()
                std_dev_time_taken = group['time-taken'].std()

                # Identify anomaly trips within the group based on z_value * std_dev_time_taken
                anomalies = group[(group['time-taken'] < mean_time_taken - z_value * std_dev_time_taken) |
                                  (group['time-taken'] > mean_time_taken + z_value * std_dev_time_taken)]
                anomalies_data_list = pd.concat([anomalies_data_list, anomalies])

            filtered_trips_data = anomalies_data_list

    if len(filtered_trips_data) > 0:
        trip_counts = filtered_trips_data.groupby(['start-gate', 'end-gate']).size().reset_index(name='trips_count')
        od_counts = [(row['start-gate'], row['end-gate'], row['trips_count']) for index, row in trip_counts.iterrows()]
        fig = create_figure(od_counts)
    else:
        fig = create_figure([])

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
