from http import HTTPStatus


def test_delete_user(client, test_user, generate_test_token):
    response = client.delete(
        f'/users/{test_user.id}',
        headers={'Authorization': f'Bearer {generate_test_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Vanished like informations about the Void Century.'}


def test_delete_wrong_user(client, test_other_user, generate_test_token):
    response = client.delete(
        f'/users/{test_other_user.id}',
        headers={'Authorization': f'Bearer {generate_test_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': "Gossips says that only Morgans manipulate's data with that "
        'freedom of not getting catched.'
    }
