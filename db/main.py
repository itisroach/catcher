import asyncpg
import asyncio


async def run_db():
    # creating a connection
    conne = await asyncpg.connect(user="postgres",database="postgres",password="amirali3362", host="127.0.0.1")

    # creating table for storing data in it
    await conne.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id              SERIAL PRIMARY KEY,
            price_rial      BIGINT NOT NULL,
            price_toman     BIGINT NOT NULL,
            time            timestamp DEFAULT current_timestamp,
            channel         VARCHAR(256) NOT NULL,
            message_id      BIGINT NOT NULL UNIQUE
        )

    ''')


    await conne.close()