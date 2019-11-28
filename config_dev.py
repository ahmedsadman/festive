import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """holds all the configuration for the flask application"""

    # general config
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    PROPAGATE_EXCEPTIONS = True

    # database for dev test
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_DEV")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
