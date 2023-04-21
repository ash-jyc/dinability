import Models
import Schemas
from Models import app, db
from flask_restful import Resource, Api
from flask import jsonify, abort, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import exc

api = Api(app)

loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = 'login'

@loginmanager.user_loader
def load_user(user_id):
    return Models.User.query.get(int(user_id))


class User_Resource(Resource):
    def get(self):
        args = request.args
        schema = Schemas.User_Schema(only={'username'})
        errors = schema.validate(args)
        if errors:
            abort(400, str(errors))
        result = Models.User.query.filter_by(username=args['username']).first_or_404()
        schema = Schemas.User_Schema(only={'id','username','email','rating'})
        result = schema.dump(result)
        return jsonify(result)

    def post(self):
        args = request.args
        schema = Schemas.User_Schema(only={'username','password','email'})
        errors = schema.validate(args)
        if errors:
            abort(400, str(errors))
        user = Models.User(username=args['username'], password=args['password'], email=args['email'])
        db.session.add(user)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            abort(400, 'Operation Failed!')
        return jsonify({'message':'OK'})

    def put(self):
        args = request.args
        schema = Schemas.User_Schema(only={'username','password','email','rating'})
        errors = schema.validate(args)
        if errors:
            abort(400, str(errors))
        result = Models.User.query.filter_by(username=args['username']).first_or_404()
        result.password = args['password']
        result.email = args['email']
        result.rating = args['rating']
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            abort(400, 'Operation Failed!')
        return jsonify({'message':'OK'})
        
    def delete(self):
        args = request.args
        schema = Schemas.User_Schema(only={'username'})
        errors = schema.validate(args)
        if errors:
            abort(400, str(errors))
        result = Models.User.query.filter_by(username=args['username']).first_or_404()
        db.session.delete(result)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            abort(400, 'Operation Failed!')
        return jsonify({'message':'OK'})
        
# class Recommendation_Resource(Resource):
#     def get(self):
#         args = request.args
#         schema = Schemas.User_Schema(only={'username'})
#         errors = schema.validate(args)
#         if errors:
#             abort(400, str(errors))
#         result = Models.User.query.filter_by(username=args['username']).first_or_404()
#         schema = Schemas.User_Schema(only={'id','username','email','rating'})
#         result = schema.dump(result)
#         return jsonify(result)


api.add_resource(User_Resource, '/user')

@app.route("/")
@login_required
def index():
    return render_template("index.html", name=current_user.username)

@app.route("/register", methods=['GET','POST'])
def register():
    print(request.method)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = Models.User(username=username, password=password, email=email)
        db.session.add(user)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            flash ('User or email already exists! Try again!')
        else:
            return redirect(url_for('profile'))
    return render_template("register.html")

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print(request.args.get('next'))
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = Models.User.query.filter_by(username=username).first_or_404()
        if user.email == email and user.password == password:
            login_user(user)
            return redirect(request.args.get('next') or url_for('profile'))
        else:
            flash('Wrong email or password! Try again!')
    return render_template("login.html")

@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/groups")
@login_required
def groups():
    return render_template("groups.html")

@app.route("/rate")
@login_required
def rate():
    return render_template("rate.html")

@app.route("/find")
@login_required
def find():
    return render_template("find.html")

# @app.route("/register", methods=["POST"])
# def register():
#     form = request.form.to_dict()
#     if form.get("username") is not None:
#         new_user = User(username=form["username"], password=form["password"], email=form["email"])
#         db.session.add(new_user)
#         db.session.commit()
#         session["username"] = form["username"]
#         return "Success"
#     else:
#         user = User.query.filter_by(email=form["email"]).first()
#         if user is None:
#             return "0"
#         elif user.password != form["password"]:
#             return "00"
#         session["username"] = user.username
#         return "1"
    

# # login endpoint
# @app.route('/login', methods=['GET'])
# def login():
#     data_in = request.form.to_dict()  # {'name': 'xxx'}
#     user = data_in["name"]
#     users_online.append(user)
#     chat_groups["Lobby"].append(user)
#     users_message[user] = []
#     users_addition[user] = {}
#     data_out = {"name": user, "online": [user]}
#     for other in users_online:
#         if other != user:
#             data_out["online"].append(other)
#             users_addition[other]["arrive"] = users_addition[other].get("arrive", [])
#             users_addition[other]["arrive"].append(user)
#     return json.dumps(data_out)


