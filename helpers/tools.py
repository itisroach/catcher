import os
from dotenv import load_dotenv
from telethon.tl.functions.channels import GetChannelRecommendationsRequest
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


async def add_data(dbInstance, *args):
    await dbInstance.execute_query("""
        INSERT INTO data(price_toman, channel, message_id) VALUES(
                $1,$2,$3                 
            )
    """,
    *args)