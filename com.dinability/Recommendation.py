from RecommendationStrategy import Pearson, Jaccard, Cossine
import numpy as np

class Recommendation():
    def __init__(self):
        self._Recommendation_Strategy = None
        self._similarity_matrix = None
        self._rating_matrix = None
    
    def calculate_matrices(self, restaurants, users, history):
        pass

    def recommend(self, user_id):
        pass


class Recommendation_Pearson(Recommendation):
    def __init__(self):
        super().__init__()
        self._Recommendation_Strategy = Pearson
        self._similarity_matrix = None
        self._rating_matrix = None

    def calculate_matrices(self, restaurants, users, history):
        self._similarity_matrix = self._Recommendation_Strategy.update_similarity_matrix(restaurants, users, history)
        self._rating_matrix = self._Recommendation_Strategy.update_rating_matrix(restaurants, users, history)

    def recommend(self, user_id):
        pass
        

class Recommendation_Cosine(Recommendation):
    def __init__(self):
        super().__init__()
        self._Recommendation_Strategy = Cossine

    def calculate_matrices(self, restaurants, users, history):
        self._similarity_matrix = self._Recommendation_Strategy.update_similarity_matrix(restaurants, users, history)
        self._rating_matrix = self._Recommendation_Strategy.update_rating_matrix(restaurants, users, history)

    def recommend(self, user_id):
        pass

class Recommendation_Jaccard(Recommendation):
    def __init__(self):
        super().__init__()
        self._Recommendation_Strategy = Jaccard

    def calculate_matrices(self, restaurants, users, history):
        self._similarity_matrix = self._Recommendation_Strategy.update_similarity_matrix(restaurants, users, history)
        self._rating_matrix = self._Recommendation_Strategy.update_rating_matrix(restaurants, users, history)

    def recommend(self, user_id):
        pass