from app import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now())
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', back_populates='reviews')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='reviews')
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Review %r>' % self.movie
