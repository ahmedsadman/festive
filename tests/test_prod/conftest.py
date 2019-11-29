import pytest
from tests.conftest_wrapper import wrapper_client

# holds all the fixtures
# fixtures are ran once during request, this client will be passed in
# other test_*.py files


@pytest.fixture(scope="module")
def client(request):
    return wrapper_client("prod")
