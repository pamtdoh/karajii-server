from app import db
from datetime import datetime

class RentItem(db.Model):
    __tablename__ = 'rent_item'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie')
    rent_order_id = db.Column(db.Integer, db.ForeignKey('rent_order.id'), nullable=False)
    rent_order = db.relationship('RentOrder', back_populates='rent_items')
    status = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    period_days = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<RentItem %r>' % self.movie


class RentOrder(db.Model):
    __tablename__ = 'rent_order'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Date, default=lambda: datetime.now())
    total_price = db.Column(db.Float, nullable=False)
    collection_mode = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='rent_orders')
    rent_items = db.relationship('RentItem', back_populates='rent_order')

    def __repr__(self):
        return '<RentOrder %r>' % self.user
