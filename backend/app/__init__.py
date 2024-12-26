from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.Config')

    # Initialize SQLAlchemy
    db.init_app(app)

    # Setup Swagger
    swagger = Swagger(app)
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.yaml'  # Path to your Swagger YAML file
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "CRUD API"}
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Import and register routes
    with app.app_context():
        from app import routes
    
    return app
