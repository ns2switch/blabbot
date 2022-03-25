import os
import time
import json
import hashlib
import virustotal3.core
from dotenv import load_dotenv


load_dotenv ()
API_KEY = os.getenv ('VT_API')
vt = virustotal3.core.Files (API_KEY)


def inform_file(filehash) :
	hash = vt.info_file (filehash, timeout=30)
	return hash

class vtotal (object) :
	def __init__(self, filename) :
		self.filename = filename
		self.hash = 0

	def get_hash_info(self) :
		sha256_hash = hashlib.sha256 ()
		with open (self.filename, "rb") as f :
			for byte_block in iter (lambda : f.read (65536), b"") :
				sha256_hash.update (byte_block)
		self.hash = sha256_hash.hexdigest ()
		vt_files = virustotal3.core.Files (API_KEY)
		try :
			info = vt_files.info_file (self.hash)
			return info
		except :
			print ("Analyzing")
			analyzed = self.get_file_analysis ()
			return analyzed

	def get_file_analysis(self) :
		response = vt.upload (self.filename)
		analysis_id = response['data']['id']
		print ('Analysis ID: {}'.format (analysis_id))
		results = virustotal3.core.get_analysis (API_KEY, analysis_id)
		status = results['data']['attributes']['status']
		print ('Waiting for results...')
		while 'completed' not in status :
			results = virustotal3.core.get_analysis (API_KEY, analysis_id)
			status = results['data']['attributes']['status']
			print ('Current status: {}'.format (status))
			time.sleep (10)
		results = virustotal3.core.get_analysis (API_KEY, analysis_id)
		#print (json.dumps (results, indent=4, sort_keys=True))
		return results


