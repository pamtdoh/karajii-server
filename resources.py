from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from app import db
import models

class User(Resource):
    @jwt_required()
    def get(self):        
        return {'username': current_identity.username}


newuser_parser = reqparse.RequestParser()
newuser_parser.add_argument('username')
newuser_parser.add_argument('password')

class Register(Resource):
    def post(self):
        args = newuser_parser.parse_args()
        
        if models.User.username_exists(args['username']):
            return {'message': 'Username taken'}, 400
        
        user = models.User(username=args['username'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {}
