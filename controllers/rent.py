from app import db
from models import User, RentOrder, RentItem, Movie
from flask import jsonify
from datetime import datetime

def get_user_orders(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return
    
    rent_orders = RentOrder.query.filter_by(user=user).all()    
    return jsonify({
        'orders': [{
            'order_id': rent_order.id,
            'order_timestamp': rent_order.timestamp.isoformat(),
            'total_price': rent_order.total_price,
            'delivery_address': rent_order.delivery_address,
            'payment_info': rent_order.payment_info,
            'rent_items': [rent_item.movie.movie_name for rent_item in rent_order.rent_items]
        } for rent_order in rent_orders]
    })


def get_user_history(username, count):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return
    
    rent_order_ids = [
        rent_order.id
        for rent_order in RentOrder.query.filter_by(user=user).all()]
    rent_items = RentItem.query.\
                filter(RentItem.rent_order_id.in_(rent_order_ids)).\
                order_by(RentItem.start_date.desc()).\
                limit(count).all()
    return jsonify({
        'history': [{
            'rent_item_id': rent_item.id,
            'start_date': rent_item.start_date.isoformat(),
            'end_date': rent_item.end_date and rent_item.end_date.isoformat(),
            'status': rent_item.status,
            'movie_name': rent_item.movie.movie_name
        } for rent_item in rent_items]
    })


def create_order(username, order_details, payment_info, delivery_address):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return
    
    order = RentOrder(
        total_price=0,
        delivery_address=delivery_address,
        payment_info=payment_info,
        user=user)
    
    count = 0
    for order_detail in order_details:
        count += 1
        movie = Movie.query.filter_by(movie_name=order_detail['movie_name']).first()
        movie.stock -= 1
        order.add_movie_item(movie, datetime.now(), order_detail['length_days'])
    if count == 0:
        return
    
    order.calc_price()
    db.session.add(order)
    db.session.commit()
    return True
