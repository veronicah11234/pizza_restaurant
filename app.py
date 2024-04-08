# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask.cli import FlaskGroup


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurants.db'
    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints and register them here
    from .route import main_bp
    app.register_blueprint(main_bp)

    return app

app = create_app()


cli = FlaskGroup(app)
cli.add_command('db', MigrateCommand)

if __name__ == '__main__':
    cli()