from http import HTTPStatus


def test_API_version_validate_version(client):
    response = client.get('/version')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'version': 'v0.0.3'}
