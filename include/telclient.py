#!/usr/bin/python3

# Copyright 2021 Anibal Cañada


# Blab is a telegram bot that recovers data leaks and allows users to search it is affected

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
from telethon import TelegramClient
from dotenv import load_dotenv
import os

#VARIABLES
load_dotenv()
API_ID=os.getenv('API_ID')
API_HASH=os.getenv('API_HASH')
client = TelegramClient('blablablabla', API_ID, API_HASH)

async def telclient() :
   # Getting information about yourself
   me = await client.get_me ()

   # "me" is a user object. You can pretty-print
   # any Telegram object with the "stringify" method:
   print (me.stringify ())


   # Sending a message returns the sent message object, which you can use
   print (message.raw_text)

   # You can reply to messages directly if you have a message object
   await message.reply ('Cool!')


   # You can print the message history of any chat:
   async for message in client.iter_messages ('me') :
      print (message.id, message.text)


with client :
   client.loop.run_until_complete (telclient())