
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
        link     TEXT   NOT NULL
    )
'''

create_phone_numbers_table = '''
    CREATE TABLE IF NOT EXISTS phone_numbers (
        id              SERIAL PRIMARY KEY,
        phone_number    TEXT   NOT NULL
    )
'''


create_website_junction_table = '''
    CREATE TABLE IF NOT EXISTS products_websites (
        product_id      INT REFERENCES products(id) ON DELETE CASCADE,
        website_id      INT REFERENCES websites(id) ON DELETE CASCADE,
        PRIMARY KEY (product_id, website_id)
    ) 
'''


create_phone_numbers_junction_table = '''
    CREATE TABLE IF NOT EXISTS products_phone_numbers (
        product_id           INT REFERENCES products(id) ON DELETE CASCADE,
        phone_number_id      INT REFERENCES phone_numbers(id) ON DELETE CASCADE,
        PRIMARY KEY (product_id, phone_number_id)
    ) 
'''


base_fetch_products = '''
    SELECT 
        p.id,
        p.price_toman,
        p.time,
        p.channel,
        p.details,
        p.post_link,
        p.message_id,
        COALESCE(STRING_AGG(DISTINCT w.link, ', '), 'No Website') AS website_links,
        COALESCE(STRING_AGG(DISTINCT ph.phone_number, ', '), 'No Phone Number') AS phone_numbers
    FROM products p
    LEFT JOIN products_websites pw ON p.id = pw.product_id
    LEFT JOIN websites w ON pw.website_id = w.id
    LEFT JOIN products_phone_numbers ppn ON p.id = ppn.product_id
    LEFT JOIN phone_numbers ph ON ppn.phone_number_id = ph.id
'''

fetch_products_query = base_fetch_products+ ' GROUP BY p.id'

fetch_product_by_channel_query = base_fetch_products+ '''
    WHERE p.channel = $1 
    GROUP BY p.id
'''

insert_to_phone_numbers_query = '''
    INSERT INTO phone_numbers (phone_number) VALUES ($1) RETURNING id
'''


insert_to_phone_numbers_junction_query = '''
    INSERT INTO products_phone_numbers(product_id, phone_number_id) VALUES ($1, $2)
'''

insert_to_website_query = '''
    INSERT INTO websites (link) VALUES ($1) RETURNING id
'''

insert_to_website_junction_query = '''
    INSERT INTO products_websites(product_id, website_id) VALUES ($1, $2)
'''




fetch_products_by_date_equal_query = base_fetch_products + """
    WHERE p.time::date = $1::date
    GROUP BY p.id
"""




fetch_products_by_date_greater_query = base_fetch_products + """
    WHERE p.time::date >= $1::date
    GROUP BY p.id
"""

fetch_products_by_date_less_query = base_fetch_products + """
    WHERE p.time::date <= $1::date
    GROUP BY p.id
"""