from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from one_piece_api.models.user_model import User
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from settings.settings import Settings
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
    engine = create_engine(Settings().DATABASE_URL)

    with Session(engine) as session:
        db_user = session.scalar(
            select(User).where(
                (User.username == user.username) | (User.email == user.email)
            )
        )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='That username has already been claimed by another pirate.',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='This email is already taken.',
            )
        elif db_user.username is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail="You cant't go on a journey at these seas without a username.",
            )
    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
