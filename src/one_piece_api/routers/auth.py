from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from one_piece_api.models.user_model import User
from one_piece_api.schemas.login_schema import GetToken
from security import get_access_token, get_current_user, verify_password

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/token', status_code=200, response_model=GetToken)
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

    access_token = get_access_token(payload_data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh-token', status_code=200, response_model=GetToken)
def refresh_token(user: User = Depends(get_current_user)):
    refreshed_token = get_access_token(payload_data={'sub': user.username})

    return {'access_token': refreshed_token, 'token_type': 'Bearer'}
