from telethon import TelegramClient, events, helpers
from helpers import readChannels, readEnvVars


API_ID    = readEnvVars.ReadEnvVar("API_ID")
API_HASH  = readEnvVars.ReadEnvVar("API_HASH")



client = TelegramClient("catcher", API_ID, API_HASH)



@client.on(events.NewMessage)
async def message_handler(event):
    print("message is: " , event.text)


with client:
    print("running...")
    client.run_until_disconnected()