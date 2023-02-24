from fastapi import APIRouter, Depends

from ..schemas.users import (
    UserOut,
    UserWishlistOut
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
    '/wishlist/'
)
async def add_to_wishlist(
   product_id: int,
   users_service: UsersService = Depends()
):
    return await users_service.add_to_wishlist(
        product_id=product_id
    )


@router.get(
    '/wishlist/',
    response_model=UserWishlistOut
)
async def get_wishlist(
    page: int = 1,
    users_service: UsersService = Depends()
) -> UserWishlistOut:
    return await users_service.get_wishlist(
        page=page
    )


@router.delete(
    '/wishlist/',
)
async def delete_from_wishlist(
    product_id: int,
    users_service: UsersService = Depends()
):
    return await users_service.delete_from_wishlist(
        product_id=product_id
    )