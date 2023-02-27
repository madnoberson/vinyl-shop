from typing import Optional

from fastapi import HTTPException, Depends
from asyncpg import Connection, ForeignKeyViolationError

from ..schemas.users import (
    BasicUser,
    User,
    UserOut,
    UserWishlist,
    UserCart
)
from ..schemas.products import BasicProduct

from .auth import get_current_user
from ..database import get_db_conn


class UsersService:
    def __init__(
        self,
        db_connection: Connection = Depends(get_db_conn),
        current_user: BasicUser = Depends(get_current_user)
    ) -> None:
        self.db_conn = db_connection
        self.current_user = current_user
    
    async def get_user(self) -> UserOut:
        if not self.current_user:
            raise HTTPException(401)

        user_record = await self.db_conn.fetchrow(
            f"""
                SELECT
                    users.*,
                    superusers.scopes
                FROM
                    users
                LEFT JOIN
                    superusers
                    ON
                    superusers.user_id = users.id
                WHERE
                    users.id = {self.current_user.id}
                LIMIT 1
            """
        )

        user_dict = dict(user_record)
        user_dict.pop("password")
        user = User.parse_obj(user_dict)

        wishlist = await self.get_wishlist()

        return UserOut(
            user=user,
            wishlist=wishlist
        )

    async def add_to_wishlist(
        self,
        product_id: int
    ) -> None:
        if not self.current_user:
            raise HTTPException(401)
        
        async with self.db_conn.transaction():
            try:
                await self.db_conn.execute(
                    f"""
                        INSERT INTO users_wishlist_products
                        (
                            product_id,
                            user_id
                        )
                        VALUES
                        (
                            {product_id},
                            {self.current_user.id}
                        )
                    """
                )
            except ForeignKeyViolationError:
                raise HTTPException(404)

        
    async def get_wishlist(
        self,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0
    ) -> UserWishlist:
        if not self.current_user:
            raise HTTPException(401)

        wishlist_products_records = await self.db_conn.fetch(
            f"""
                SELECT
                    products.id,
                    products.name
                FROM
                    users_wishlist_products
                LEFT JOIN
                    products
                    ON
                    products.id = users_wishlist_products.product_id
                WHERE
                    users_wishlist_products.user_id = {self.current_user.id}
                LIMIT {limit}
                OFFSET {offset}
            """ 
        )

        wishlist_products = [
            BasicProduct.parse_obj(dict(product))
            for product in wishlist_products_records 
        ]

        wishlist_products_count = await self.db_conn.fetchval(
            f"""
                SELECT
                    users_counts.wishlist_products_count
                FROM
                    users_counts
                WHERE
                    users_counts.user_id = {self.current_user.id}
            """
        )

        return UserWishlist(
            products=wishlist_products,
            products_count=wishlist_products_count
        )
    
    async def delete_from_wishlist(
        self,
        product_id: int
    ) -> None: 
        if not self.current_user:
            raise HTTPException(401)
        
        
        async with self.db_conn.transaction():
            status = await self.db_conn.execute(
                f"""
                    DELETE
                    FROM
                        users_wishlist_products
                    WHERE
                        users_wishlist_products.user_id = {self.current_user.id}
                        AND
                        users_wishlist_products.product_id = {product_id}
                """
            )

            if status == "DELETE 0":
                raise HTTPException(404)


    async def add_to_cart(
        self,
        product_id: int
    ) -> None:
        if not self.current_user:
            raise HTTPException(401)
        
        async with self.db_conn.transaction():
            try:
                await self.db_conn.execute(
                    f"""
                        INSERT INTO users_cart_products
                        (
                            product_id,
                            user_id
                        )
                        VALUES
                        (
                            {product_id},
                            {self.current_user.id}
                        )
                    """
                )
            except ForeignKeyViolationError:
                raise HTTPException(404)
            

    async def get_cart(
        self,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0
    ) -> UserCart:
        if not self.current_user:
            raise HTTPException(401)
        
        cart_products_records = await self.db_conn.fetch(
            f"""
                SELECT
                    products.id,
                    products.name
                FROM
                    users_cart_products
                LEFT JOIN
                    products
                    ON
                    products.id = users_cart_products.product_id
                WHERE
                    users_cart_products.user_id = {self.current_user.id}
                LIMIT {limit}
                OFFSET {offset}
            """ 
        )

        cart_products = [
            BasicProduct.parse_obj(dict(product))
            for product in cart_products_records 
        ]

        cart_products_count = await self.db_conn.fetchval(
            f"""
                SELECT
                    users_counts.cart_products_count
                FROM
                    users_counts
                WHERE
                    users_counts.user_id = {self.current_user.id}
            """
        )

        return UserCart(
            products=cart_products,
            products_count=cart_products_count
        )
    
    async def delete_from_cart(
        self,
        product_id: int
    ) -> None:
        if not self.current_user:
            raise HTTPException(401)
        
        async with self.db_conn.transaction():
            status = await self.db_conn.execute(
                f"""
                    DELETE
                    FROM
                        users_cart_products
                    WHERE
                        users_cart_products.user_id = {self.current_user.id}
                        AND
                        users_cart_products.product_id = {product_id}
                """
            )

            if status == "DELETE 0":
                raise HTTPException(404)
        
