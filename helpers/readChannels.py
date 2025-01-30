
# opening a file to read the channels' username
def GetChannelsId(fileName: str):
    file = open(fileName, "r")
    channelIds = file.readlines()

    return channelIds