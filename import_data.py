import re
import requests
from requests.exceptions import HTTPError
import hashlib

## Configuration
msgfile = 'record.xls'
outdir = 'tmp/'
##

records = []
urlregexp = re.compile(r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:;%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:;%_\+.~#?&//=]*)")

def start():
	with open(msgfile, 'r') as csvfile:
		fieldnames = ['id', 'time', 'nickname','status', 'type', 'msg']
		for (i, row) in enumerate(csvfile.readlines()):	
			if (i < 2): #start with 3rd line
				continue
			record = {}
			record["msgid"] = i - 2
			record['id'] = row[0:30]
			record['time'] = row[30:55]
			record['nickname'] = row[55:80]
			record['status'] = row[80:100]
			record['type'] = row[100:120]
			record['msg'] = row[120:]
			records.append(record)
			for match in urlregexp.finditer(record["msg"]):
				url = match.group(0)
				fetchUrl(record, url)
				#print url

def hash(str):
	m = hashlib.sha1()
	m.update(str)
	return m.hexdigest()

def fetchUrl(record, url):
	try:
		r = requests.get(url)
		r.raise_for_status()
	except Exception:
		#print 'Could not download page'
		pass
	else:
		with open(outdir + str(record["msgid"]) + '-' + hash(r.url) + '.html', 'w') as output:
			output.write(r.content)
		print hash(r.url), r.url, 'downloaded successfully'

start()