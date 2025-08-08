from pydantic import BaseModel


class CreateNewUser(BaseModel):
    message: str
    message = 'Usuário registrado com sucesso!'
