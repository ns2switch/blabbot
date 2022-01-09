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
import boto3
from dotenv import load_dotenv
from boto3.dynamodb.conditions import Key, Attr
load_dotenv()
TABLE_CHAT=os.getenv('TABLE_CHAT')

class blabdynamo :
	def __init__(self) :
		self.dynamodb = boto3.resource ('dynamodb',region_name='eu-west-1')
		self.table = self.dynamodb.Table (TABLE_CHAT)
	# variables - conf

	def save(self, data) :
		self.table.put_item (Item=data)

	def get(self, key) :
		response = self.table.get_item (key)
		return response

	def update(self, key, expresion, attribute) :
		self.table.update_item(key,expresion,attribute)
		self.save(key)

	def search(self,key,value):
		response = self.table.query(
			IndexName="message-index",
			KeyConditionExpression=Key(key).eq(value))
		items = response['Items']
		return items

	def scan(self,key,value):

		response = self.table.scan(
			FilterExpression=Attr(key).contains(value))
		return response['Items']