import os
import json

from dotenv import load_dotenv
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from .virustotal.vt import inform_file
from .dynamo import blabdynamo
from .helpers import analyze_and_upload
from .storage.storage import s3bucket



load_dotenv ()
TOKEN = os.getenv ('TELEGRAM_TOKEN')
API_ID = os.getenv ('API_ID')
API_HASH = os.getenv ('API_HASH')
MIME_TYPES = json.loads(os.getenv('MIME_TYPES'))
TABLE_CHAT=os.getenv('TABLE_CHAT')

async def help_commands(FullMessage,sender,client):
	message = "Todos los comandos llevan una / delante " + '\n'
	comandos = '/infouser + user - Imprime informacion sobre el usuario' + '\n'
	comandos += '/whichchan - Informacion de los canales monitorizados' + '\n'
	comandos += '/joinpriv + url_del_canal - Accede al canal' + '\n'
	comandos += '/part - Abandona el canal actual'+ '\n'
	comandos += '/getmedia canal cantidad - Descarga , analiza y sube al S3 bucket los archivos del canal' + '\n'
	comandos += '/inforchan canal - '+ '\n'
	comandos += '/getdb cadena - Busca en la base de datos de conversaciones la/s palabra/s en cadena' + '\n'
	comandos += 'processLink' + '\n'
	comandos +='allfiles'+ '\n'
	comand = message + comandos
	await client.send_message (sender, comand)

async def infouser_function(FullMessage, sender, client):
	message = FullMessage.message.split ()
	user = message[1]
	full = await client (GetFullUserRequest (user))
	bio = full
	print (bio)

async def join_priv_channel(FullMessage, sender, client):
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


async def which_channel_iam(FullMessage,sender,client):
	await client.send_message (sender, 'Currently monitoring: ')
	async for dialog in client.iter_dialogs () :
		if dialog.is_channel :
			dialog_total = str (dialog.entity.title) + ' - ' + str (dialog.entity.username)
			await client.send_message (sender, dialog_total)

async def part_channel(FullMessage,sender,client):
	async for dialog in client.iter_dialogs () :
		if dialog.is_channel :
			print (dialog.entity)
			await client.delete_dialog (dialog.entity)
	print(f'{dialog.entity} has been leaved')

async def info_channel(FullMessage,sender,client):
	message = FullMessage.message.split ()
	channame = message[1]
	channel = await client.get_entity (channame)
	await client.send_message (sender, channel.stringify ())

async def get_data_from_dinamo(FullMessage,sender,client):
	dyn = blabdynamo(TABLE_CHAT)
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

async def process_link_in_dynamo(FullMessage,sender,client):
	dyn = blabdynamo(TABLE_CHAT)
	url = ''
	pattern = dyn.scan ('message', 'https')
	for element in pattern :
		if element['media'] :
			if element['media']['webpage']['url'] :
				url += element['media']['webpage']['url']
				url += "\n"
	await client.send_message (sender, url)

async def list_all_files_in_s3(FullMessage,sender,client):
	message = FullMessage.message.split ()
	data = s3bucket()
	filesdata = data.get_all_list_files()
	for filesx in filesdata:
		await client.send_message (sender, filesx)

async def file_info_hash(FullMessage,sender,client):
	message = FullMessage.message.split ()
	filehash = message[1]
	dialog_total = inform_file(filehash)
	await client.send_message (sender, dialog_total)


async def getmedia_from_chan(FullMessage,sender,client):
	message = FullMessage.message.split ()
	channame = message[1]
	limited = int (message[2])
	channel = await client.get_entity (channame)
	mime = MIME_TYPES
	data = s3bucket ()
	prev_files = data.get_all_list_files ()
	for tipos in mime :
		async for message in client.iter_messages (channel, limit=limited) :
			if message.media :
				if message.file :
					if message.file.name not in prev_files :
						if tipos in message.file.mime_type :
							fileinfo = str (message.file.name) + " - " + str (message.file.mime_type) + " - " + str (
								message.file.size) + ' in bytes'
							if message.file.size > 324179621:
								await client.send_message (sender, 'File too big to analyze')
							else:
								await client.send_message (sender, fileinfo)
								await client.send_message (sender, 'Analyzing....')
								path = await client.download_media (message.media, "../tmp")
								file_info = analyze_and_upload (path)
								await client.send_message (sender, 'analyzed and uploaded to S3')
								await client.send_message(sender,'hash: ' + str(file_info))
								await client.send_message (sender, 'Virustotal link: '+ 'https://www.virustotal.com/gui/file/' + str (file_info))
