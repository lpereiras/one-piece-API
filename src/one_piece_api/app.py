from http import HTTPStatus

from fastapi import FastAPI

from one_piece_api.schemas.schema_API_version import Version
from one_piece_api.schemas.schema_create_new_user import CreateNewUser

app = FastAPI(version='v0.1.0')


@app.get('/', status_code=200, response_model=Version)
def API_version():
    return {'version': app.version}


@app.post(
    '/one-piece-api/sign-up',
    status_code=201,
    response_model=CreateNewUser,
)
def create_new_user():
    return {'message': 'Usuário registrado com sucesso!'}
