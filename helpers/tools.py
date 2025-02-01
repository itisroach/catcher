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

    print(result)