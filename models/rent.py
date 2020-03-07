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
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    length_days = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<RentItem %r>' % self.movie


class RentOrder(db.Model):
    __tablename__ = 'rent_order'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now())
    total_price = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(100))
    payment_info = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='rent_orders')
    rent_items = db.relationship('RentItem', back_populates='rent_order')

    def add_movie_item(self, movie, start_date, length_days):
        rent_item = RentItem(
            movie=movie,
            rent_order=self,
            status='on_delivery',
            start_date=start_date,
            length_days=length_days)
        db.session.add(rent_item)
    
    def calc_price(self):
        self.total_price = sum(
            rent_item.movie.price
            for rent_item in self.rent_items)

    def __repr__(self):
        return '<RentOrder %r>' % self.user
