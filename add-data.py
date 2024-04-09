from app import create_app, db
from models import Restaurant, Pizza, RestaurantPizza  # Import models directly

app = create_app()

with app.app_context():
    db.create_all()

    pizza1 = Pizza(name='Margherita', ingredients='Tomato sauce, mozzarella cheese, basil')
    pizza2 = Pizza(name='Pepperoni', ingredients='Tomato sauce, mozzarella cheese, pepperoni, peppers, onions')
    pizza3 = Pizza(name='Vegetarian', ingredients='Tomato sauce, mozzarella cheese, mushrooms, peppers, onions, olives')

    restaurant1 = Restaurant(name='Pizza Palace', address='123 Main Street')
    restaurant2 = Restaurant(name='Italian Delight', address='456 Oak Avenue')

    db.session.add_all([pizza1, pizza2, pizza3, restaurant1, restaurant2])
    db.session.commit()

    print("Realistic items have been added to the database.")
