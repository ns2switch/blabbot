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
from .dynamo import blabdynamo
from .telbot_helper import *

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

		elif '/help' in FullMessage.message:
			await help_commands(FullMessage,sender,client)

		elif '/infouser' in FullMessage.message :
			await infouser_function(FullMessage,sender,client)

		elif '/joinpriv' in FullMessage.message :
			await join_priv_channel(FullMessage,sender,client)

		elif '/part' in FullMessage.message :
			await part_channel(FullMessage,sender,client)

		elif '/getmedia' in FullMessage.message :
			await getmedia_from_chan(FullMessage,sender,client)

		elif '/whichchan' in FullMessage.message:
			await which_channel_iam(FullMessage,sender,client)

		elif '/infochan' in FullMessage.message :
			await infouser_function(FullMessage,sender,client)

		elif '/getdb' in FullMessage.message :
			await get_data_from_dinamo(FullMessage,sender,client)

		elif '/processlink' in FullMessage.message :
			await process_link_in_dynamo(FullMessage,sender,client)

		elif '/allfiles' in FullMessage.message :
			await list_all_files_in_s3(FullMessage,sender,client)