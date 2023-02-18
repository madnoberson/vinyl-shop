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


async def create_tables() -> None:
    db_conn = await get_db_conn()

    await db_conn.execute(
        """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(128) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS superusers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) NOT NULL,
                token TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS products_updates (
                product_id INTEGER REFERENCES products (id),
                created_by INTEGER REFERENCES superusers (id),
                description TEXT NOT NULL,
                datetime TIMESTAMP NOT NULL DEFAULT now
            );
        """
    )


async def create_functions() -> None:
    db_conn = await get_db_conn()

    await db_conn.execute(
        """
            CREATE OR REPLACE FUNCTION get_basic_product(product_id integer)
            RETURNS TABLE (
                products.id,
                products.name
            ) AS $$ 
            BEGIN
                SELECT products.id,
                       products.name
                FROM products
                WHERE products.id = product_id
            END; $$
            LANGUAGE sql;
        """
    )


async def clean_up_db() -> None:
    db_conn = await get_db_conn()

    await db_conn.execute(
        """
            DROP TABLE products
        """
    )


if __name__ == '__main__':
    import asyncio


    async def create_db() -> None:
        await create_tables()
        await create_functions()
    

    asyncio.run(create_db())