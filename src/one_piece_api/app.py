from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from one_piece_api.models.user_model import User
from one_piece_api.schemas.API_version_schema import Version
from one_piece_api.schemas.login_schema import GetToken
from one_piece_api.schemas.user_schema import UserCreated, UserList, UserPublic, UserSchema
from security import get_access_token, get_current_user, get_password_hash, verify_password

app = FastAPI(version='v0.0.2', title='One Piece API')


# Retorna a versão atual da API
@app.get('/version', status_code=200, response_model=Version)
def API_version():
    return {'version': app.version}


# Realiza o cadastro de um novo usuário
@app.post(
    '/users/',
    status_code=201,
    response_model=UserCreated,
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
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
    db_user = User(
        username=user.username, email=user.email, password=get_password_hash(user.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


# Realiza uma busca por todos os usuários registrados
@app.get('/users/', status_code=200, response_model=UserList)
def list_users(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 10,
    current_user=Depends(get_current_user),
):
    db_users = session.scalars(select(User).limit(limit).offset(skip)).all()
    return {'users': db_users}


# Realiza uma busca por um usuário específico baseado em seu {user_id}
@app.get('/users/{user_id}', status_code=200, response_model=UserPublic)
def list_specific_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='There is nothing to see here. Or are you searching for '
            'someone from the Void Century?',
        )
    else:
        return db_user


# Realiza exclusão de um usuário específico baseado em seu {user_id}
@app.delete('/users/{user_id}', status_code=200)
def delete_user(
    user_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Are you trying to manipulate data that doesn't belong to your concern? "
            'Morgans will know that',
        )
    else:
        session.delete(current_user)
        session.commit()
    return {'message': "I hope you're satisfied with the bounty."}


# Verifica se o usuário já existe na base de dados, e retorna token de acesso se for o caso
@app.post('/token', status_code=200, response_model=GetToken)
def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
):
    user = session.scalar(select(User).where(User.username == form_data.username))
    invalid_access = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Invalid username or password',
    )

    if not user:
        raise invalid_access

    elif not verify_password(form_data.password, user.password):
        raise invalid_access

    access_token = get_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'Bearer'}
