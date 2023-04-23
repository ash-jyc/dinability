from Ranking import Ranking
from Recommendation import Recommendation_Pearson, Recommendation_Cosine, Recommendation_Jaccard

class RecommendationAdapter:
    def __init__(self):
        pass
    
    def recommend(self, restaurants, **kwargs):
        pass

class RecommendationAdapter_for_Ranking(RecommendationAdapter):
    def __init__(self):
        super().__init__()
        self._Ranking = Ranking()

    def recommend(self, restaurants, **kwargs):
        aspect = kwargs.get('aspect')
        if aspect is None:
            raise Exception('Parameter aspect is missing.')
        output = self._Ranking.rank(restaurants, aspect=aspect)
        return output

class RecommendationAdapter_for_Similarity(RecommendationAdapter):
    def __init__(self, method='Pearson'):
        super().__init__()
        if method == 'Pearson':
            self._Recommendation_System = Recommendation_Pearson()
        elif method == 'Jaccard':
            self._Recommendation_System = Recommendation_Jaccard()
        elif method == 'Cosine':
            self._Recommendation_System = Recommendation_Cosine()
        else:
            raise Exception('Wronf method is given.')

    def recommend(self, restaurants, **kwargs):
        history = kwargs.get('aspect')
        users = kwargs.get('users')
        user_id = kwargs.get('user_id')
        if history is None:
            raise Exception('Parameter history is missing.')
        if users is None:
            raise Exception('Parameter user is missing.')
        if user_id is None:
            raise Exception('Parameter user_id is missing.')
        self._Recommendation_System.calculate_matrices(restaurants, users, history)
        output =self._Recommendation_System.recommend(user_id)
        return output