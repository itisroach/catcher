import asyncpg
import asyncio
from helpers.tools import ReadEnvVar
from .queries import *

DBConfig = {
    "user": ReadEnvVar("DB_USER"),
    "password": ReadEnvVar("DB_PASS"),
    "host": ReadEnvVar("DB_ADDR"),
    "database": ReadEnvVar("DB_NAME"),
    "server_settings": {"client_encoding": "UTF8"} 
}




class Database():

    def __init__(self):
        self.pool = None


    async def init_db(self):
        self.pool = await asyncpg.create_pool(**DBConfig)
        # crating a table for storing all products
        await self.pool.execute(create_products_table)

        # crating a table for storing products' websites (links)
        await self.pool.execute(create_websites_table)
        # crating a junction table for storing relation between products and websites table
        await self.pool.execute(create_website_junction_table)
        # crating a table for storing products' phone numbers
        await self.pool.execute(create_phone_numbers_table)
        # crating a junction table for storing relation between products and phone_numbers table
        await self.pool.execute(create_phone_numbers_junction_table)

        # creating indexes for most accessable columns
        await self.pool.execute("""
            CREATE INDEX IF NOT EXISTS idx_channel ON products(channel)
        """)
        await self.pool.execute("""
            CREATE INDEX IF NOT EXISTS idx_message_id ON products(message_id)
        """)
        await self.pool.execute("""
            CREATE INDEX IF NOT EXISTS idx_price ON products(price_toman)
        """)

    # executing queries like UPDATE, INSERT, DELETE
    async def execute_query(self, query, *args):
        async with self.pool.acquire() as connection:
            # using fetchval to return the value specified the RETURNING statement
            return await connection.fetchval(query, *args)
        
    # fetching one row 
    async def fetch_one_row(self, query):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query)

    # fething multiple rows
    async def fetch_rows(self, query):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query)

    # fetch all products
    async def fetch_products(self):
        async with self.pool.acquire() as connection:
            return await connection.fetch(fetch_products_query)

    # fetch a products by its channel username
    async def fetch_product_by_channel(self, channel: str):
        async with self.pool.acquire() as connection:
            return await connection.fetch(fetch_product_by_channel_query, channel)

    async def close_connection(self):
        await self.pool.close()