from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class BasicProduct(BaseModel):
    id: int
    name: str


class BasicProductOut(BaseModel):
    product: BasicProduct


class Product(BasicProduct):
    pass


class ProductIn(BaseModel):
    name: str


class ProductUpdate(BaseModel):
    description: str
    created_by: int
    created_at: datetime

    @validator('created_at')
    def get_date(datetime_obj: datetime) -> str:
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")


class ProductUpdateIn(BaseModel):
    name: Optional[str] = None

    description: str


class ProductUpdateOut(BaseModel):
    product: Product
    update: ProductUpdate


class ProductOut(BaseModel):
    product: Product

    updates: Optional[list[ProductUpdate]] = None
