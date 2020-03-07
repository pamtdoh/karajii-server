from app import db
from models.user import User
import json
from flask import jsonify


def username_used(username):
    return User.query.filter_by(username=username).first() is not None


def email_used(email):
    return User.query.filter_by(email=email).first() is not None


def create_user(username, password, email, address):
    if username_used(username) or email_used(email):
        return
    
    user = User(
        username=username,
        email=email,
        address=address)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    return True


def get_user_details(username):
    user = User.query.filter_by(username=username).first()
    return jsonify({
        'username': user.username,
        'email': user.email,
        'address': user.address
    })


def update_user_details(username=None, password=None, email=None, address=None):
    pass


def get_all_users(count):
    users = User.query.limit(count).all()
    return jsonify({
        'users': [user.username for user in users]
    })
