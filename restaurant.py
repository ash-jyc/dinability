import menu
import review
class restaurant:
    def __init__(self,name:str,location:str,distance:int,env:float,taste:float, varieties:float,menu:menu,reviews:list):
        self.name = name 
        self.location = location
        self.env = env
        self.taste = taste
        self.taste = varieties
        self.menu = menu
        self.review = review
        self.distance = distance
        #three attributes to be included in rating: env,varities,taste
    def get_name(self):
        return self.name
    def get_menu(self):
        return self.menu
    def change_rating(self,important1:str,important2:str, important3:str):#change rating catering to users' need
        rate = 0
        # total rate maximum would be 5
        l = ["env","taste","varieties"]
        if all([important1 in l,important2 in l,important2 in l]) == False:
            raise ValueError("Item(s) not attributes of restaurant")
        if important1 == "env":
            rate += self.env * 0.2
        if important1 == "taste":
            rate += self.taste * 0.2
        if important1 == "varieties":
            rate += self.varieties * 0.2

        if important2 == "env":
            rate += self.env * 0.2
        if important2 == "taste":
            rate += self.taste * 0.2
        if important2 == "varieties":
            rate += self.varieties * 0.2

        if important3 == "env":
            rate += self.env * 0.1
        if important3 == "taste":
            rate += self.taste * 0.1
        if important3 == "varieties":
            rate += self.varieties * 0.1
        
        return round(rate,1) #rate reserves one decimal rating

    def add_review(self,review:review):
        self.reviews.append(review)

    def get_reviews(self):
        return self.reviews

    
    
        

