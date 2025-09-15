from pydantic import BaseModel

from one_piece_api.models.devil_fruit_model import TypeEnumSchema


class DevilFruitSchema(BaseModel):
    name: str
    description: str
    actual_user: str
    type: TypeEnumSchema


class DevilFruitCreated(BaseModel):
    id: int
    name: str
    message: str = 'Added to Devil fruit encyclopedia'


class DevilFruitPublic(BaseModel):
    id: int
    name: str
    description: str
    actual_user: str
    type: TypeEnumSchema


class DevilFruitList(BaseModel):
    devul_fruits: list[DevilFruitPublic]
