from fastapi import HTTPException, Depends, Request
from asyncpg import Connection
from pydantic import ValidationError
from jose import jwt, JWTError

from ..schemas.admin import Superuser

from ..database import get_db_conn
from ..settings import settings


async def get_superuser(request: Request) -> Superuser:
    token = request.cookies.get("superuser")

    if not token:
        return None

    return AdminService.validate_token(token)


class AdminService:
    def __init__(
        self,
        db_connection: Connection = Depends(get_db_conn)
    ) -> None:
        self.db_conn = db_connection

    @staticmethod
    def create_token(
        superuser_data: Superuser
    ) -> str:
        payload = {
            "superuser": superuser_data.dict()
        }

        token = jwt.encode(
            claims=payload,
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )

        return token

    @staticmethod
    def validate_token(
        token: str  
    ) -> Superuser | None:
        try:
            payload = jwt.decode(
                token=token,
                key=settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )

            superuser = Superuser.parse_obj(
                payload.get("superuser")
            )
        except (JWTError, ValidationError):
            return None

        return superuser
    