# @app.route("/user/update")
# def update_user():
#     username = input("Username: ")
#     password = input("Password: ")
#     user = User.query.filter_by(username).first()
#     user.password = password
#     #synchronization in database
#     db.session.commit()
#     return "Updated"



# @app.route("/user/query")
# # to be modified
# def query_user():
#     users = User.query.filter_by(username = 'blabla')
#     for user in users:
#         print(user.username)
#     return "found"

# @app.route("/user/del")
# def delete_user():
#     user = User.query.get(1)
#     db.session.delete(user)
#     #synchronization in database
#     db.session.commit()



# @app.route("/user/query")
# # to be modified
# def query_user():
#     users = User.query.filter_by(username = 'blabla')
#     for user in users:
#         print(user.username)
#     return "found"

# # A sample dictionary to store the restaurant data
# """restaurants = {
#     1: {"name": "Le Big Mac", "rating": 4.5},
#     2: {"name": "Lafayette", "rating": 4.2},
#     3: {"name": "KFC", "rating": 4.7},
#     4: {"name": "Sushi", "rating": 3.9},
#     5: {"name": "Steak", "rating": 4.8},
# }
# """

# # Route to get a list of recommended restaurants
# @app.route('/recommend', methods=['GET'])
# def recommend_restaurant():
#     # Retrieve the rating parameter from the request
#     rating = request.args.get('rating')
    
#     # Convert the rating parameter to a float
#     rating = float(rating)
    
#     # Find all restaurants with a rating greater than the provided rating
#     recommended_restaurants = [restaurant for restaurant in restaurants.values() if restaurant['rating'] >= rating]
#     if recommended_restaurants != []:
#         # Return the recommended restaurants as JSON
#         return jsonify(recommended_restaurants)
#     else:
#         return('No restaurant that meets the criteria')
#     if recommended_restaurants != []:
#         # Return the recommended restaurants as JSON
#         return jsonify(recommended_restaurants)
#     else:
#         return('No restaurant that meets the criteria')


    
# @app.route('/recommend/choose-restaurant', methods=['GET'])
# def choose_retaurant(restaurant_name):
#     for restaurant in restaurant:
#         if restaurant_name == restaurant:
#             return jsonify(restaurant)
#             break
#     return("The restaurant is not included")
            
# def choose_retaurant(restaurant_name):
#     for restaurant in restaurant:
#         if restaurant_name == restaurant:
#             return jsonify(restaurant)
#             break
#     return("The restaurant is not included")
            

# #Endpoint to retrieve all restaurants
# @app.route('/restaurants', methods=['GET'])
# def get_restaurants():
#     # Get search query from request parameter
#     query = request.args.get('q')
    
#     # Filter restaurants based on search query
#     filtered_restaurants = [r for r in restaurants if (query.lower() in r['name'].lower() or query.lower() in r['cuisine'].lower())]
    
#     # Sort restaurants based on request parameters
#     sort_by = request.args.get('sort_by', 'rating')
#     sort_order = request.args.get('sort_order', 'desc')
#     reverse = True if sort_order == 'desc' else False
#     sorted_restaurants = sorted(filtered_restaurants, key=lambda r: r[sort_by], reverse=reverse)
    
#     # Return response as JSON
#     return jsonify(sorted_restaurants)

# # Endpoint to retrieve a single restaurant by ID
# @app.route('/restaurants/<int:id>', methods=['GET'])
# def get_restaurant(id):
#     for restaurant in restaurant.keys():
#         if id == restaurant:
#             return jsonify(restaurant)
#             break
#     return jsonify({"message": "Restaurant not found"}), 404

# # Endpoint to create a new restaurant
# @app.route('/restaurants', methods=['POST'])
# def create_restaurant(name,address,cuisine,rating,reviews):
#     # Get data from request body
#     data = request.get_json()
#     name = data.get(str(name))
#     address = data.get(str(address))
#     cuisine = data.get(str(cuisine))
#     rating = data.get(str(rating), 0)
#     reviews = data.get(str(reviews), 0)
    
#     # Generate new ID
#     new_id = max(r['id'] for r in restaurants) + 1
    
#     # Create new restaurant object
#     new_restaurant = {
#         "id": new_id,
#         "name": name,
#         "address": address,
#         "cuisine": cuisine,
#         "rating": rating,
#         "reviews": reviews
#     }
    
#     # Add new restaurant to list
#     restaurants.append(new_restaurant)
    
#     # Return response as JSON
#     return jsonify(new_restaurant), 201





    
if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
