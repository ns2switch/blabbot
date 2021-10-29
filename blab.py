#!/usr/bin/python3

#Copyright 2021 Anibal Cañada


#Blab is a telegram bot that recovers data leaks and allows users to search it is affected

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import json
import random
import string
import datetime
import logging
import time
import yaml
import re
import hibpwned
from uuid import uuid4
from datetime import date , datetime , timedelta
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from pymongo import MongoClient, TEXT, DESCENDING

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#variables - conf
with open("conf/config.yml") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

SHORT_TIME_FORMAT = cfg['date']['short_format']
DAY_NAMES = cfg['date']['names']
TOKEN=cfg['telegram']['token']


def get_text_repr(doc):
    time = doc['time']
    day_shortname = get_day_shortname(time)
    time_str = '%s (%s)' % (time.strftime(SHORT_TIME_FORMAT), day_shortname)
    text = '•' + ' %s\n%s' % (time_str, doc['post'])
    return text


def get_day_shortname(time):
    today = datetime.utcnow().date()
    if time.date() == today:
        return 't'

    yesterday = today - timedelta(days=1)
    if time.date() == yesterday:
        return 'y'

    weekday = DAY_NAMES[time.weekday()]
    return weekday


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi!')

def get_user_collection(user):
    client = MongoClient('mongodb://mongodb:27017/')
    database = client['telbot']

    collection_name = str(user.id)
    user_collection = database[collection_name]
    return user_collection

def history_cursor_to_str(cur):
    reprs = [get_text_repr(d) for d in cur]
    return '\n\n'.join(reprs[::-1])

def get_document_from_message(msg):
    DATETIME_SET_RE = r'#t (\d{4}.\d{2}.\d{2} \d{1,2}:\d{1,2})'
    timestamp = re.search(DATETIME_SET_RE, msg)
    if timestamp:
        explicit_time = datetime.strptime(timestamp.group(1), SHORT_TIME_FORMAT)
        msg = re.sub(DATETIME_SET_RE, '', msg)
    else:
        explicit_time = None

    post = msg

    doc = {
	'time': explicit_time or datetime.utcnow(),
        'post': post,
    }
    return doc

def search(update: Update, _: CallbackContext ) -> None:
    user = update.message.from_user
    user_collection = get_user_collection(user)

    # make sure user collection has a text index
    user_collection.create_index([('post', TEXT)], default_language='spanish')

    msg = update.message.text.replace('/busca', '')

    res_cur = user_collection.find({'$text': {'$search': msg }}) \
                             .sort('time', -1) \
                             .limit(10)
    res_str = history_cursor_to_str(res_cur)
    if not res_str.strip():
        res_str = 'No se que me dices'
    update.message.reply_text(res_str, disable_web_page_preview=True)

def save(update: Update, _: CallbackContext ) -> None:
    msg = update.message.text
    user = update.message.from_user
    msg = update.message.text.replace('/recuerda', '')
    user_collection = get_user_collection(user)
    doc = get_document_from_message(msg)
    doc_id = user_collection.insert_one(doc)
    if doc_id:
        update.message.reply_text('Apuntado')

def stats(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    user_coll = get_user_collection(user)
    response = 'Hay logeados {} mensajes\n'.format(user_coll.count())
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['telbot']
    coll_counts = [db[coll].count() for coll in db.collection_names()]
    response += '\nTelBot has `{}` users\n'.format(len(coll_counts))
    response += 'Conversacion mas larga: `{}`\n'.format(sorted(coll_counts)[-3:])
    month_ago = datetime.utcnow() - timedelta(days=30)
    recent_counts = [db[coll].find({'time': {'$gt': month_ago}}).count() for coll in db.collection_names()]
    response += 'Mensajes en el ultimo mess:  `{}`\n'.format(sum(recent_counts))
    active_colls = sum([c > 0 for c in recent_counts])
    response += 'Usuarios activos en el ultimo mess: `{}`\n'.format(active_colls)

    update.message.reply_text(response, parse_mode='Markdown')


def pass_command(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    length = update.message.text.split(" ")[1]
    if not length:
        length = 1
    length = int(length)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    all = lower + upper + num + symbols
    temp = random.sample(all,length)
    passw = "".join(temp)
    update.message.reply_text(passw)


def pwned_commad(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    text =  update.message.text.replace('/pwned', '')
    pwnedSearch =  hibpwned.Pwned(text, APP_NAME, PWNED_API)
    tBreaches = pwnedSearch.searchAllBreaches ()
    for item in tBreaches:
        data = tBreaches[item][0]['link']
    update.message.reply_text(data)

def inlinequery(update: Update, _: CallbackContext) -> None:
    query = update.inline_query.query

    if query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]

    update.inline_query.answer(results)


def main() -> None :
    # Create the Updater and pass it your bot's token.
    updater = Updater (TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler (CommandHandler ("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler (InlineQueryHandler (inlinequery))

    # Start the Bot
    updater.start_polling ()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle ()

if __name__ == '__main__':
    main()


