from fastapi import APIRouter, Depends

from ..schemas.auth import (
    Token,
    UserSignUp,
    UserSignIn
)

from ..services.auth import AuthService


router = APIRouter(
    tags=['auth']
)


@router.post(
    '/sign_up/',
    response_model=Token
)
async def sign_up(
    create_user: UserSignUp,
    auth_service: AuthService = Depends()
) -> Token:
    return await auth_service.sign_up(
        create_user=create_user
    )


@router.post(
    '/sign_in/',
    response_model=Token
)
async def sign_in(
    user_data: UserSignIn,
    auth_service: AuthService = Depends()
) -> Token:
    return await auth_service.sign_in(
        user_data=user_data
    )