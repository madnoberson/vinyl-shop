import asyncpg
from asyncpg import Connection


async def get_db_conn() -> Connection:
    db_conn = await asyncpg.connect(
        "postgres://postgres:1234@localhost/vinyl"
    )

    try:
        yield db_conn
    finally:
        await db_conn.close()

