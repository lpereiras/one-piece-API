from http import HTTPStatus


def test_delete_user(client, test_user):
    response = client.delete(f'/users/{test_user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': "I hope you're happy with the bounty. "}


def test_delete_user_not_found(client):
    response = client.delete(f'/users/{0}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'The one that you chasing is no longer between us.'}
