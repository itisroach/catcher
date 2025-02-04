
create_products_table = '''
    CREATE TABLE IF NOT EXISTS products (
        id              SERIAL PRIMARY KEY,
        price_toman     BIGINT NOT NULL,
        time            timestamp DEFAULT current_timestamp,
        channel         VARCHAR(256) NOT NULL,
        details         TEXT,
        post_link       TEXT NOT NULL,
        message_id      BIGINT NOT NULL
    )
'''


create_websites_table = '''
    CREATE TABLE IF NOT EXISTS websites (
        id       SERIAL PRIMARY KEY,
        link     TEXT   NOT NULL,
        product  INTEGER NOT NULL,
        CONSTRAINT fK_websites_product
            FOREIGN KEY(product)
            REFRENCES products(id)
    )
'''

create_phone_numbers_table = '''
    CREATE TABLE IF NOT EXISTS phone_numbers (
        id              SERIAL PRIMARY KEY,
        phone_number    TEXT   NOT NULL,
        product  INTEGER NOT NULL,
        CONSTRAINT fK_websites_product
            FOREIGN KEY(product)
            REFRENCES products(id)
    )
'''


fetch_products_query = '''
    SELECT 
        p.id,
        p.price_toman,
        p.time,
        p.channel,
        p.details,
        p.post_link,
        p.message_id,
        w.link AS website_link
    FROM products p
    LEFT JOIN websites w ON p.id = w.product
'''

fetch_product_by_channel_query = '''
    SELECT 
        p.id,
        p.price_toman,
        p.time,
        p.channel,
        p.details,
        p.post_link,
        p.message_id,
        w.link AS website_link
    FROM products p
    LEFT JOIN websites w ON p.id = w.product
    WHERE p.channel = $1 
'''