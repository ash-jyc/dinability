from flask import Flask, request, jsonify, render_template, session,json
import pysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

app = Flask(__name__)
app.secret_key = 'my_secret_key'
#config for flask, database info
#Xiaocheng Yang

chat_id = 0
users_online = []
users_message = {}
users_addition = {}
chat_groups = {"Lobby": []}

host_name = "127.0.0.1"
port = 3306
username = "Stephen"
password = "pass"
database = "tables"
# replace engine
app.config['SQLAlCHEMY_DATABASE_URI'] = f"mysql + pysql://{username}:{password}@{host_name}:{port}/{database}?charset = utf8mb4"

db = SQLAlchemy(app)
#To be extracted from database, test if the database is connected successfully
with app.app_context():#上下文
    with db.engine.connect() as conn:
        rs = conn.execute("select 1")
        print(rs.fetchone())

# might not be used later on

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
    rating = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.username
    
class group_member(User):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    group_id = db.Column(db.Integer, unique=True, primary_key=True)

    def __repr__(self):
        return '<group member %r>' % self.username
    
class group_owner(User):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    group_id = group_id = db.Column(db.Integer, unique=True, primary_key=True)
    def __repr__(self):
        return '<group owner %r>' % self.username
    
class group(db.Model):
    group_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, nullable=False) #use the owner object?
    payment_method = db.Column(db.String(50), nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    restaurant_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<group%r>' % str(self.group_id)

class restaurant(db.Model):
    name = db.Column(db.String(50), nullable=False, primary_key=True)
    picture = db.Column(db.String(50), nullable=False)
    desciption = db.Column(db.String(50), nullable=False)
    Rating_Aspect_1 = db.Column(db.Integer)
    Rating_Aspect_2 = db.Column(db.Integer)
    Rating_Aspect_3 = db.Column(db.Integer)
    Rating_Aspect_4 = db.Column(db.Integer)
    Rating_Aspect_5 = db.Column(db.Integer)
    menu = db.Column(db.String(50))
    location = db.Column(db.String(50))

    def __repr__(self):
        return '<restaurant %r>' % self.name
   ####
   # whether to stay or not 
class menu(db.Model):
    menu = db.Column(db.String(50), unique=False, nullable=False) # to be modified datatype of menu
    restaurant_name = db.Column(db.String(50), unique=False, nullable=False)
    
    def __repr__(self):
        return '<menu %r>' % self.restaurant_name
    
########
######
    
class food(db.Model):
    restaurant_name = db.Columns(db.String(50), nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False, primary_key=True)
    picture = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer)
    Rating_Aspect_1 = db.Column(db.Integer)
    Rating_Aspect_2 = db.Column(db.Integer)
    Rating_Aspect_3 = db.Column(db.Integer)
    Rating_Aspect_4 = db.Column(db.Integer)
    Rating_Aspect_5 = db.Column(db.Integer)

    def __repr__(self):
        return '<food %r>' % self.name

class review_on_restaurant(db.Model):
    user_id = db.Column(db.Integer(10), nullable=False, primary_key=True)
    Time = db.Column(db.Integer(10), nullable=False, primary_key=True)
    restaurant_name = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(150))
    # menu = db.Column(db.String(50), unique=False, nullable=False) # to be modified 
    Rating_Aspect_1 = db.Column(db.Integer)
    Rating_Aspect_2 = db.Column(db.Integer)
    Rating_Aspect_3 = db.Column(db.Integer)
    Rating_Aspect_4 = db.Column(db.Integer)
    Rating_Aspect_5 = db.Column(db.Integer)
    
    def __repr__(self):
        return '<review_on_restaurant %r>' % self.retaurant_name

@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html", name=session["username"])
    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    form = request.form.to_dict()
    if form.get("username") is not None:
        new_user = User(username=form["username"], password=form["password"], email=form["email"])
        db.session.add(new_user)
        db.session.commit()
        session["username"] = form["username"]
        return "Success"
    else:
        user = User.query.filter_by(email=form["email"]).first()
        if user is None:
            return "0"
        elif user.password != form["password"]:
            return "00"
        session["username"] = user.username
        return "1"
    

