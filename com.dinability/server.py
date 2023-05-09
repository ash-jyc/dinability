import datetime
import Models
import Schemas
from Models import app, db
from utils import rating_aggregate, pop_aggregate
from Recommendation import Recommendation, Ranking
from RecommendationStrategy import Pearson, Jaccard, Cosine
from flask_restful import Resource, Api
from flask import jsonify, abort, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from sqlalchemy import exc, select
import pandas as pd
import numpy as np

api = Api(app)

loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = 'login'

socketio = SocketIO(app, cors_allowed_origins="*")
chat_id = 0
users_online = []
users_message = {}
users_addition = {} 
#store additional information about each user that needs to be sent to other users when a user logs in, sends a message, or leaves the chat.
chat_groups = {"Lobby": []}
number_of_users = 0

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
        
class Recommendation_Resource(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        method = data['method']
        param = data['param']

        users = Models.User.query.filter_by(username=username).first_or_404()
        userid = users.id
        restaurants = db.session.query(Models.Restaurant).all()

        restaurants_df = pd.DataFrame([(r.restaurant_name, r.picture_uri, r.description, r.rating_aspect_1,
                r.rating_aspect_2, r.rating_aspect_3, r.rating_aspect_4, r.rating_aspect_5) for r in restaurants],
                columns=['restaurant_name', 'picture_uri', 'description', 'rating_aspect_1', 'rating_aspect_2',
                'rating_aspect_3', 'rating_aspect_4', 'rating_aspect_5'])
        restaurants_df = restaurants_df.fillna(np.nan)
        restaurants_df = rating_aggregate(restaurants_df)
        reviews = db.session.query(Models.Review_on_Restaurant).all()
        reviews_df = pd.DataFrame([(r.user_id, r.restaurant_name, r.time, r.rating_aspect_1,
                r.rating_aspect_2, r.rating_aspect_3, r.rating_aspect_4, r.rating_aspect_5) for r in reviews],
                columns=['user_id', 'restaurant_name', 'time', 'rating_aspect_1', 'rating_aspect_2',
                'rating_aspect_3', 'rating_aspect_4', 'rating_aspect_5'])
        reviews_df = reviews_df.fillna(np.nan)
        reviews_df = rating_aggregate(reviews_df)
        restaurants_df = pop_aggregate(restaurants_df, reviews_df)

        if method == 'Ranking':
            rec_engine = Ranking(restaurants_df, param)
            result = rec_engine.topk()
        elif method == 'Similarity':
            if param == 'Cosine':
                rec_strategy = Cosine(reviews_df, 'user_id', 'restaurant_name', 'rating')
            elif param == 'Pearson':
                rec_strategy = Pearson(reviews_df, 'user_id', 'restaurant_name', 'rating')
            elif param == 'Jaccard':
                rec_strategy = Jaccard(reviews_df, 'user_id', 'restaurant_name', 'rating')
            else:
                raise Exception('Unexpected param!')
            rec_engine = Recommendation(reviews_df, restaurants_df, 'user_id', 'restaurant_name', 'rating', rec_strategy)
            result = rec_engine.topk(userid)
            
        result = result.to_json(orient="index")
        return result

api.add_resource(User_Resource, '/user')
api.add_resource(Recommendation_Resource, '/recommendation')

# when user logs in; send the total number of users in the server and the groups in the database
@socketio.on('connect')
def user_connect():
    print('connect')
    global number_of_users
    number_of_users+=1
    groups_query = Models.Group.query.all()
    groups = []
    for group in groups_query:
        groups.append({'group_id': group.group_id, 'group_name': group.group_name})
    send({'total_users': number_of_users, 'groups': groups}, broadcast=True)

# user logs out/ close the page/ refresh the page; update the current number of users
@socketio.on('disconnect')
def user_disconnect():
    print('disconnect')
    global number_of_users
    number_of_users-=1
    emit('disconnect',str(number_of_users), broadcast=True)

# user creates a group, save the group name in db; update the available groups
@socketio.on('create')
def create_group(group_name):
    print('create')
    group =  Models.Group.query.filter_by(group_name=group_name).first_or_404()
    db.session.add(group)
    db.session.commit()
    groups_query = Models.Group.query.all()
    groups = []
    for group in groups_query:
        groups.append({'group_id': group.group_id, 'group_name': group.group_name})
    send({'total_users': number_of_users, 'groups': groups}, broadcast=True)

# user joins a group; load and send all the messages based on the group id
@socketio.on('join_group')
def on_join(data):
    print('join_group')
    username = data['username']
    group_id = data['group_id']
    group = Models.Group.query.filter_by(group_id=group_id).first().group_name
    join_room(group_id)
    messages_query = Models.Message.query.filter_by(group_id=group_id).all()
    sender_id = Models.User.query.filter_by(username=username).first().id
    messages =[]
    for message in messages_query:
        messages.append({'sender': message.sender_id, 'message': message.content})
    emit('load_messages',{'group_name': group,'messages': messages})
    emit('joined',username + ' has joined the group.', room=group_id)
    now = datetime.datetime.now()
    message = Models.Message(content=f'{username} has entered the group',sender_id=sender_id,group_id=group_id,time=now)
    db.session.add(message)
    db.session.commit()

# user left the group; save the left message in db
@socketio.on('leave')
def on_leave(data):
    print('leave')
    username = data['username']
    group_id = data['group_id']
    now = datetime.datetime.now()
    sender_id = Models.User.query.filter_by(username=username).first().id
    message = Models.Message(content=f'{username} has left the group',sender_id=sender_id,group_id=group_id,time=now)
    db.session.add(message)
    db.session.commit()
    emit('leave',username + ' has left the group.', room=group_id)
    leave_room(group_id)


# user deletes the group; delete all group messages first before removing the group name in db
@socketio.on('delete')
def delete_group(data):
    print('delete')
    username = data['username']
    group_id = data['group_id']
    group = Models.Group.query.filter_by(group_id=group_id).first()
    emit('delete',username + ' has deleted this group.', room=group_id)
    Models.Message.query.filter_by(group_id=group_id).delete()
    db.session.commit()
    Models.Group.query.filter_by(group_id=group_id).delete()
    db.session.commit()
    groups_query = Models.Group.query.all()
    groups = []
    for group in groups_query:
        groups.append({'group_id': group.group_id, 'group_name': group.group_name})
    send({'total_users': number_of_users, 'groups': groups}, broadcast=True)

# all messages will be saved in db and will be broadcasted to all the users in the group
@socketio.on('chat')
def chat_message(data):
    print('chat')
    message = data['message_body']
    sender = data['sender']
    sender_id = Models.User.query.filter_by(username=sender).first().id
    group_id = data['group_id']
    now = datetime.datetime.now()
    message_object = Models.Message(content=message,sender_id=sender_id,group_id=group_id,time=now)
    db.session.add(message_object)
    db.session.commit()
    emit('chat',{'message':message, 'sender': sender, 'current_time':now}, room=group_id)


@app.route("/")
@login_required
def index():
    return render_template("index.html", name=current_user.username)

@app.route("/register", methods=['GET','POST'])
def register():
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
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = Models.User.query.filter_by(username=username).first_or_404()
        if user.email == email and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
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
    return render_template("find.html", username=current_user.username)

@app.route("/restaurant/<string:restaurant_name>")
@login_required
def restaurant(restaurant_name):
    restaurant = Models.Restaurant.query.filter_by(restaurant_name=restaurant_name).first_or_404()
    return render_template("restaurant.html", restaurant=restaurant)

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
    # app.run('127.0.0.1', 5000, debug=True)
    socketio.run(app, debug=True)
