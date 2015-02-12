#!/usr/bin/python
import json
import sys
import getopt;


def usage():
	print "Usage: combinedata.py [--output <outfile>] [-h] <inputfile list>"

try: 
	optlist, args = getopt.getopt(sys.argv[1:], 'ho:', ['output=', 'help'])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) 
        usage()
        sys.exit(2)
chunks=5
size=0
path="."
output="combine.json"
for o, a in optlist:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-o", "--output"):
		output = a
	else:
		assert False, "unhandled option"

allData = {}
	

for a in args:
	thisChunk = {}
	json_data=open(a)
	thisChunk = json.load(json_data)
	json_data.close()
	
	allData = dict(allData.items() + thisChunk.items())


	
outfile = open(output, 'w');
outfile.write(json.dumps(allData, sort_keys=True, indent=4, separators=(',', ': ')));
outfile.close();
