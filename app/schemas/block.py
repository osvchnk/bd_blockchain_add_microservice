from datetime import datetime

from pydantic import BaseModel


class BlockBaseSchema(BaseModel):
    date: datetime
    prev_hash: str
    transactions: list[str]


class BlockHashedSchema(BlockBaseSchema):
    hash: str


class BlockSignedSchema(BlockHashedSchema):
    admin_sign: str

    class Config:
        orm_mode = True


class BlockCreateSchema(BaseModel):
    date: datetime
    prev_hash: str
    hash: str
    admin_sign: str


class BlockOutSchema(BlockCreateSchema):
    id: int

    class Config:
        orm_mode = True
