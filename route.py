from flask import jsonify, request
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

# Define routes here

@app.route('/')
def index():
    return jsonify({"message": "Welcome to Pizza Restaurant API"})

@app.route('/restaurants/<int:id>', methods=['GET'])
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

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    } for pizza in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
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
        db.session.commit()
        pizza = Pizza.query.get(pizza_id)
        return jsonify({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Restaurant or Pizza not found"]}), 404


@app.route('/favicon.ico')
def favicon():
    return "", 404
