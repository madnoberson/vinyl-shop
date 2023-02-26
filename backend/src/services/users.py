from typing import Optional

from fastapi import HTTPException, Depends
from asyncpg import Connection, ForeignKeyViolationError

from ..schemas.users import (
    BasicUser,
    User,
    UserOut,
    UserWishlist
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
    ):
        if not self.current_user:
            raise HTTPException(401)
        
        async with self.db_conn.transaction():
            try:
                await self.db_conn.execute(
                    f"""
                        INSERT INTO users_wishes
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
            
            try:
                await self.db_conn.execute(
                    f"""
                        UPDATE
                            users
                        SET
                            wishes_count = wishes_count + 1
                        WHERE
                            id = {self.current_user.id}
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
                    users_wishes
                LEFT JOIN
                    products
                    ON
                    products.id = users_wishes.product_id
                WHERE
                    users_wishes.user_id = {self.current_user.id}
                LIMIT {limit}
                OFFSET {offset}
            """ 
        )

        wishlist_products = [
            BasicProduct.parse_obj(dict(product))
            for product in wishlist_products_records 
        ]

        return UserWishlist(products=wishlist_products)
    
    async def delete_from_wishlist(
        self,
        product_id: int
    ): 
        if not self.current_user:
            raise HTTPException(401)
        
        
        status = await self.db_conn.execute(
            f"""
                DELETE
                FROM
                    users_wishes
                WHERE
                    users_wishes.user_id = {self.current_user.id}
                    AND
                    users_wishes.product_id = {product_id}
            """
        )

        if status == "DELETE 0":
            raise HTTPException(404)
        



