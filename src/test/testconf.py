import pytest

from test.utils import APIClient


@pytest.fixture(scope='session')
def api_client():
    return APIClient()