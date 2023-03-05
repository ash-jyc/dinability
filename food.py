from review import *

class Food:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description
    
    def get_name(self):
        return self.name
    
    def get_price(self):
        return self.price
    
    def modify_price(self,new_price):
        self.price = new_price
        return self.price
    
    def relevant_reviews(self):
        return review.reviews
    
    def set_description(self, description):
        self.description = description
    
    def get_description(self):
        return self.description
        
    
    