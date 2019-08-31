from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from application.error_handlers import *

# globally accessible variables
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    '''Create the core application, uses application factory pattern'''
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register error handler
    @app.errorhandler(BaseError)
    def handle_request_error(error):
        return error.to_dict(), error.status

    with app.app_context():
        from . import routes
        
        db.create_all()
        return app