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
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
                scopes INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(128) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS products_updates (
                product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
                created_by INTEGER REFERENCES superusers(user_id) ON DELETE CASCADE,
                description TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT 'now'
            );
            CREATE TABLE IF NOT EXISTS users_wishlist_products (
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                product_id INTEGER REFERENCES products(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS users_cart_products (
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                product_id INTEGER REFERENCES products(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS users_counts (
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                cart_products_count INTEGER DEFAULT 0,
                wishlist_products_count INTEGER DEFAULT 0
            )
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
                        users.id = user_id
                    LIMIT 1;
                END; 
            $$ LANGUAGE plpgsql;

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
                        products.id = product_id
                    LIMIT 1;
                END;
            $$ LANGUAGE plpgsql;


            CREATE OR REPLACE FUNCTION create_user_count()
            RETURNS TRIGGER AS $$
                BEGIN
                    INSERT INTO users_counts
                    (user_id)
                    VALUES
                    (NEW.id);

                    RETURN NEW;
                END;
            $$ LANGUAGE plpgsql;


            CREATE CONSTRAINT TRIGGER create_user_count_dep
            AFTER INSERT ON users
            DEFERRABLE INITIALLY DEFERRED
            FOR EACH ROW EXECUTE PROCEDURE create_user_count(); 

            
            CREATE OR REPLACE FUNCTION user_count()
            RETURNS TRIGGER AS $$
                BEGIN
                    IF TG_OP = 'INSERT' THEN

                        IF TG_NAME = 'user_cart_count_mod' THEN
                            UPDATE
                                users_counts
                            SET
                                cart_products_count = cart_products_count + 1
                            WHERE
                                user_id = NEW.user_id;

                        ELSIF TG_NAME = 'user_wishlist_count_mod' THEN
                            UPDATE
                                users_counts
                            SET
                                wishlist_products_count = wishlist_products_count + 1
                            WHERE
                                user_id = NEW.user_id;

                        END IF;

                        RETURN NEW;

                    ELSIF TG_OP = 'DELETE' THEN

                        IF TG_NAME = 'user_cart_count_mod' THEN
                            UPDATE
                                users_counts
                            SET
                                cart_products_count = cart_products_count - 1
                            WHERE
                                user_id = OLD.user_id;

                        ELSIF TG_NAME = 'user_wishlist_count_mod' THEN
                            UPDATE
                                users_counts
                            SET
                                wishlist_products_count = wishlist_products_count - 1
                            WHERE
                                user_id = OLD.user_id;
                        
                        END IF;
                        
                        RETURN OLD;

                    END IF;
                END;
            $$ LANGUAGE plpgsql;

            CREATE CONSTRAINT TRIGGER user_cart_count_mod
            AFTER INSERT OR DELETE ON users_cart_products
            DEFERRABLE INITIALLY DEFERRED
            FOR EACH ROW EXECUTE PROCEDURE user_count();

            CREATE CONSTRAINT TRIGGER user_wishlist_count_mod
            AFTER INSERT OR DELETE ON users_wishlist_products
            DEFERRABLE INITIALLY DEFERRED
            FOR EACH ROW EXECUTE PROCEDURE user_count();
        """
    )


if __name__ == "__main__":
    async def create_tables_and_functions():
        await create_tables()
        await create_functions()

    asyncio.run(create_tables_and_functions())