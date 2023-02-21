import asyncio
import asyncpg


async def create_tables() -> None:
    db_conn = await asyncpg.connect(
        "postgres://postgres:1234@localhost/vinyl"
    )

    await db_conn.execute(
        """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(256) NOT NULL UNIQUE,
                first_name VARCHAR(32) NOT NULL,
                last_name VARCHAR(32) NOT NULL,
                password VARCHAR(256) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS superusers (
                user_id INTEGER REFERENCES users (id) UNIQUE,
                scopes INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(128) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS products_updates (
                product_id INTEGER REFERENCES products (id),
                created_by INTEGER REFERENCES superusers (user_id),
                description TEXT NOT NULL,
                datetime TIMESTAMP NOT NULL DEFAULT 'now'
            );
        """
    )


async def create_functions() -> None:
    db_conn = await asyncpg.connect(
        "postgres://postgres:1234@localhost/vinyl"
    )

    await db_conn.execute(
        """
            CREATE OR REPLACE FUNCTION get_basic_user(user_id integer)
            RETURNS TABLE (
                id INTEGER,
                first_name VARCHAR,
                lastname VARCHAR,
                email VARCHAR
            ) AS $$
            BEGIN
                RETURN QUERY
                SELECT
                    users.id,
                    users.first_name,
                    users.last_name,
                    users.email
                FROM
                    users
                WHERE
                    users.id = user_id;
            END; $$
            LANGUAGE plpgsql;


            CREATE OR REPLACE FUNCTION get_basic_product(product_id integer)
            RETURNS TABLE (
                id INTEGER,
                name VARCHAR
            ) AS $$ 
            BEGIN
                RETURN QUERY
                SELECT 
                    products.id,
                    products.name
                FROM
                    products
                WHERE 
                    products.id = product_id;
            END; $$
            LANGUAGE plpgsql;
        """
    )


if __name__ == "__main__":
    async def create_tables_and_functions():
        await create_tables()
        await create_functions()

    asyncio.run(create_tables_and_functions())