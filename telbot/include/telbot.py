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
import json
from pprint import pprint
from dotenv import load_dotenv
from telethon.tl.functions.messages import ImportChatInviteRequest, GetHistoryRequest
from telethon.tl.functions.users import GetFullUserRequest
from .helpers import analyze_and_upload
from .storage.storage import s3bucket
from .dynamo import blabdynamo

# VARIABLES

load_dotenv ()
TOKEN = os.getenv ('TELEGRAM_TOKEN')
API_ID = os.getenv ('API_ID')
API_HASH = os.getenv ('API_HASH')
MIME_TYPES = json.loads(os.getenv('MIME_TYPES'))

class botcommand :

	def __init__(self, events) :
		self.events = events
		self.sender = sender
		self.FullMessage = FullMessage

	async def BotMode(FullMessage, sender, client) :
		dyn = blabdynamo ()
		# await client.send_message (sender, 'Hola amo!')
		if FullMessage.message == '/start' :
			await client.send_message (sender, 'Activado')

		elif '/infouser' in FullMessage.message :
			message = FullMessage.message.split ()
			user = message[1]
			full = await client (GetFullUserRequest (user))
			bio = full
			print (bio)

		elif '/joinpriv' in FullMessage.message :
			message = FullMessage.message.split ()
			hashed = message[1]
			hashed = hashed.replace ("https://t.me/+", "")
			chan = await client (ImportChatInviteRequest (hashed))
			chaninfo = chan.to_dict ()
			print (chaninfo)
			print (chaninfo['chats']['title'])
			print (chaninfo['chats']['id'])
			print (chaninfo['chats']['participants_count'])
			print (chaninfo['chats']['date'])


		elif '/joinpart' in FullMessage.message :
			async for dialog in client.iter_dialogs () :
				if dialog.id == chat_id :
					print (chat_id)
					await client.delete_dialog (chat_id)
			print_msg_time (f'{channel[1]} has been leaved')

		elif '/getmedia' in FullMessage.message :
			message = FullMessage.message.split ()
			channame = message[1]
			limited = int (message[2])
			channel = await client.get_entity (channame)
			mime = MIME_TYPES
			data = s3bucket ()
			prev_files = data.get_all_list_files ()
			'''getmessages = await client.get_messages(channel, limit= limited)'''
			for tipos in mime:
				async for message in client.iter_messages (channel,limit=limited) :
					if message.media:
						if message.file:
							if message.file.name not in prev_files:
								if tipos in message.file.mime_type :
									fileinfo = str(message.file.name) + " - " + str(message.file.mime_type)+" - "+ str(message.file.size)+' in bytes'
									await client.send_message(sender,fileinfo )
									await client.send_message(sender,'downloading....')
									path = await client.download_media (message.media, "../tmp")
									analyze_and_upload(path)
									await client.send_message (sender, 'analyzed and uploaded to S3')
				#else:
				#	await client.send_message (sender, 'no files found')



		elif '/whichchan' in FullMessage.message:
			message = FullMessage.message.split ()
			await client.send_message (sender, 'Currently monitoring: ')
			async for dialog in client.iter_dialogs () :
				if dialog.is_channel :
					dialog_total = str(dialog.entity.title) + ' - ' + str(dialog.entity.username)
					await client.send_message (sender, dialog_total)


		elif '/infochan' in FullMessage.message :
			message = FullMessage.message.split ()
			channame = message[1]
			channel = await client.get_entity (channame)
			await client.send_message (sender, channel.stringify())

		elif '/getdb' in FullMessage.message :
			answer = ''
			message = FullMessage.message.split ()
			patternkey = message[1]
			pattern = dyn.scan ('message', patternkey)
			for element in pattern :
				answer += str (element['date']) + " - " + str (element['user']) + " - " + str (
					element['channel']) + " - " + str (element['message'])
				if element['media'] :
					answer += " - " + element['media']['webpage']['url']
				answer += "\n"
			await client.send_message (sender, answer)

		elif '/processlink' in FullMessage.message :
			url = ''
			pattern = dyn.scan ('message', 'https')
			for element in pattern :
				if element['media'] :
					if element['media']['webpage']['url'] :
						url += element['media']['webpage']['url']
						url += "\n"
			await client.send_message (sender, url)

		elif '/allfiles' in FullMessage.message :
			message = FullMessage.message.split ()
			'''channame = message[1]'''
			data = s3bucket()
			filesdata = data.get_all_list_files()
			for filesx in filesdata:
				await client.send_message (sender, filesx)