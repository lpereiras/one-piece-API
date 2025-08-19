from http import HTTPStatus

from one_piece_api.schemas.user_schema import UserPublic


def test_list_users(client, test_user):
    test_user_schema = UserPublic.model_validate(test_user).model_dump()

    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [test_user_schema]}
