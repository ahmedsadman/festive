import pytest
from dotenv import load_dotenv
from application import create_app
from config import Config

# holds all the fixtures
# fixtures are ran once during request, this client will be passed in
# other test_*.py files


@pytest.fixture(scope="module")
def client(request):
    flask_app = create_app(Config)
    testing_client = flask_app.test_client()
    return testing_client
