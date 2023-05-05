import pandas as pd
import numpy as np

class RecommendationStrategy():
    def __init__(self, rating_data, user_col, item_col, rating_col):
        self.rating_data = rating_data
        self.user_col = user_col
        self.item_col = item_col
        self.rating_col = rating_col

    def similarity(self, item1, item2):
        pass

class Pearson(RecommendationStrategy):
    def __init__(self, rating_data, user_col, item_col, rating_col):
        super(Pearson, self).__init__(rating_data, user_col, item_col, rating_col)

    def similarity(self, item1, item2):
        R_item1 = self.rating_data[self.rating_data[self.item_col] == item1][[self.user_col, self.rating_col]]
        R_item2 = self.rating_data[self.rating_data[self.item_col] == item2][[self.user_col, self.rating_col]]
        R_intersect = pd.merge(R_item1, R_item2, on=[self.user_col], suffixes=('_item1', '_item2'))
        if R_intersect.empty:
            return 0.0
        print(R_intersect)
        R_item1, R_item2 = np.array(R_intersect[self.rating_col+'_item1']), np.array(R_intersect[self.rating_col+'_item2'])
        similarity_score = np.dot((R_item1 - np.mean(R_item1)), (R_item2 - np.mean(R_item2)))/\
                           (np.linalg.norm(R_item1 - np.mean(R_item1))*np.linalg.norm(R_item2 - np.mean(R_item2))+1e-8)
        return similarity_score

class Jaccard(RecommendationStrategy):
    def __init__(self, rating_data, user_col, item_col, rating_col):
        super(Jaccard, self).__init__(rating_data, user_col, item_col, rating_col)

    def similarity(self, item1, item2):
        U_item1 = self.rating_data[self.rating_data[self.item_col] == item1][self.user_col]
        U_item2 = self.rating_data[self.rating_data[self.item_col] == item2][self.user_col]
        union, intersect = np.union1d(U_item1, U_item2), np.intersect1d(U_item1, U_item2, assume_unique=True)
        similarity_score = len(intersect)/(len(union)+1e-8)
        return similarity_score

class Cosine(RecommendationStrategy):
    def __init__(self, rating_data, user_col, item_col, rating_col):
        super(Cosine, self).__init__(rating_data, user_col, item_col, rating_col)

    def similarity(self, item1, item2):
        R_item1 = self.rating_data[self.rating_data[self.item_col] == item1][[self.user_col, self.rating_col]]
        R_item2 = self.rating_data[self.rating_data[self.item_col] == item2][[self.user_col, self.rating_col]]
        R_intersect = pd.merge(R_item1, R_item2, on=[self.user_col], suffixes=('_item1', '_item2'))
        if R_intersect.empty:
            return 0.0
        R_item1, R_item2 = np.array(R_intersect[self.rating_col+'_item1']), np.array(R_intersect[self.rating_col+'_item2'])
        similarity_score = np.dot(R_item1, R_item2)/(np.linalg.norm(R_item1)*np.linalg.norm(R_item2)+1e-8)
        return similarity_score

if __name__ == '__main__':
    my_df = pd.DataFrame({'user':[1,1,1,2,2,2,3,3,3], 'item':[1,2,3,1,2,3,1,2,3], 'rating':[10,10,10,10,10,10,10,10,10]})
    my_Rec = Cosine(my_df, 'user', 'item', 'rating')
    print(my_Rec.similarity(1,2))