def rating_aggregate(df):
    df['rating'] = df.apply(lambda row: (df['rating_aspect_1']+df['rating_aspect_2']+
            df['rating_aspect_3']+df['rating_aspect_4']+df['rating_aspect_5'])/5)
    return df