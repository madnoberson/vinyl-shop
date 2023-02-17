from fastapi import HTTPException, Depends
from asyncpg import Connection

from ..schemas.products import (
    BasicProdcut,
    BasicProductOut,
    Product,
    ProductOut
)

from ..database import get_db_conn


class ProductsService:
    def __init__(
        self,
        db_connection: Connection = Depends(get_db_conn)
    ) -> None:
        self.db_conn = db_connection

    async def get_basic_product(
        self,
        product_id: int
    ) -> BasicProdcut:
        product_record = await self.db_conn.fetchrow(
            f"SELECT * FROM get_basic_product({product_id})"
        )
        
        if not product_record:
            raise HTTPException(404)
        
        product = BasicProdcut.parse_obj(dict(product_record))

        return BasicProductOut(
            product=product
        )

    async def get_product(
        self,
        product_id: int
    ) -> ProductOut:
        product_record = await self.db_conn.fetchrow(
            f"SELECT * FROM products WHERE id = {product_id}"
        )

        if not product_record:
            raise HTTPException(404)
        
        product = Product.parse_obj(dict(product_record))

        return ProductOut(
            product=product
        )