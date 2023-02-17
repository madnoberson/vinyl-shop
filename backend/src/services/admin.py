from fastapi import HTTPException, Depends
from asyncpg import Connection

from ..schemas.admin import Token

from ..database import get_db_conn
    

class AdminService:
    def __init__(
        self,
        db_connection: Connection = Depends(get_db_conn)
    ) -> None:
        self.db_conn = db_connection
    
    