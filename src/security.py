from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from one_piece_api.models.user_model import User
from settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_access_token(payload_data: dict):
    to_encode = payload_data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, key=Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)
    return encoded_jwt


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Gossips says that only Morgans manipulate's data with that "
        'freedom of not getting catched.',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
        username = payload.get('sub')

        if not username:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    db_user = session.scalar(select(User).where(User.username == username))

    if not db_user:
        raise credentials_exception
    return db_user