# login endpoint
@app.route('/login', methods=['GET'])
def login():
    data_in = request.form.to_dict()  # {'name': 'xxx'}
    user = data_in["name"]
    users_online.append(user)
    chat_groups["Lobby"].append(user)
    users_message[user] = []
    users_addition[user] = {}
    data_out = {"name": user, "online": [user]}
    for other in users_online:
        if other != user:
            data_out["online"].append(other)
            users_addition[other]["arrive"] = users_addition[other].get("arrive", [])
            users_addition[other]["arrive"].append(user)
    return json.dumps(data_out)


@app.route("/user/update")
def update_user():
    username = input("Username: ")
    password = input("Password: ")
    user = User.query.filter_by(username).first()
    user.password = password
    #synchronization in database
    db.session.commit()
    return "Updated"



@app.route("/user/query")
# to be modified
def query_user():
    users = User.query.filter_by(username = 'blabla')
    for user in users:
        print(user.username)
    return "found"

@app.route("/user/del")
def delete_user():
    user = User.query.get(1)
    db.session.delete(user)
    #synchronization in database
    db.session.commit()



@app.route("/user/query")
# to be modified
def query_user():
    users = User.query.filter_by(username = 'blabla')
    for user in users:
        print(user.username)
    return "found"

# A sample dictionary to store the restaurant data
"""restaurants = {
    1: {"name": "Le Big Mac", "rating": 4.5},
    2: {"name": "Lafayette", "rating": 4.2},
    3: {"name": "KFC", "rating": 4.7},
    4: {"name": "Sushi", "rating": 3.9},
    5: {"name": "Steak", "rating": 4.8},
}
"""

# Route to get a list of recommended restaurants
@app.route('/recommend', methods=['GET'])
def recommend_restaurant():
    # Retrieve the rating parameter from the request
    rating = request.args.get('rating')
    
    # Convert the rating parameter to a float
    rating = float(rating)
    
    # Find all restaurants with a rating greater than the provided rating
    recommended_restaurants = [restaurant for restaurant in restaurants.values() if restaurant['rating'] >= rating]
    if recommended_restaurants != []:
        # Return the recommended restaurants as JSON
        return jsonify(recommended_restaurants)
    else:
        return('No restaurant that meets the criteria')
    if recommended_restaurants != []:
        # Return the recommended restaurants as JSON
        return jsonify(recommended_restaurants)
    else:
        return('No restaurant that meets the criteria')


    
@app.route('/recommend/choose-restaurant', methods=['GET'])
def choose_retaurant(restaurant_name):
    for restaurant in restaurant:
        if restaurant_name == restaurant:
            return jsonify(restaurant)
            break
    return("The restaurant is not included")
            
def choose_retaurant(restaurant_name):
    for restaurant in restaurant:
        if restaurant_name == restaurant:
            return jsonify(restaurant)
            break
    return("The restaurant is not included")
            

#Endpoint to retrieve all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    # Get search query from request parameter
    query = request.args.get('q')
    
    # Filter restaurants based on search query
    filtered_restaurants = [r for r in restaurants if (query.lower() in r['name'].lower() or query.lower() in r['cuisine'].lower())]
    
    # Sort restaurants based on request parameters
    sort_by = request.args.get('sort_by', 'rating')
    sort_order = request.args.get('sort_order', 'desc')
    reverse = True if sort_order == 'desc' else False
    sorted_restaurants = sorted(filtered_restaurants, key=lambda r: r[sort_by], reverse=reverse)
    
    # Return response as JSON
    return jsonify(sorted_restaurants)

# Endpoint to retrieve a single restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    for restaurant in restaurant.keys():
        if id == restaurant:
            return jsonify(restaurant)
            break
    return jsonify({"message": "Restaurant not found"}), 404

# Endpoint to create a new restaurant
@app.route('/restaurants', methods=['POST'])
def create_restaurant(name,address,cuisine,rating,reviews):
    # Get data from request body
    data = request.get_json()
    name = data.get(str(name))
    address = data.get(str(address))
    cuisine = data.get(str(cuisine))
    rating = data.get(str(rating), 0)
    reviews = data.get(str(reviews), 0)
    
    # Generate new ID
    new_id = max(r['id'] for r in restaurants) + 1
    
    # Create new restaurant object
    new_restaurant = {
        "id": new_id,
        "name": name,
        "address": address,
        "cuisine": cuisine,
        "rating": rating,
        "reviews": reviews
    }
    
    # Add new restaurant to list
    restaurants.append(new_restaurant)
    
    # Return response as JSON
    return jsonify(new_restaurant), 201





    


if __name__ == '__main__':
    app.run(debug=True)
