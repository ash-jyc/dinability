from marshmallow import Schema, fields

class User_Schema(Schema):
    id = fields.Integer(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)
    rating = fields.Integer(required=True)
