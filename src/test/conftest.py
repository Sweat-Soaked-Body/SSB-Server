import pytest

from test.utils import APIClient
import django


@pytest.fixture(scope='session')
def api_client():
    django.setup()
    return APIClient()