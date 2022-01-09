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

import mysql.connector
import sys
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
ENDPOINT=os.getenv('ENDPOINT')
PORT=os.getenv('PORT')
USER=os.getenv('USER')
REGION=os.getenv('REGION')
DBNAME=os.getenv('DBNAME')


class rsql :
	def __init__(self) :
		self.client = boto3.client('rds')
		self.token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)
		try :
			self.conn = mysql.connector.connect(host=ENDPOINT, user=USER, passwd=self.token, port=PORT, database=DBNAME)
			self.cur = self.conn.cursor ()
			self.cur.execute ("""SELECT now()""")
			query_results = self.cur.fetchall ()
			print (query_results)
		except Exception as e :
			print ("Database connection failed due to {}".format (e))


	def save(self):
		pass


	def get_data(self):
		pass