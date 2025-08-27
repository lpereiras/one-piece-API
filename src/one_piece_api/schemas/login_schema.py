from pydantic import BaseModel


class GetToken(BaseModel):
    access_token: str
    token_type: str
