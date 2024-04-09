from sqlalchemy.orm import validates
from app import db  # Moved db import from app.py to models.py

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Added unique constraint
    address = db.Column(db.String(100), nullable=False)
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', backref='restaurants')

    @validates('name')
    def validate_name(self, key, name):
        # Validate name length
        if len(name) > 50:
            raise ValueError("Name must be less than 50 characters")
        return name

class Pizza(db.Model):
    __tablename__ = 'pizza'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

    # Add any other columns you need for the pizza table

    def __repr__(self):
        return f'Pizza(id={self.id}, name={self.name}, ingredients={self.ingredients})'

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
