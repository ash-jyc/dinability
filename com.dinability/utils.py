import numpy as np

def rating_aggregate(df):
        print(df[['rating_aspect_1']].head())
        df['rating'] = df.apply(lambda row: np.nanmean((row['rating_aspect_1'],row['rating_aspect_2'],
                row['rating_aspect_3'],row['rating_aspect_4'],row['rating_aspect_5'])), axis=1)
        return df