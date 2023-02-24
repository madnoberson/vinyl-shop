import asyncio
import asyncpg


async def clean_up_db() -> None:
    db_conn = await asyncpg.connect(
        "postgres://postgres:1234@localhost/vinyl"
    )

    await db_conn.execute(
        """
            DROP TABLE IF EXISTS 
                                users,
                                superusers,
                                products,
                                products_update,
                                users_wishes
                                CASCADE;
            DROP SEQUENCE IF EXISTS
                                   products,
                                   users
                                   CASCADE;
        """
    )


if __name__ == "__main__":
    asyncio.run(clean_up_db())