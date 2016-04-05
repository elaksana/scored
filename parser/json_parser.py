import json, sys
from pprint import pprint
reload(sys)
sys.setdefaultencoding("utf-8")

class JsonParser(object):
	def __init__(self, json_path):
		self.filepath = json_path
		try:
			with open(json_path) as data_file:
				self.data = json.load(data_file)
			for key in self.data:
				self.data[key] = self.data[key].replace('\n',' ')
		except:
			print 'Issue parsing ' + self.filepath
			print 'Error: ' + str(sys.exc_info()[0]) 
			return	
	def print_json(self):
		print(self.data['acknowledgement'])
		for key in self.data:
			print '\033[1m' +'\033[96m'+ key
			print '\033[0m' + "\n" + self.data[key]

	def get_filepath(self):
		return self.filepath

	def get_json_data(self):
		return self.data

