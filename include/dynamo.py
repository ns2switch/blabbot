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

import boto3
import yaml
from boto3.dynamodb.conditions import Key, Attr

class blabdynamo :
	# variables - conf
	with open ("conf/config.yml") as ymlfile :
		cfg = yaml.safe_load (ymlfile)
	TABLE_CHAT = cfg['dynamodb']['table_chat']
	dynamodb = boto3.resource ('dynamodb',region_name='eu-west-3')
	table = dynamodb.Table (TABLE_CHAT)

	def save(self, item) :
		self.table.put_item (item)

	def get(self, key) :
		response = self.table.get_item (key)
		return response

	def update(self, key, expresion, attribute) :
		self.table.update_item(key,expresion,attribute)
		self.save(key)

	def search(self,key,value):
		response = self.table.query(KeyConditionExpression=Key(key).eq(value))
		items = response['Items']
		return items

	def scan(self,key,ident,value):
		sdata = ident + "(" + value +")"
		filter = "Attr" + "(" + key + ")" + "." + sdata
		response = self.table.scan(FilterExpression=filter)
		return response['Items']