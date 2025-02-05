from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest, GetChannelRecommendationsRequest
from helpers import messageParser, tools
from db.main import Database
import asyncio
import os

# reading telegram API credentials
API_ID    = tools.ReadEnvVar("API_ID")
API_HASH  = tools.ReadEnvVar("API_HASH")





async def main():
    
    # getting an instance of Database class
    DB = Database()

    # initializing the database
    await DB.init_db()  
    
    # creating an instance of telegram client
    client = TelegramClient("catcher", API_ID, API_HASH)

    # getting file path
    path = input("Please enter the path to the .txt file containing channels' usernames (each line one username): ")
    # get channels id's that user entered to join
    channels = tools.GetChannelsId(path)

    # if channels list was empty
    if not channels:
        return

    async with client:
        
        
        # looping through channels to join
        for id in channels:
            try:
                # joining channels requested
                await client(JoinChannelRequest(id))   
            # if id not found
            except ValueError:
                # removing it from cannels list to prevent further errors
                channels.remove(id)
                print(f"{id}, channel not found.".replace("\n", ""))
                continue
        
        
        # listening for new messages
        print(channels)
        @client.on(events.NewMessage(chats=channels))
        async def message_handler(event):
            print("ran")
            prices = messageParser.parse_message(event.text)

            if prices:
                for price in prices:
                    channel_username = event.chat.username
                    message_id = event.id
                    # creating a link for each new message
                    post_link = tools.make_post_link(channel_username, message_id)
                    productId = await tools.add_product(DB, price["price"], channel_username, message_id, price["details"], post_link)
                    await tools.extract_website_address(DB, event.text, productId)
                    await tools.extract_phone_numbers(DB, event.text, productId)

        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
