import pytest


@pytest.mark.django_db
def test_signup_api(api_client):
    # given
    data = {
        "username": 'testsignup',
        "email": 'test@test.com',
        "password": 'test'
    }

    # when
    response = api_client.post('/auth/signup/', data=data)

    # then
    assert response.status_code == 201
