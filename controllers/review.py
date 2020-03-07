from app import db
from models import User, Movie, Review
import json


def add_review(username, movie_name, rating, content):
    user = User.query.filter_by(username=username).first()
    movie = Movie.query.filter_by(movie_name=movie_name).first()
    if user is None or movie is None:
        return
    
    review = Review(user=user, movie=movie, rating=rating, content=content)
    db.session.add(review)
    db.session.commit()


def get_movie_reviews(movie_name, count):
    movie = Movie.query.filter_by(movie_name=movie_name).first()
    if movie is None:
        return
    
    reviews = Review.query.\
              filter_by(movie=movie).\
              sort_by(Review.timestamp.desc()).\
              limit(count).all()
    return json.dumps({
        'reviews': [{
            'username': review.user.username,
            'rating': review.rating,
            'content': review.content
        } for review in reviews]
    })
    