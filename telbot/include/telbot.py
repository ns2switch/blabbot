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
from dotenv import load_dotenv
from .dynamo import blabdynamo
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.users import GetFullUserRequest

#VARIABLES
load_dotenv()
TOKEN=os.getenv('TELEGRAM_TOKEN')
API_ID=os.getenv('API_ID')
API_HASH=os.getenv('API_HASH')


class botcommand:

    def __init__ (self,events):
        self.events = events
        self.sender = sender
        self.FullMessage = FullMessage

    async def BotMode(self,FullMessage,sender,client):
        dyn = blabdynamo ()
        #await client.send_message (sender, 'Hola amo!')
        if FullMessage.message == '/start':
            await client.send_message (sender, 'Activado')

        elif '/infouser' in FullMessage.message:
            message = FullMessage.message.split ()
            user = message[1]
            full = await client (GetFullUserRequest (user))
            bio = full
            print(bio)

        elif '/joinpriv' in FullMessage.message:
            message = FullMessage.message.split()
            hashed = message[1]
            hashed = hashed.replace("https://t.me/+","")
            chan = await client(ImportChatInviteRequest(hashed))
            chaninfo = chan.to_dict()
            print(chaninfo)
            print(chaninfo['chats']['title'])
            print(chaninfo['chats']['id'])
            print(chaninfo['chats']['participants_count'])
            print(chaninfo['chats']['date'])
            #print('Joining in ' + str(hash))
            #print(chaninfo)

        elif '/joinpart' in FullMessage.message :
            async for dialog in client.iter_dialogs () :
                if dialog.id == chat_id :
                    print(chat_id)
                    await client.delete_dialog (chat_id)
            print_msg_time (f'{channel[1]} has been leaved')

        elif '/infochat' in FullMessage.message :
            dialogs = await client.get_dialogs ()
            print(dialogs)

        elif '/getdb' in FullMessage.message :
            answer = ''
            message = FullMessage.message.split ()
            patternkey = message[1]
            pattern = dyn.scan('message',patternkey)
            for element in pattern:
                answer+= str(element['date']) + " - " + str(element['user']) + " - " + str(element['channel']) + " - " + str(element['message'] )
                if element['media']:
                    answer += " - " + element['media']['webpage']['url']
                answer+= "\n"
            await client.send_message (sender,answer)

        elif '/processlink' in FullMessage.message:
            url = ''
            pattern = dyn.scan ('message', 'https')
            for element in pattern :
                if element['media'] :
                    if element['media']['webpage']['url']:
                        url +=  element['media']['webpage']['url']
                        url += "\n"
            await client.send_message (sender, url)