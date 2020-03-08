from app import db
from models import Movie, MovieGenre
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


def get_movie_list(catalogue=False, count=None, genre=None, year=None):
    query = Movie.query
    if year is not None:
        query = query.filter_by(year=year)
    if genre is not None:
        query = query.filter(Movie.genres.any(MovieGenre.genre == genre))
    if count is not None:
        query = query.limit(count)
    res = query.all()
    
    if catalogue:
        return jsonify({
            'movies': [{
                'movie_name': movie.movie_name,
                'title': movie.title,
                'cover_image': movie.cover_image
            } for movie in res]
        })
    else:
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
        'genres': [genre.genre for genre in res.genres],
        'summary': res.summary,
        'duration': res.duration,
        'price': res.price,
        'stock': res.stock,
        'year': res.year
    })

