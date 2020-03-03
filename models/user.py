from app import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def username_exists(username):
        return User.query.filter_by(username=username).first() is not None
