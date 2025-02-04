import os
import re
from dotenv import load_dotenv
from telethon.tl.functions.channels import GetChannelRecommendationsRequest
from emoji import replace_emoji

# opening a file to read the channels' username
def GetChannelsId(fileName: str):
    file = open(fileName, "r")
    channelIds = file.readlines()

    return channelIds


load_dotenv()

def ReadEnvVar(name: str):
    value = os.getenv(name)

    return value


async def GetSimilarChannels(client, channel_id: str):

    result = await client(GetChannelRecommendationsRequest(channel_id))

# a query to insert data to database
async def add_data(dbInstance, *args):
    await dbInstance.execute_query("""
        INSERT INTO data(price_toman, channel, message_id, details, post_link) VALUES(
                $1,$2,$3,$4,$5           
            )
    """,
    *args)

# remove emojis and : in a string
def clean_text(text):
    text = replace_emoji(text, "")
    text = text.replace(":", "")

    return text



# converts Persian numbers to English numbers
def convert_numbers(text: str):
    persian_characters = "۰۱۲۳۴۵۶۷۸۹٫"
    english_characters = "0123456789,"
    # creating a translation table to translate strings
    translator     = str.maketrans(persian_characters, english_characters)
    return text.translate(translator)




def extract_details(text: str):
    detailsRegex = r"\b(?:\d{1,3}(?:,\d{3})*|\d+|[\u06F0-\u06F9]+)\s*(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|معامله|خرید|فروش|IRR|IRT|میلیون تومان|میلیون ریال|هزار تومان|هزار ریال)|" \
            r"(?:تومان|ریال|Toman|Rials|Price|قیمت|تومن|\$|buy|sell|معامله|خرید|فروش|IRR|IRT|میلیون تومان|میلیون ریال|هزار تومان|هزار ریال)\s*(?:\d{1,3}(?:,\d{3})*|\d+|[\u06F0-\u06F9]+)\b |" \
            r"\b\d{1,3}(?:,\d{3})+\b|" \
            r"\b\d{5,}\b"
    
    # finding currency and price (the numbers)
    matchCase = re.findall(detailsRegex, text)[0]
    # keeping everything except price and currency
    details = text.replace(matchCase, "")
    # removing extra spaces at end and start of string
    details = clean_text(details).strip()
    # returnig details extracted and currecy with price
    return details, matchCase


# a helpers function to make the link of posts of channels
def make_post_link(channel_username, message_id):
    return f"https://t.me/{channel_username}/{message_id}"