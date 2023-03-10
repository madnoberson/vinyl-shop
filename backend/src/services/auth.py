from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from asyncpg import Connection, UniqueViolationError
from pydantic import ValidationError
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.hash import bcrypt

from ..schemas.users import BasicUser
from ..schemas.auth import (
    Token,
    UserSignUp,
    UserSignIn
)

from ..utils.scopes import get_scopes_from_scopes_sum
from ..database import get_db_conn
from ..settings import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/sign_in/',
    auto_error=False
)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme)
) -> BasicUser:
    if not token:
        return None

    return AuthService.validate_token(token)


class AuthService:
    def __init__(
        self,
        db_connection: Connection = Depends(get_db_conn)
    ) -> None:
        self.db_conn = db_connection
    
    async def sign_up(
        self,
        create_user: UserSignUp
    ) -> Token:
        hashed_password = self.hash_password(
            plain_password=create_user.password
        )

        try:
            user_record = await self.db_conn.fetchrow(
                f"""
                    INSERT INTO users
                    (
                        first_name,
                        last_name,
                        email,
                        password
                    )
                    VALUES
                    (
                        '{create_user.first_name}',
                        '{create_user.last_name}',
                        '{create_user.email}',
                        '{hashed_password}'
                    )
                    RETURNING 
                            id,
                            first_name,
                            last_name,
                            email
                """
            )
        except UniqueViolationError:
            raise HTTPException(
                status_code=409,
                detail="?????????????????? email ?????? ????????????????????????"
            )
        
        user_dict = dict(user_record) | {"scopes": []}

        return self.create_token(user_dict)

    async def sign_in(
        self,
        user_data: UserSignIn
    ) -> Token:
        user_record = await self.db_conn.fetchrow(
            f"""
                SELECT 
                     users.id,
                     users.first_name,
                     users.last_name,
                     '{user_data.email}' AS email,
                     superusers.scopes
                FROM
                     users
                LEFT JOIN 
                        superusers
                     ON
                        superusers.user_id = users.id
                WHERE
                     users.email = '{user_data.email}'
            """
        )

        if not user_record:
            raise HTTPException(
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"}
            )

        return self.create_token(
            user_data=dict(user_record)
        )
        
    @staticmethod
    def create_token(
        user_data: dict
    ) -> Token:
        """?????????????? access token"""

        now = datetime.utcnow()
        payload = {
            "exp": now + timedelta(settings.jwt_expires),
            "user": user_data
        }

        token = jwt.encode(
            claims=payload,
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )

        return Token(
            access_token=token
        )

    @staticmethod
    def validate_token(
        token: str
    ) -> BasicUser:
        """
            ???????????????????? ?????????? ?? ???????????????????? ???? ???????? ????????????
            ?? ????????????????????????
        """

        try:
            payload = jwt.decode(
                token=token,
                key=settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )

            user = BasicUser.parse_obj(
                payload.get('user')
            )    
        except (JWTError, ValidationError) as e:
            print(e)
            raise HTTPException(
                status_code=401,
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except ExpiredSignatureError:
            pass

        return user
    
    @staticmethod
    def verify_password(
        plain_password: str | bytes,
        hashed_password: str | bytes
    ) -> bool:
        """ ???????????????????????? ???????????? """
        return bcrypt.verify(
            plain_password, hashed_password
        )
    
    @staticmethod
    def hash_password(
        plain_password: str | bytes
    ) -> str:
        """ ???????????????????? ?????? ???????????? """
        return bcrypt.hash(plain_password)