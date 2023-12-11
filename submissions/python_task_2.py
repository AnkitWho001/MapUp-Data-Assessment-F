#ques1

import pandas as pd
import numpy as np

def calculate_distance_matrix(df):
   
    grouped = df.groupby(['from', 'to'])['distance'].sum().reset_index()

    pivot_table = pd.pivot_table(grouped, values='distance', index='from', columns='to', fill_value=0)

    distance_array = pivot_table.to_numpy()

    distance_array += distance_array.T

    for i in range(distance_array.shape[0]):
        for j in range(distance_array.shape[1]):
            for k in range(distance_array.shape[0]):
                distance_array[i, j] = max(distance_array[i, j], distance_array[i, k] + distance_array[k, j])

    np.fill_diagonal(distance_array, 0)

    distance_matrix = pd.DataFrame(distance_array, index=pivot_table.index, columns=pivot_table.columns)

    return distance_matrix

#ques2

def unroll_distance_matrix(distance_df):
  
    distance_df_reset = distance_df.reset_index()

    unrolled_df = pd.melt(distance_df_reset, id_vars='index', value_name='distance')

    unrolled_df = unrolled_df.rename(columns={'index': 'id_start', 'variable': 'id_end'})
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    return unrolled_df.reset_index(drop=True)

#ques3

def find_ids_within_ten_percentage_threshold(df, reference_value):

    reference_df = df[df['id_start'] == reference_value]

    average_distance = reference_df['distance'].mean()

    threshold_range = (0.9 * average_distance, 1.1 * average_distance)

    filtered_ids = df[(df['distance'] >= threshold_range[0]) & (df['distance'] <= threshold_range[1])]['id_start']
    sorted_filtered_ids = sorted(filtered_ids.unique())

    return sorted_filtered_ids

#ques4

import pandas as pd

def calculate_toll_rate(df):
   
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle, rate in rate_coefficients.items():
        df[vehicle] = df['distance'] * rate

    return df

#ques5

def calculate_time_based_toll_rates(df):
   
    weekday_time_ranges = [
        (datetime.time(0, 0, 0), datetime.time(10, 0, 0)),
        (datetime.time(10, 0, 0), datetime.time(18, 0, 0)),
        (datetime.time(18, 0, 0), datetime.time(23, 59, 59))
    ]
    weekend_time_range = (datetime.time(0, 0, 0), datetime.time(23, 59, 59))

    weekday_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday',
                   5: 'Saturday', 6: 'Sunday'}

    for day in range(7):
        for start_time, end_time in weekday_time_ranges:
            mask = ((df['start_time'] >= start_time) & (df['start_time'] < end_time)) & (df['start_day'] == day)
            df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.8 if day < 5 else 0.7
            df.loc[mask, ['start_day', 'start_time', 'end_day', 'end_time']] = weekday_map[day], start_time, weekday_map[day], end_time

        mask = ((df['start_time'] >= weekend_time_range[0]) & (df['start_time'] <= weekend_time_range[1])) & (df['start_day'] == day)
        df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.7
        df.loc[mask, ['start_day', 'start_time', 'end_day', 'end_time']] = weekday_map[day], weekend_time_range[0], weekday_map[day], weekend_time_range[1]

    return df


