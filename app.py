from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize db outside of the create_app function
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurants.db'

    # Initialize db with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints here to avoid circular imports
    from route import main_bp  # Moved the import inside the function
    app.register_blueprint(main_bp)

    return app
