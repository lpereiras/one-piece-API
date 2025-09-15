from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from one_piece_api.models.devil_fruit_model import Devil_fruit
from one_piece_api.models.user_model import User
from one_piece_api.schemas.devil_fruit_schema import DevilFruitCreated, DevilFruitSchema
from security import get_current_user

router = APIRouter(prefix='/fruits', tags=['Devil Fruits'])
T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=201, response_model=DevilFruitCreated)
def register_devil_fruit(devil_fruit: DevilFruitSchema, session: T_Session, user: T_User):
    db_devil_fruit = session.scalar(select(Devil_fruit).where(Devil_fruit.name == devil_fruit.name))
    if db_devil_fruit:
        if db_devil_fruit.name == devil_fruit.name:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='That Devil fruit has already been added to our encyclopedia.',
            )
    db_devil_fruit = Devil_fruit(
        name=devil_fruit.name,
        description=devil_fruit.description,
        actual_user=devil_fruit.actual_user,
        type=devil_fruit.type,
    )

    session.add(db_devil_fruit)
    session.commit()
    session.refresh(db_devil_fruit)

    return db_devil_fruit
