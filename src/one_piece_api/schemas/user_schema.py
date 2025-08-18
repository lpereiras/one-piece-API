from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreated(BaseModel):
    id: int
    username: str
    message: str = 'User successfully registered!'

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserList(BaseModel):
    users: list[UserPublic]