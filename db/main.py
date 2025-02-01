import asyncpg
import asyncio
from helpers.tools import ReadEnvVar

DBConfig = {
    "user": ReadEnvVar("DB_USER"),
    "password": ReadEnvVar("DB_PASS"),
    "host": ReadEnvVar("DB_ADDR"),
    "database": ReadEnvVar("DB_NAME")
}


class Database():

    def __init__(self):
        self.pool = None


    async def init_db(self):
        self.pool = await asyncpg.create_pool(**DBConfig)

        await self.pool.execute(
            '''CREATE TABLE IF NOT EXISTS data (
                id              SERIAL PRIMARY KEY,
                price           BIGINT NOT NULL,
                currency        
                time            timestamp DEFAULT current_timestamp,
                channel         VARCHAR(256) NOT NULL,
                message_id      BIGINT NOT NULL UNIQUE
            )'''
        )


        await self.pool.execute("""
            CREATE INDEX IF NOT EXISTS idx_channel ON channel;
        """)
        await self.pool.execute("""
            CREATE INDEX IF NOT EXISTS idx_message_id ON message_id;
        """)
        await self.pool.execute("""
            CREATE INDEX IF NOT EXISTS idx_price ON price;
        """)

    # executing queries like UPDATE, INSERT, DELETE
    async def execute_query(self, query):
        async with self.pool.acquire() as connection:
            return await connection.execute(query)
        
    # fetching one row 
    async def fetch_one_row(self, query):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query)

    # fething multiple rows
    async def fetch_rows(self, query):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query)

    async def close_connection(self):
        await self.pool.close()