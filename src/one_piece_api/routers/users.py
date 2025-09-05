from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from one_piece_api.models.user_model import User
from one_piece_api.schemas.user_schema import UserCreated, UserList, UserPublic, UserSchema
from security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['Users'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/',
    status_code=201,
    response_model=UserCreated,
)
def create_user(user: UserSchema, session: T_Session):
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


@router.get('/{user_id}', status_code=200, response_model=UserPublic)
def list_specific_user(
    user_id: int,
    session: T_Session,
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


@router.get('/', status_code=200, response_model=UserList)
def list_users(
    session: T_Session,
    skip: int = 0,
    limit: int = 10,
    current_user=Depends(get_current_user),
):
    db_users = session.scalars(select(User).limit(limit).offset(skip)).all()
    return {'users': db_users}


@router.delete('/{user_id}', status_code=200)
def delete_user(user_id: int, session: T_Session, current_user=Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Gossips says that only Morgans manipulate's data with that "
            'freedom of not getting catched.',
        )
    else:
        session.delete(current_user)
        session.commit()
    return {'message': 'Vanished like informations about the Void Century.'}
