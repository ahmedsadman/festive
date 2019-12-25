from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from application.error_handlers import *

# globally accessible variables
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config):
    """Create the core application, uses application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register error handler
    @app.errorhandler(BaseError)
    def handle_request_error(error):
        return error.to_dict(), error.status

    with app.app_context():
        # import blueprints
        from .resources.info import info_bp
        from .resources.event import event_bp
        from .resources.register import register_bp
        from .resources.participant import participant_bp
        from .resources.auth import auth_bp
        from .resources.team import team_bp
        from .resources.payment import payment_bp

        # register blueprints
        app.register_blueprint(info_bp, url_prefix="/")
        app.register_blueprint(event_bp, url_prefix="/event")
        app.register_blueprint(register_bp, url_prefix="/register")
        app.register_blueprint(participant_bp, url_prefix="/participant")
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(team_bp, url_prefix="/team")
        app.register_blueprint(payment_bp, url_prefix="/payment")

        db.create_all()
        return app
