def test_health_check_api(api_client):
    # when
    response = api_client.get('/health-check')

    # then
    assert response.status_code == 200
