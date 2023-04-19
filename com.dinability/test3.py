import Models
import Schemas
from Models import app, db
from flask_restful import Resource, Api, marshal_with
from flask import jsonify, abort, request, render_template
from sqlalchemy import or_, exc

api = Api(app)


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
        

api.add_resource(User_Resource, '/user')

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/")
# def index():
#     return render_template("index.html")
    
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/")
# def index():
#     return render_template("index.html")


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)