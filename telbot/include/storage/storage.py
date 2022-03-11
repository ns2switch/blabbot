import os
import boto3
from os import remove
from dotenv import load_dotenv

BUCKET_NAME = os.getenv('BUCKET_NAME')

class s3bucket:

	def __init__(self) :
		self.s3blab = boto3.client ('s3',region_name='eu-west-1')


	def upload_file(self,filename):
		file_name = os.path.basename(filename)
		with open (filename, "rb") as f :
			self.s3blab.upload_fileobj (f, BUCKET_NAME, file_name )
		remove(filename)

	def list_all_files(self):
		list_file_list =[]
		for object in self.s3blab.list_objects(Bucket=BUCKET_NAME)['Contents']:
			list_file_list.append(object['Key'])
		return list_file_list

	def get_all_list_files(self):
		list_files = s3bucket.list_all_files(self)
		return list_files

	def signed_url(self):
		share = self.s3blab.generate_presigned_url(ClientMethod="get_object",ExpiresIn=3600,Params={"Bucket":BUCKET_NAME,"Key":self.filename})
		return share
