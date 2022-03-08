import os
import boto3
from os import remove
from dotenv import load_dotenv

BUCKET_NAME = os.getenv('BUCKET_NAME')

class s3bucket (object):

	def __init__(self,filename) :
		self.s3blab = boto3.client ('s3',region_name='eu-west-1')
		self.filename = filename

	def upload_file(self):
		file_name = os.path.basename(self.filename)
		with open (self.filename, "rb") as f :
			self.s3blab.upload_fileobj (f, BUCKET_NAME, file_name )
		remove(self.filename)

