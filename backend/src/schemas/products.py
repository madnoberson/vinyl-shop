from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Update(BaseModel):
    description: str
    created_by: int
    created_at: datetime


class BasicProdcut(BaseModel):
    id: int
    name: str


class BasicProductOut(BaseModel):
    product: BasicProdcut


class Product(BasicProdcut):
    pass


class ProductIn(BaseModel):
    name: str


class ProductUpdate(BaseModel):
    id: int
    name: Optional[str] = None


class ProductOut(BaseModel):
    product: Product

    updates: Optional[Update | list[Update]] = None
