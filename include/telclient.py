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
from telethon import TelegramClient, events,types
from .telbot  import *
from .dynamo import blabdynamo
from .helpers import date_format, to_json

# VARIABLES
load_dotenv ()
API_ID = os.getenv ('API_ID')
API_HASH = os.getenv ('API_HASH')
ADMIN_ID = os.getenv('ADMIN_ID')
client = TelegramClient ('Anonblab', API_ID, API_HASH)

class telclient():
	print('client')
	async def teldat() :
		# Getting information about yourself
		me = await client.get_me ()
		print (me.stringify ())
		async for message in client.iter_messages ('me') :
			print (message.id, message.text)


	@client.on (events.NewMessage (outgoing=False))

	async def incoming_message(event) :
		dyn = blabdynamo()
		newMessage = event.message.message
		FullMessage = event.message # complete message
		sender = event.sender_id
		fullsender = await client.get_entity (sender)
		senderstr = str (event.sender_id)
		time = date_format(datetime.now())
		if isinstance (FullMessage.peer_id, (types.PeerChannel, types.PeerChat)):
			channel = FullMessage.peer_id
			fullchan = await client.get_entity (channel)
			print(to_json(FullMessage))
			dyn.save(to_json(FullMessage))
			print ("user: " + str (fullsender.username) + " Channel: " + str(fullchan.title) + " time: " + str(time))
			print(FullMessage.message)
			if FullMessage.mentioned:
				await client.send_message(channel, "I am away.Let your message, when listen 'Beep'")
		else:
			print ("user: " + str(fullsender.username) + " at " + str(time))
			print (newMessage)
			if senderstr == ADMIN_ID:
				await botcommand.BotMode(FullMessage,event.sender_id,client)
			elif newMessage == 'hi' :
				await client.send_message (FullMessage.peer_id, 'hi')
			elif newMessage == '/start':
				await client.send_message (FullMessage.from_id, 'You are not an authorized user')
			else :
				pass

	with client:
		client.run_until_disconnected()