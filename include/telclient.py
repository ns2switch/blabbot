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

import os
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events

# VARIABLES
load_dotenv ()
API_ID = os.getenv ('API_ID')
API_HASH = os.getenv ('API_HASH')
client = TelegramClient ('Anonblab', API_ID, API_HASH)

class telclient():
	print('client')
	async def teldat() :
		# Getting information about yourself
		me = await client.get_me ()
		# "me" is a user object. You can pretty-print
		# any Telegram object with the "stringify" method:
		print (me.stringify ())
		message = await client.send_message (
			'me',
			'a [nice website](https://google.com)!',
			link_preview=True
		)
		await message.reply ('Cool!')
		# You can print the message history of any chat:
		async for message in client.iter_messages ('me') :
			print (message.id, message.text)


	@client.on (events.NewMessage (outgoing=False))
	async def incoming_message(event) :
		newMessage = event.message.message
		FullMessage = event.message
		time = datetime.now ().strftime ("%d-%m-%Y %H:%M:%S")
		print ("====================================== " + time)
		print (newMessage)
		if newMessage == 'hola' :
			await client.send_message (FullMessage.from_id, 'hola')
		elif newMessage == 'hi':
			await client.send_message (FullMessage.from_id, 'hi')
		else :
			await client.send_message (FullMessage.from_id, newMessage)
	with client:
		client.run_until_disconnected()
