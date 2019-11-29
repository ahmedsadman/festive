from config import Config as config_prod
from config_dev import Config as config_dev
from application import create_app


def wrapper_client(branch):
    if branch == "dev":
        app_config = config_dev
    else:
        app_config = config_prod

    flask_app = create_app(app_config)
    testing_client = flask_app.test_client()
    return testing_client
