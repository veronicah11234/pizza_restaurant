from flask import jsonify, request, Blueprint, Response
import json
from sqlalchemy.exc import IntegrityError
from models import db, Restaurant, Pizza, RestaurantPizza  # Import db and models from models.py

main_bp = Blueprint('main', __name__)

@main_bp.route('/restaurant')
def index():
    return jsonify({"message": "Welcome to Pizza Restaurant API"})


@main_bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    
    # Construct a list of dictionaries containing restaurant data
    restaurants_data = []
    for restaurant in restaurants:
        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        }
        restaurants_data.append(restaurant_data)
    
    # Convert the list of dictionaries to JSON format
    json_data = json.dumps(restaurants_data, indent=2)
    
    # Return the JSON response with the appropriate content type
    return Response(json_data, mimetype='application/json')


@main_bp.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get_or_404(id)

    # Construct a list of dictionaries containing pizza data for the restaurant
    pizzas_data = []
    for pizza in restaurant.pizzas:
        pizza_data = {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }
        pizzas_data.append(pizza_data)

    # Construct the restaurant data dictionary including the list of pizzas
    restaurant_data = {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "pizzas": pizzas_data
    }

    # Convert the dictionary to JSON format
    json_data = json.dumps(restaurant_data, indent=2)

    # Return the JSON response with the appropriate content type
    return Response(json_data, mimetype='application/json')


@main_bp.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()  
    return '', 204

@main_bp.route('/restaurant_pizzas/<int:restaurant_id>/<int:pizza_id>', methods=['DELETE'])
def delete_restaurant_pizza(restaurant_id, pizza_id):
    # Find the RestaurantPizza record based on the restaurant_id and pizza_id
    restaurant_pizza = RestaurantPizza.query.filter_by(restaurant_id=restaurant_id, pizza_id=pizza_id).first()

    if restaurant_pizza:
        db.session.delete(restaurant_pizza)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Restaurant pizza not found"}), 404


@main_bp.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()

    # Custom JSON formatting
    pizzas_data = [
        '{\n'
        '  "id": ' + str(pizza.id) + ',\n'
        '  "name": "' + pizza.name + '",\n'
        '  "ingredients": "' + pizza.ingredients + '"\n'
        '}' for pizza in pizzas
    ]
    
    # Join the list of pizza objects with commas and newlines
    response = ",\n".join(pizzas_data)
    
    # Add square brackets to encapsulate the list
    response = "[\n" + response + "\n]"

    # Return the response with the correct content type
    return response, 200, {'Content-Type': 'application/json'}

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
    price = int(data.get('price'))
    pizza_id = int(data.get('pizza_id'))
    restaurant_id = int(data.get('restaurant_id'))
    
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
