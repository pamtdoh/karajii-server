from app import db

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(50), nullable=False, unique=True)
    title = db.Column(db.String(50), nullable=False)
    cover_image = db.Column(db.String(255))
    genres = db.relationship('MovieGenre', back_populates='movie')
    summary = db.Column(db.Text)
    duration = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Review', back_populates='movie')

    def add_genre(self, genre):
        genre = MovieGenre(genre=genre, movie=self)
        db.session.add(genre)

    def __repr__(self):
        return '<Movie %r>' % self.title


class MovieGenre(db.Model):
    __tablename__ = 'movie_genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(20), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', back_populates='genres')
