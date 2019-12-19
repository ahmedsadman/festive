import os


class Config:
    """holds all the configuration for the flask application"""

    # general config
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    PROPAGATE_EXCEPTIONS = True

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
