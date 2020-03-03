from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import os
from werkzeug.security import check_password_hash


load_dotenv()

# Main app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
CORS(app)

# Set up db
db = SQLAlchemy(app)
import models
db.create_all()

# Set up JWT
def authenthicate(username, password):
    user = models.User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return models.User.query.filter_by(id=user_id).first()

jwt = JWT(app, authenthicate, identity)


# Set up resource endpoints
api = Api(app)
import resources
api.add_resource(resources.Register, '/register')
api.add_resource(resources.User, '/user')

@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)