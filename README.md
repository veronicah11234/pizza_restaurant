# Title
Pizza Restaurants API

# Description
This project implements a Flask-based API for managing pizza restaurants and their associated pizzas. It provides endpoints for retrieving restaurant information, managing pizzas, and creating relationships between restaurants and pizzas.

# Features
- Restaurant Management: Create, retrieve, update, and delete restaurants.
- Pizza Management: Create, retrieve, update, and delete pizzas.
- Relationships: Establish relationships between restaurants and pizzas, allowing a pizza to belong to multiple      restaurants and vice versa.
- Validation: Validate input data to ensure consistency and integrity in the database.
- API Endpoints: Provides RESTful endpoints for interacting with the API.

# Setup
Clone the repository:
git clone <repository-url>

- Install dependencies:
pip install -r requirements.txt

- Run the database migrations:
flask db upgrade

- Start the Flask server:
flask run


# API Endpoints
- GET /restaurants: Retrieve a list of all restaurants.
- GET /restaurants/:id: Retrieve information about a specific restaurant by ID.
- DELETE /restaurants/:id: Delete a restaurant by ID.
- GET /pizzas: Retrieve a list of all pizzas.
- POST /restaurant_pizzas: Create a new restaurant-pizza relationship.

# Author
Name-Miriam wangui 
Github- https://github.com/veronicah11234/pizza_restaurant.git

# License
This project is licensed under the MIT License.


