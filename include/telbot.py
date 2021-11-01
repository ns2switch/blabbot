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
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv

#VARIABLES
load_dotenv()
TOKEN=os.getenv('TELEGRAM_TOKEN')
API_ID=os.getenv('API_ID')
API_HASH=os.getenv('API_HASH')

bot = TelegramClient('BlabBlabBot', API_ID, API_HASH).start(bot_token=TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hi!')
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def echo(event):
    """Echo the user message."""
    await event.respond(event.text)

bot.run_until_disconnected()