from fastapi import HTTPException, Depends
from asyncpg import Connection

from ..schemas.users import BasicUser
from ..schemas.admin import (
    SuperUser,
    SuperUserIn,
    SuperUserOut
)

from .auth import get_current_user
from ..database import get_db_conn


def scopes_required(scopes: list[str]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            service = args[0]
            current_user: BasicUser = service.current_user

            if not current_user:
                raise HTTPException(404)

            for scope in scopes:
                if scope not in current_user.scopes:
                    raise HTTPException(404)
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


class AdminService:
    def __init__(
        self,
        current_user: BasicUser = Depends(get_current_user),
        db_connection: Connection = Depends(get_db_conn)
    ) -> None:
        self.current_user = current_user
        self.db_conn = db_connection
    
    @scopes_required(scopes=['admin'])
    async def create_superuser(
        self,
        create_superuser: SuperUserIn
    ):
        user_record = await self.db_conn.fetchrow(
            f"""
                INSERT INTO superusers
                (
                    user_id,
                    scopes
                )
                VALUES
                (
                    {create_superuser.user_id},
                    {create_superuser.scopes}
                );
                SELECT *
                FROM get_basic_user({create_superuser.user_id})
            """
        )

        user = BasicUser.parse_obj(dict(user_record))
        superuser = SuperUser(
            user=user,
            scopes=create_superuser.scopes
        )

        return SuperUserOut(
            superuser=superuser
        )