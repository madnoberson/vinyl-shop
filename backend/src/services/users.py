from typing import Optional

from fastapi import HTTPException, Depends
from asyncpg import Connection

from ..schemas.users import (
    BasicUser,
    User,
    UserOut,
    UserWishlist,
    UserWishlistOut
)
from ..schemas.products import BasicProduct

from .auth import get_current_user
from ..database import get_db_conn
from ..settings import settings


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
                    array_agg(users_wishes.product_id) AS wishlist
                FROM
                    users
                JOIN
                    users_wishes
                    ON
                    users_wishes.user_id = users.id
                WHERE
                    users.id = {self.current_user.id}
                GROUP BY
                    users.id
                LIMIT 1
            """
        )

        user_dict = dict(user_record) | {"scopes": []}
        print(user_dict)

        user = User.parse_obj(user_dict)

        return UserOut(
            user=user
        )

    async def add_to_wishlist(
        self,
        product_id: int
    ):
        if not self.current_user:
            raise HTTPException(401)
        
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
        
    async def get_wishlist(
        self,
        page: Optional[int] = 1
    ) -> UserWishlistOut:
        if not self.current_user:
            raise HTTPException(401)

        elems_per_page = settings.user_wishlist_elems_per_page

        wishes_records = await self.db_conn.fetch(
            f"""
                WITH products_ids AS (
                    SELECT
                        users_wishes.product_id
                    FROM
                        users_wishes
                    WHERE
                        users_wishes.user_id = {self.current_user.id}
                    LIMIT {elems_per_page}
                    OFFSET {elems_per_page * (page - 1)}
                )
                SELECT
                    products.id,
                    products.name
                FROM
                    products
                WHERE
                    products.id IN products_ids
                LIMIT {elems_per_page}
                OFFSET {elems_per_page * (page - 1)}   
            """
        )

        products = []
        if wishes_records:
            products = [
                BasicProduct.parse_obj(dict(product))
                for product in wishes_records
            ]

        wishlist = UserWishlist(
            products=products
        )

        return UserWishlistOut(
            wishlist=wishlist
        )
    
    async def delete_from_wishlist(
        self,
        product_id: int
    ): 
        if not self.current_user:
            raise HTTPException(401)
        
        await self.db_conn.execute(
            f"""
                DELETE
                FROM
                    users_wishlists
                WHERE
                    users_wishlists.user_id = {self.current_user.id}
                    AND
                    users_wishlists.product_id = {product_id}
            """
        )



