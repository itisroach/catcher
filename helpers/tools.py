import os
import re
from dotenv import load_dotenv
from telethon.tl.functions.channels import GetChannelRecommendationsRequest
from emoji import replace_emoji
import csv

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


def human_readable_time(timestamp):
    human_readable = timestamp.strftime("%A, %B %d, %Y at %I:%M %p")

    return human_readable


def create_csv_file(products):
    try:
        with open("report.csv", "w+", newline='', encoding="utf-8-sig") as csvfile:
            fieldnames = ["date", "channel", "details", "price", "post link", "other links", "phone numbers"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            
            for product in products:
                writer.writerow([
                    human_readable_time(product["time"]),  
                    f'@{product["channel"]}',  
                    product["details"],  
                    f'{product["price_toman"]:,}',  
                    product["post_link"],  
                    product["website_links"], 
                    product["phone_numbers"]
            ])
            return csvfile.name
    except:
        return False



def is_date(text):
    date_regex = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'

    if re.match(date_regex, text):
        return True
    
    return False

def generate_error(value):
    return f"not found any rows by value {value}"