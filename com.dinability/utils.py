import numpy as np
import pandas as pd

def rating_aggregate(df):
        df['rating'] = df.apply(lambda row: np.nanmean((row['rating_aspect_1'],row['rating_aspect_2'],
                row['rating_aspect_3'],row['rating_aspect_4'],row['rating_aspect_5'])), axis=1)
        return df

def pop_aggregate(df1, df2):
        df_temp = df2.groupby('restaurant_name')[['user_id']].size().reset_index()
        df_temp.columns = ['restaurant_name', 'pop']
        df1 = pd.merge(df2, df_temp, on='restaurant_name')
        return df1