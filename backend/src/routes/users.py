from typing import Optional

from fastapi import APIRouter, Depends

from ..schemas.users import (
    UserOut,
    UserWishlist
)
from ..services.users import UsersService


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get(
    '/',
    response_model=UserOut
)
async def get_user(
    users_service: UsersService = Depends()
) -> UserOut:
    return await users_service.get_user()


@router.post(
    '/wishlist/',
    status_code=201
)
async def add_to_wishlist(
   product_id: int,
   users_service: UsersService = Depends()
):
    await users_service.add_to_wishlist(
        product_id=product_id
    )


@router.get(
    '/wishlist/',
    response_model=UserWishlist
)
async def get_wishlist(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    users_service: UsersService = Depends()
) -> UserWishlist:
    return await users_service.get_wishlist(
        limit=limit, offset=offset
    )


@router.delete(
    '/wishlist/',
    status_code=204
)
async def delete_from_wishlist(
    product_id: int,
    users_service: UsersService = Depends()
):
    return await users_service.delete_from_wishlist(
        product_id=product_id
    )