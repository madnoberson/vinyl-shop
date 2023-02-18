from fastapi import HTTPException, Depends
from asyncpg import Connection

from ..schemas.products import (
    BasicProdcut,
    BasicProductOut,
    Product,
    ProductIn,
    ProductOut,
    ProductUpdate,
    Update
)
from ..schemas.admin import Superuser

from .admin import get_superuser
from ..utils import sql_utils
from ..database import get_db_conn


class ProductsService:
    def __init__(
        self,
        db_connection: Connection = Depends(get_db_conn),
        superuser: Superuser = Depends(get_superuser)
    ) -> None:
        self.db_conn = db_connection
        self.superuser = superuser
    
    async def create_product(
        self,
        create_product: ProductIn
    ) -> ProductOut:
        if not self.superuser:
            raise HTTPException(404)
        
        columns, values = sql_utils.dict_to_sql_columns_and_values(
            create_product.dict(exclude_unset=True)
        )

        product_record = await self.db_conn.fetchrow(
            f"""
                INSERT INTO products
                {columns}
                VALUES
                {values}
                RETURNING name
            """
        )

        product = Product.parse_obj(
            dict(product_record)
        )

        return ProductOut(
            product=product
        )

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

    async def update_product(
        self,
        update_product: ProductUpdate
    ) -> ProductOut:
        if not self.superuser:
            raise HTTPException(404)
        
        update_product_dict = update_product.dict(
            exclude_unset=True
        )

        product_id = update_product_dict.pop('id')
        update_description = update_product_dict.pop('description')

        columns, values = sql_utils.dict_to_sql_columns_and_values(
            update_product_dict
        )

        records = await self.db_conn.fetch(
            f"""
                UPDATE products
                SET {columns} = {values}
                WHERE products.id = {product_id}
                RETURNING *;

                INSERT INTO products_updates
                (product_id, description, created_by)
                VALUES
                (
                    {product_id},
                    '{update_description}',
                    {self.superuser.id}
                )
                RETURNING description,
                          created_by
                          datetime AS created_at;
            """
        )

        product = Product.parse_obj(records[0])
        update = Update.parse_obj(records[1])

        return ProductOut(
            product=product,
            updates=update
        )