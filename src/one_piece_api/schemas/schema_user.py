from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreated(BaseModel):
    username: str
    message: str
    message = 'Usuário registrado com sucesso!'
