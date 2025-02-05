import os
import re
from dotenv import load_dotenv
from telethon.tl.functions.channels import GetChannelRecommendationsRequest
from emoji import replace_emoji
from db import queries

# opening a file to read the channels' username
def GetChannelsId(fileName: str):
    # if file extension is not .txt
    if not fileName.lower().endswith(".txt"):
        print("only .txt file allowed")
        return
    try:
        file = open(fileName, "r")
        channelIds = file.readlines()
        return channelIds
    except FileNotFoundError:
        print("file not found")
        return


load_dotenv()

def ReadEnvVar(name: str):
    value = os.getenv(name)

    return value


async def GetSimilarChannels(client, channel_id: str):

    result = await client(GetChannelRecommendationsRequest(channel_id))

# a query to insert data to database
async def add_product(dbInstance, *args):
    data = await dbInstance.execute_query("""
        INSERT INTO products(price_toman, channel, message_id, details, post_link) VALUES(
                $1,$2,$3,$4,$5           
            ) RETURNING id
    """,
    *args)
    return data

# remove emojis and : in a string
def clean_text(text):
    text = replace_emoji(text, "")
    text = text.replace(":", "")
    text = text.replace("-", "")
    text = text.replace(",", "")
    text = text.replace(".", "")
    text.strip()
    return text



# converts Persian numbers to English numbers
def convert_numbers(text: str):
    persian_characters = "۰۱۲۳۴۵۶۷۸۹٫"
    english_characters = "0123456789,"
    # creating a translation table to translate strings
    translator     = str.maketrans(persian_characters, english_characters)
    return clean_text(text.translate(translator))




def extract_details(text: str):
    detailsRegex = r"\b(?:\d{1,3}(?:,\d{3})*|\d+|[\u06F0-\u06F9]+)\s*(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|معامله|خرید|فروش|IRR|IRT|میلیون تومان|میلیون ریال|هزار تومان|هزار ریال)|" \
            r"(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|معامله|خرید|فروش|IRR|IRT|میلیون تومان|میلیون ریال|هزار تومان|هزار ریال)\s*(?:\d{1,3}(?:,\d{3})*|\d+|[\u06F0-\u06F9]+)\b |" \
            r"\b(?![0+-])\d{5,}\b|"\
            r"https?:\/\/(?!t\.me\b)(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b[-a-zA-Z0-9@:%_\+.~#?&//=]*|"\
            r"(?:\+98|0098|0)?(?:9\d{9}|(?:21|26|25|24|23|28|31|34|35|38|41|44|74|45|51|84|54|56|58|61|66|71|76|13|77|81|83|86|87|11|17)[-_]?\d{8})"
    
    # finding currency and price (the numbers)
    matchCase = re.findall(detailsRegex, text)[0]
    
    # keeping everything except price and currency
    details = text.replace(matchCase, "")
    # returnig details extracted and currecy with price
    return details, matchCase


# a helpers function to make the link of posts of channels
def make_post_link(channel_username, message_id) -> str:
    return f"https://t.me/{channel_username}/{message_id}"



async def extract_website_address(dbInstance, text, productId):
    urlRegex = r"(?:https?:\/\/)?(?!t\.me\b)(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?"

    urls = re.findall(urlRegex, text, re.IGNORECASE)

    for url in urls:
        websiteId = await dbInstance.execute_query(queries.insert_to_website_query, url)
        await dbInstance.execute_query(queries.insert_to_website_junction_query, productId, websiteId)


async def extract_phone_numbers(dbInstance, text, productId):
    phoneRegex =  r"(?:\+98|0098|0)?(?:9\d{9}|(?:21|26|25|24|23|28|31|34|35|38|41|44|74|45|51|84|54|56|58|61|66|71|76|13|77|81|83|86|87|11|17)[-_]?\d{8})"

    phone_numbers = re.findall(phoneRegex, text)

    for phone_number in phone_numbers:
        phoneNumberId = await dbInstance.execute_query(queries.insert_to_phone_numbers_query, phone_number)
        await dbInstance.execute_query(queries.insert_to_phone_numbers_junction_query, productId, phoneNumberId)