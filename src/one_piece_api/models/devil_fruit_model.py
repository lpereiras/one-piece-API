from datetime import datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


class TypeEnumSchema(str, Enum):
    ZOAN = 'ZOAN'
    PARAMECIA = 'PARAMECIA'
    LOGIA = 'LOGIA'


@table_registry.mapped_as_dataclass
class Devil_fruit:
    __tablename__ = 'devil_fruits'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    actual_user: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[TypeEnumSchema]
    # TODO: fruit_picture need to see how to handle images
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    # TODO: character_id: Mapped[str] = mapped_column(ForeignKey='')
    # create the relationship between a character and his devil fruit
    # if they eated some
