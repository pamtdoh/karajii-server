from app import db
from models.movie import Movie, MovieGenre
from flask import jsonify


def add_movie(payload):
    genres = payload.pop('genres', None)
    movie = Movie(**payload)
    if genres:
        for genre in genres:
            movie.add_genre(genre)
    
    db.session.add(movie)
    db.session.commit()
    return True


def delete_movie(movie_name):
    n = Movie.query.filter_by(movie_name=movie_name).delete()
    db.session.commit()
    return n


def get_movie_list(count=20, genre=None):
    if genre is None:
        res = Movie.query.limit(count).all()
    else:
        res = MovieGenre.query.filter_by(genre=genre).limit(count).all()
        res = [genre.movie for genre in res]
    
    return jsonify({
        'movies': [movie.movie_name for movie in res]
    })


def get_movie_details(movie_name):
    res = Movie.query.filter_by(movie_name=movie_name).first()
    if res is None:
        return
    
    return jsonify({
        'movie_name': res.movie_name,
        'title': res.title,
        'cover_image': res.cover_image,
        'genre': [genre.genre for genre in res.genres],
        'summary': res.summary,
        'duration': res.duration,
        'price': res.price,
        'stock': res.stock,
        'year': res.year
    })

