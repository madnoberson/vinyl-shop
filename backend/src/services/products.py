from datetime import datetime

from fastapi import HTTPException, Depends
from asyncpg import Connection

from ..schemas.products import (
    BasicProduct,
    BasicProductOut,
    Product,
    ProductIn,
    ProductOut,
    ProductUpdate,
    ProductUpdateIn,
    ProductUpdateOut

)
from ..schemas.users import BasicUser

from .auth import get_current_user
from .admin import scopes_required
from ..utils import sql_utils
from ..database import get_db_conn


class ProductsService:
    def __init__(
        self,
        db_connection: Connection = Depends(get_db_conn),
        current_user: BasicUser = Depends(get_current_user)
    ) -> None:
        self.db_conn = db_connection
        self.current_user = current_user
    
    @scopes_required(scopes=['edit'])
    async def create_product(
        self,
        create_product: ProductIn
    ) -> ProductOut:
        columns, values = sql_utils.dict_to_sql_columns_and_values(
            create_product.dict(exclude_unset=True)
        )

        print(
            f"""
                INSERT INTO products
                {columns}
                VALUES
                {values}
                RETURNING id, name
            """
        )

        product_record = await self.db_conn.fetchrow(
            f"""
                INSERT INTO products
                {columns}
                VALUES
                {values}
                RETURNING id, name
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
    ) -> BasicProduct:
        product_record = await self.db_conn.fetchrow(
            f"SELECT * FROM get_basic_product({product_id})"
        )
        
        if not product_record:
            raise HTTPException(404)
        
        product = BasicProduct.parse_obj(dict(product_record))

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

    @scopes_required(scopes=['edit'])
    async def update_product(
        self,
        product_id: int,
        update_product: ProductUpdateIn
    ) -> ProductOut:
        update_product_dict = update_product.dict(
            exclude_unset=True
        )

        update_description = update_product_dict.pop('description')

        columns, values = sql_utils.dict_to_sql_columns_and_values(
            update_product_dict, mode='update'
        )

        async with self.db_conn.transaction():
            product_record = await self.db_conn.fetchrow(
                f"""
                    UPDATE products
                    SET {columns} = {values}
                    WHERE products.id = {product_id}
                    RETURNING *
                    ;
                """
            )

            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            update_record = await self.db_conn.fetchrow(
                f"""
                    INSERT INTO products_updates
                    (
                        product_id,
                        description,
                        created_by,
                        created_at
                    )
                    VALUES
                    (
                        {product_id},
                        '{update_description}',
                        {self.current_user.id},
                        '{created_at}'
                        
                    )
                    RETURNING description,
                              created_by,
                              created_at
                    ;
                """
            )


        product = Product.parse_obj(product_record)
        update = ProductUpdate.parse_obj(update_record)

        print(product, update)

        return ProductUpdateOut(
            product=product,
            update=update
        )
    
    @scopes_required(scopes=['edit'])
    async def delete_product(
        self,
        product_id: int
    ):
        status = await self.db_conn.execute(
            f"""
                DELETE
                FROM products
                WHERE products.id = {product_id}
            """
        )

        print(status)
