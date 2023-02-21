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


class AdminService:
    def __init__(
        self,
        current_user: BasicUser = Depends(get_current_user),
        db_connection: Connection = Depends(get_db_conn)
    ) -> None:
        self.current_user = current_user
        self.db_conn = db_connection
    
    async def create_superuser(
        self,
        create_superuser: SuperUserIn
    ):
        if not self.current_user or \
            (self.current_user and not 'admin' in self.current_user.scopes):
            raise HTTPException(404)

        superuser_record = await self.db_conn.fetchrow(
            f"""
                WITH scopes_row AS (
                    INSERT INTO superusers 
                    (
                        user_id,
                        scopes
                    )
                    VALUES
                    (
                        {create_superuser.user_id},
                        {create_superuser.scopes}
                    )
                    RETURNING scopes
                )
                SELECT
                      scopes,
                      users.*
                FROM
                      scopes_row
                JOIN
                      get_basic_user({create_superuser.user_id})
            """
        )

        return 