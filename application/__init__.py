from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# globally accessible variables
db = SQLAlchemy()

def create_app():
    '''Create the core application, uses application factory pattern'''
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from . import routes
        
        db.create_all()
        return app