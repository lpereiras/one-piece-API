from http import HTTPStatus

from one_piece_api.schemas.user_schema import UserPublic


def test_list_users_when_exists(client, test_user, test_other_user, generate_test_token):
    test_user_schema = UserPublic.model_validate(test_user).model_dump()
    test_other_user_schema = UserPublic.model_validate(test_other_user).model_dump()

    response = client.get('/users', headers={'Authorization': f'Bearer {generate_test_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [test_user_schema, test_other_user_schema]}
