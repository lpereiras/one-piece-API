# import uuid

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreated(BaseModel):
    # user_id: uuid.uuid4()
    username: str
    message: str
    message = 'User successfully registered!'


class UpdateUser(UserSchema):
    message: str
    message = 'User successfully updated!'
