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

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown


class botcomand :

	def __init__(self, update) :
		self.update = update

	def pass_command(update: Update, _: CallbackContext) -> None :
		user = update.message.from_user
		length = update.message.text.split (" ")[1]
		if not length :
			length = 1
		length = int (length)
		lower = string.ascii_lowercase
		upper = string.ascii_uppercase
		num = string.digits
		symbols = string.punctuation
		all = lower + upper + num + symbols
		temp = random.sample (all, length)
		passw = "".join (temp)
		update.message.reply_text (passw)

	def inlinequery(update: Update, _: CallbackContext) -> None :
		query = update.inline_query.query
		if query == "" :
			return
		results = [
			InlineQueryResultArticle (
				id=str (uuid4 ()),
				title="Caps",
				input_message_content=InputTextMessageContent (query.upper ()),
			),
			InlineQueryResultArticle (
				id=str (uuid4 ()),
				title="Bold",
				input_message_content=InputTextMessageContent (
					f"*{escape_markdown (query)}*", parse_mode=ParseMode.MARKDOWN
				),
			),
			InlineQueryResultArticle (
				id=str (uuid4 ()),
				title="Italic",
				input_message_content=InputTextMessageContent (
					f"_{escape_markdown (query)}_", parse_mode=ParseMode.MARKDOWN
				),
			),
		]

		update.inline_query.answer (results)

	def start(update: Update, _: CallbackContext) -> None :
		update.message.reply_text ('Hi!')

	def arsa(update: Update, _: CallbackContext) -> None :
		update.message.reply_text ('Arsa!')

	def help(update: Update, _: CallbackContext) -> None :
		update.message.reply_text ('Usage: \n /help to see this text \n /start to begin')
