from flask import jsonify, request, Blueprint
from sqlalchemy.exc import IntegrityError
from models import db, Restaurant, Pizza, RestaurantPizza  # Import db and models from models.py

main_bp = Blueprint('main', __name__)

@main_bp.route('/restaurant')
def index():
    return jsonify({"message": "Welcome to Pizza Restaurant API"})

@main_bp.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    pizzas = [{
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    } for pizza in restaurant.pizzas]
    return jsonify({
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "pizzas": pizzas
    })

@main_bp.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()  
    return '', 204

@main_bp.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    } for pizza in pizzas])

@main_bp.route('/pizzas', methods=['POST'])
def create_pizza():
    data = request.json

    name = data.get('name')
    ingredients = data.get('ingredients')
    new_pizza = Pizza(name=name, ingredients=ingredients)

    try:
        db.session.add(new_pizza)
        db.session.commit()
        return jsonify({'message': 'Pizza created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    
    if not all([price, pizza_id, restaurant_id]):
        return jsonify({"errors": ["All fields are required"]}), 400

    if not 1 <= price <= 30:
        return jsonify({"errors": ["Price must be between 1 and 30"]}), 400

    restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
    db.session.add(restaurant_pizza)

    try:
        db.session.commit()  # Committing the changes to the database session
        pizza = Pizza.query.get(pizza_id)
        return jsonify({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }), 201
    except IntegrityError:
        db.session.rollback()  # Rollback the session if there's an integrity error
        return jsonify({"errors": ["Restaurant or Pizza not found"]}), 404

@main_bp.route('/favicon.ico')
def favicon():
    return "", 404
