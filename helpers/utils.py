from .tools import *
from db import queries

# a query to insert data to database
async def add_product(dbInstance, *args):
    data = await dbInstance.execute_query("""
        INSERT INTO products(price_toman, channel, message_id, details, post_link) VALUES(
                $1,$2,$3,$4,$5           
            ) RETURNING id
    """,
    *args)
    return data


# extracting and saving the website links related to a product
async def extract_website_address(dbInstance, text, productId):
    urlRegex = r"(?:https?:\/\/)?(?!t\.me\b)(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?"

    urls = re.findall(urlRegex, text, re.IGNORECASE)

    for url in urls:
        websiteId = await dbInstance.execute_query(queries.insert_to_website_query, url)
        await dbInstance.execute_query(queries.insert_to_website_junction_query, productId, websiteId)

# extracting and saving the phone numbers related to a product
async def extract_phone_numbers(dbInstance, text, productId):
    phoneRegex =  r"(?:\+98|0098|0)?(?:9\d{9}|(?:21|26|25|24|23|28|31|34|35|38|41|44|74|45|51|84|54|56|58|61|66|71|76|13|77|81|83|86|87|11|17)[-_]?\d{8})"

    phone_numbers = re.findall(phoneRegex, text)

    for phone_number in phone_numbers:
        phoneNumberId = await dbInstance.execute_query(queries.insert_to_phone_numbers_query, phone_number)
        await dbInstance.execute_query(queries.insert_to_phone_numbers_junction_query, productId, phoneNumberId)



# fetch products by date filter
async def get_report_by_date(dbInstance, date, comparison_operator):
    products = await dbInstance.fetch_product_by_date(date, comparison_operator)
    
    if not products:
        return generate_error(date)

    filepath = create_csv_file(products)

    return filepath

# fetch products by channel filter
async def get_report_by_channel(dbInstance, channel):
    products = await dbInstance.fetch_product_by_channel(channel)

    if not products:
        return generate_error(channel)

    filepath = create_csv_file(products)


    return filepath
