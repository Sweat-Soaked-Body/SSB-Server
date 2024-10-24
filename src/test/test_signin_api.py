import pytest

from user.models import ServiceUser


@pytest.mark.django_db
def test_signin_api(api_client):
    # given
    data = {
        "username": 'testsignin',
        "password": 'test'
    }
    ServiceUser.objects.create_user(**data)

    # when
    response = api_client.post('/auth/signin/', data=data)

    # then
    assert response.status_code == 200
