import os
import time
import json
import hashlib
import virustotal3.core
from dotenv import load_dotenv

load_dotenv ()
API_KEY = os.getenv('VT_API')
vt = virustotal3.core.Files(API_KEY)


class vtotal(object):
	def __init__(self,filename) :
		self.filename = filename

	def get_hash_info(self):
		sha256_hash = hashlib.sha256 ()
		with open (self.filename, "rb") as f :
			for byte_block in iter (lambda : f.read (65536), b"") :
				sha256_hash.update (byte_block)
		filehash = sha256_hash.hexdigest ()
		vt_files = virustotal3.core.Files (API_KEY)
		try:
			info = vt_files.info_file(filehash)
			return info
		except:
			return "Not present in virustotal - hash: " + str(filehash)

	def get_file_analysis(self):
		response = vt.upload(filename)
		analysis_id = response['data']['id']
		print('Analysis ID: {}'.format(analysis_id))
		results = virustotal3.core.get_analysis(API_KEY, analysis_id)
		status = results['data']['attributes']['status']
		print('Waiting for results...')
		while 'completed' not in status:
			results = virustotal3.core.get_analysis(API_KEY, analysis_id)
			status = results['data']['attributes']['status']
			print('Current status: {}'.format(status))
			time.sleep(10)
		results = virustotal3.core.get_analysis(API_KEY, analysis_id)
		print(json.dumps(results, indent=4, sort_keys=True))