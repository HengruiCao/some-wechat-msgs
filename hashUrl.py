import sys
import hashlib

def hash(str):
	m = hashlib.sha1()
	m.update(str)
	return m.hexdigest()

if len(sys.argv) < 2:
	print "If you don't find your crawled html use this hash function"
	print "Supply your url as argument"

inputstring = sys.argv[1]
print hash(inputstring)
