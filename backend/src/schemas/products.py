from pydantic import BaseModel


class BasicProdcut(BaseModel):
    id: int
    name: str


class BasicProductOut(BaseModel):
    product: BasicProdcut


class Product(BasicProdcut):
    pass


class ProductOut(BaseModel):
    product: Product