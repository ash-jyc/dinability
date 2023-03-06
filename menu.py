import food
#import food class from food.py
class menu:
    def __init__(self,restaurant,food_list = []):
        self.owner = restaurant
        self.food_list = food_list
        #a list of food class
    def show_foods(self):
        return self.food_list
        #display all food

    def add_food(self,food:food):
        self.food_list.append(food)
        
    def delete_food(self,food):
        self.food_list.remove(food)


