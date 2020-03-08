from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from flask import request
from app import db, api
from controllers.user import get_user_details, create_user
from controllers.rent import get_user_history, get_user_orders, create_order


newuser_parser = reqparse.RequestParser()
newuser_parser.add_argument('username', required=True)
newuser_parser.add_argument('password', required=True)
newuser_parser.add_argument('email', required=True)
newuser_parser.add_argument('address', required=True)

count_parser = reqparse.RequestParser()
count_parser.add_argument('count', type=int)

class User(Resource):
    @jwt_required()
    def get(self, username):
        if current_identity.username != username:
            return {'message': 'Invalid user.'}, 400
        
        return get_user_details(username)

    def post(self, username):
        args = newuser_parser.parse_args()
        result = create_user(
            args['username'],
            args['password'],
            args['email'],
            args['address']
        )

        if result is None:
            return {'message': 'Invalid request.'}, 400
        
        return {'message': 'OK'}


class UserHistory(Resource):
    @jwt_required()
    def get(self, username):
        if current_identity.username != username:
            return {'message': 'Invalid user.'}, 400
        
        args = count_parser.parse_args()
        return get_user_history(username, args['count'])


class UserOrders(Resource):
    @jwt_required()
    def get(self, username):
        if current_identity.username != username:
            return {'message': 'Invalid user.'}, 400
        
        args = count_parser.parse_args()
        return get_user_orders(username)


class UserOrder(Resource):
    @jwt_required()
    def post(self, username):
        if current_identity.username != username:
            return {'message': 'Invalid user.'}, 400
        
        data = request.json
        res = create_order(
            username,
            data['order_details'],
            data['payment_info'],
            data['delivery_address'])
        if res is None:
            return {'message': 'Error'}, 400
        
        return {'message': 'OK'}


api.add_resource(User, '/user/<string:username>')
api.add_resource(UserHistory, '/user/<string:username>/history')
api.add_resource(UserOrders, '/user/<string:username>/orders')
api.add_resource(UserOrder, '/user/<string:username>/order')