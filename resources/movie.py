from flask_restful import Resource, reqparse
from flask import request
from app import api
from controllers.movie import *


filter_parser = reqparse.RequestParser()
filter_parser.add_argument('genre')
filter_parser.add_argument('count')

class MovieList(Resource):
    def get(self):
        args = filter_parser.parse_args()
        movies = get_movie_list(**args)
        return movies


class Movie(Resource):
    def get(self, movie_name):
        movie = get_movie_details(movie_name)
        if movie is None:
            return {'message': 'Not found'}, 400
        
        return movie
    
    def post(self, movie_name):
        res = add_movie(request.json)
        if res is None:
            return {'message': 'Error adding movie'}, 400
        return {'message': 'OK'}


api.add_resource(MovieList, '/movies')
api.add_resource(Movie, '/movie/<string:movie_name>')
