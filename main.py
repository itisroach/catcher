from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest, GetChannelRecommendationsRequest
from helpers import messageParser, tools, utils
from db.main import Database
import asyncio
from datetime import datetime
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
        
        # getting account credentials
        me = await client.get_me()
        # appending saved message to channels list to listen for new messages on it
        channels.append(me.id)

        # listening for new messages
        @client.on(events.NewMessage(chats=channels))
        async def message_handler(event):
            if event.chat.id == me.id:
                # spliting commands to list
                commands = event.text.split(" ")

                filepath = None
                # if only report sent
                if len(commands) == 1 and commands[0] == "report":
                    await client.send_message('me', "you can send `report {channel username}` to get channel's report or date like `report {date(like 2025-02-23)}` to get the day report")
                
                # report command says to find rows by date specified
                elif commands[0] == "report" and tools.is_date(commands[1]):
                    # creating date time object to pass to db query
                    date_object = datetime.strptime(commands[1], "%Y-%m-%d").date()
                    
                    comp_operator = "equal"
                    if len(commands) == 3 and commands[2] in ["greater", "less"]:
                        comp_operator = commands[2]

                    filepath = await utils.get_report_by_date(DB, date_object, comp_operator)

                # report command says to find rows by channel name specified
                elif commands[0] == "report" and commands[1]:
                    filepath = await utils.get_report_by_channel(DB, commands[1])
                
                # if file created send it to me(saved message) 
                if filepath and "not found" not in filepath:
                    await client.send_file("me", filepath)
                    # removing file from server
                    os.remove(filepath)

                # if query returned 0 rows 
                elif filepath and "not found" in filepath:
                    await client.send_message("me", filepath)

                # if error occured in those functions
                elif filepath == False:
                    await client.send_message('me', )

               
                
            else:
                prices = messageParser.parse_message(event.text)

                if prices:
                    for price in prices:
                        channel_username = event.chat.username
                        message_id = event.id
                        # creating a link for each new message
                        post_link = tools.make_post_link(channel_username, message_id)
                        productId = await utils.add_product(DB, price["price"], channel_username, message_id, price["details"], post_link)
                        await utils.extract_website_address(DB, event.text, productId)
                        await utils.extract_phone_numbers(DB, event.text, productId)

        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
