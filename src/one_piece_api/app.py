from http import HTTPStatus

from fastapi import FastAPI

from one_piece_api.schemas.API_version_schema import Version
from one_piece_api.schemas.user_schema import UserCreated, UserSchema

app = FastAPI(version='v0.0.1')


# Retorna a versão atual da API
@app.get('/one-piece-api/get-version', status_code=200, response_model=Version)
def API_version():
    return {'version': app.version}


# Realiza o cadastro de um novo usuário
@app.post(
    '/one-piece-api/sign-up',
    status_code=201,
    response_model=UserCreated,
)
def create_user(user: UserSchema):
    return user
