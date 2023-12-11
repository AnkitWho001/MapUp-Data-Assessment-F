import pandas as pd

#ques1
def generate_car_matrix():
    readf = pd.read_csv('dataset-1.csv')
    df = readf.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    for i in range(min(df.shape)):
        df.iloc[i, i] = 0

    return df

#ques2

def get_type_count(df):
  
    
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    
    type_counts = df['car_type'].value_counts().sort_index()

    dict = type_counts.to_dict()
    return dict

#ques3

def filter_routes(df):

    routes = df.groupby('route')['truck'].mean()
    filtered_routes = routes[routes > 7].index.tolist()  
    return sorted(filtered_routes)

#ques4

def multiply_matrix(df):

    modified_df = df.copy() 

    modified_df[df > 20] *= 0.75
    modified_df[(df <= 20) & (df > 0)] *= 1.25

    modified_df = modified_df.round(1)
    return modified_df

#ques5

def multiply_matrix(input_df):
    
    modified_df = input_df.copy()  # Create a copy of the input DataFrame

    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    modified_df = modified_df.round(1)
    return modified_df

#ques6


def verify_time_completeness(df):
   
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    df['time_diff'] = df['end_timestamp'] - df['start_timestamp']

    completeness_check = df.groupby(['id', 'id_2']).apply(
        lambda x: (x['time_diff'].min() >= pd.Timedelta(days=7)) 
                  and (x['start_timestamp'].min().time() == pd.Timestamp('00:00:00').time()) 
                  and (x['end_timestamp'].max().time() == pd.Timestamp('23:59:59').time())
    )

    return completeness_check
