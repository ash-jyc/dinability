from RecommendationStrategy import Pearson, Jaccard, Cosine
import numpy as np
import pandas as pd

class Recommendation:
    def __init__(self, rating_data, item_data, user_col, item_col, rating_col, recommendation_strategy):
        self.rating_data = rating_data
        self.item_data = item_data
        self.user_col = user_col
        self.item_col = item_col
        self.rating_col = rating_col
        self.recommendation_strategy = recommendation_strategy
    
    def rating_predict(self, user, item):
        predict_score = -1.0
        I_user = self.rating_data[(self.rating_data[self.user_col] == user) &
                                (self.rating_data[self.item_col] != item)][[self.item_col, self.rating_col]]
        I_user.loc[:,'Similarity'] = I_user[self.item_col].apply(lambda m: self.recommendation_strategy.similarity(item, m))
        R_user, Sim_user = np.array(I_user[self.rating_col]), np.array(I_user['Similarity'])
        predict_score = np.dot(R_user, Sim_user)/(np.sum(Sim_user)+1e-8)
        return predict_score

    
    def topk(self, user, k=5):
        drop_df = self.rating_data[self.rating_data[self.user_col] == user][self.item_col]
        candidate_df = self.item_data[~self.item_data[self.item_col].isin(drop_df)]
        candidate_df.loc[:,'Predict-score'] = candidate_df[self.item_col].apply(lambda m: self.rating_predict(user, m))
        candidate_df = candidate_df.sort_values(by='Predict-score',ascending=False).head(k)
        return candidate_df

class Ranking:
    def __init__(self, item_data, on):
        self.rating_data = item_data
        self.on = on

    def topk(self, k=5):
        candidate_df = self.rating_data.sort_values(by=self.on, assending=False).head(k)
        return candidate_df


if __name__ == '__main__':
    my_df = pd.DataFrame({'user':[1,1,1,2,2,2,3,3,3,4,4,4], 'item':[1,2,3,1,2,3,1,2,3,6,5,4], 'rating':[10,10,10,10,10,10,10,10,10,5,5,5]})
    my_item_df = pd.DataFrame({'item':[1,2,3,4]})
    my_Rec = Cosine(my_df, 'user', 'item', 'rating')
    my_Sys = Recommendation(my_df, my_item_df, 'user', 'item', 'rating', my_Rec)

    print(my_Sys.topk(4))