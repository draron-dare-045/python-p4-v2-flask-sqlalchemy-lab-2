from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Set naming convention for migrations
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    items = association_proxy('reviews', 'item')

    __serialize_rules__= ('-reviews.customer', '-reviews.item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')
    customers = association_proxy('reviews', 'customer')

    __serialize_rules__ = ('-reviews.item', '-reviews.customer')
   
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    item = db.relationship('Item', back_populates='reviews')
    customer = db.relationship('Customer', back_populates='reviews')

    __serialize_rules__ = ('-item.reviews', '-customer.reviews')

    def __repr__(self):
        return f'<Review {self.id}, Item: {self.item_id}, Customer: {self.customer_id}, Rating: {self.rating}>'
