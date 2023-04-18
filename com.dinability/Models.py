from flask import Flask
from flask_sqlalchemy import SQLAlchemy

username = "root"
password = ""
hostname = "127.0.0.1"
database = "dining"

conn = f'mysql+pymysql://{username}:{password}@{hostname}/{database}'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    restaurant_name = db.Column(db.String(50), nullable=False, primary_key=True)
    picture_uri = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(50), nullable=False)
    rating_aspect_1 = db.Column(db.Integer)
    rating_aspect_2 = db.Column(db.Integer)
    rating_aspect_3 = db.Column(db.Integer)
    rating_aspect_4 = db.Column(db.Integer)
    rating_aspect_5 = db.Column(db.Integer)
    def __repr__(self):
        return '<Restaurant %r>' % str(self.restaurant_name)

class Food(db.Model):
    __tablename__ = 'food'
    restaurant_name = db.Column(db.String(50), db.ForeignKey('restaurant.restaurant_name'), nullable=False, primary_key=True)
    food_name = db.Column(db.String(50), nullable=False, primary_key=True)
    pricture_uri = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer)
    rating_aspect_1 = db.Column(db.Integer)
    rating_aspect_2 = db.Column(db.Integer)
    rating_aspect_3 = db.Column(db.Integer)
    rating_aspect_4 = db.Column(db.Integer)
    rating_aspect_5 = db.Column(db.Integer)
    def __repr__(self):
        return '<Food %r %r>' % (str(self.restaurant_name), str(self.food_name))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    rating = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>' % str(self.id)

class Group(db.Model):
    __tablename__ = 'group'
    group_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    restaurant_name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Group %r>' % str(self.group_id)

class Group_Buy_Food(db.Model):
    __tablename__ = 'group_buy_food'
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'), nullable=False, primary_key=True)
    restaurant_name = db.Column(db.String(50), nullable=False, primary_key=True)
    food_name = db.Column(db.String(50), nullable=False, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['restaurant_name', 'food_name'],
            ['food.restaurant_name', 'food.food_name']
        ),
    )
    def __repr__(self):
        return '<Group_Buy_Food %r %r %r>' % (str(self.group_id), str(self.restaurant_name), str(self.food_name))

class User_Participate_in_Group(db.Model):
    __tablename__ = 'user_participate_in_group'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'), nullable=False, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return '<User_Participate_in_Group %r %r>' % (str(self.user_id), str(self.group_id))

class User_Rate_User(db.Model):
    __tablename__ = 'user_rate_user'
    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    ratee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(50))
    def __repr__(self):
        return '<User_Rate_User %r %r %r>' % (str(self.rater_id), str(self.ratee_id), str(self.time))

class Review_on_Restaurant(db.Model):
    __tablename__ = 'review_on_restaurant'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, primary_key=True)
    restaurant_name = db.Column(db.String(50), db.ForeignKey('restaurant.restaurant_name'), nullable=False)
    comment = db.Column(db.String(59))
    rating_aspect_1 = db.Column(db.Integer)
    rating_aspect_2 = db.Column(db.Integer)
    rating_aspect_3 = db.Column(db.Integer)
    rating_aspect_4 = db.Column(db.Integer)
    rating_aspect_5 = db.Column(db.Integer)
    def __repr__(self):
        return '<Review_on_Restaurant %r %r>' % (str(self.user_id), str(self.time))

class Review_on_Food(db.Model):
    __tablename__ = 'review_on_food'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, primary_key=True)
    restaurant_name = db.Column(db.String(50), nullable=False)
    food_name = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(59))
    rating_aspect_1 = db.Column(db.Integer)
    rating_aspect_2 = db.Column(db.Integer)
    rating_aspect_3 = db.Column(db.Integer)
    rating_aspect_4 = db.Column(db.Integer)
    rating_aspect_5 = db.Column(db.Integer)
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['restaurant_name', 'food_name'],
            ['food.restaurant_name', 'food.food_name']
        ),
    )
    def __repr__(self):
        return '<Review_on_Restaurant %r %r>' % (str(self.user_id), str(self.time))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()