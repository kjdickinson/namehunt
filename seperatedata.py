#!/usr/bin/python
import json
import sys
import getopt;


def usage():
	print "Usage: seperatedata.py [--chunks <chunkcount>] [--size <chunksize>] [--path <output dir>] [--output <outfile suffix>] [-h]"

try: 
	optlist, args = getopt.getopt(sys.argv[1:], 'hc:s:p:o:', ['chunks=', 'size=', 'path=', 'output=', 'input=', 'help', 'single'])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) 
        usage()
        sys.exit(2)
chunks=5
size=0
path="."
output="chuck.json"
inputfile="possibilities.json"
single = 0;
for o, a in optlist:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-c", "--chunk"):
		chunks = a
	elif o in ("-s", "--size"):
		size = a
	elif o in ("-p", "--path"):
		path = a
	elif o in ("-o", "--output"):
		output = a
	elif o in ("-i", "--input"):
		inputfile = a 
	elif o in ("--single"):
		single = 1 
	else:
		assert False, "unhandled option"

allData = {}
	
json_data=open(inputfile)
allData = json.load(json_data)
json_data.close()


if (single == 1):
	# Just one chunk is desired
	size = int(size)
	if (size == 0):
		print "option --size required with --single option";
		exit(1);
	thisChunk = {}
	for i in range(size):
		try:
			key, value = allData.popitem();
			thisChunk[key] = value;
		except:
			break;
	print "Write chunk"
	outfile = open("chunk-" + output, 'w');
	outfile.write(json.dumps(thisChunk, sort_keys=True, indent=4, separators=(',', ': ')));
	outfile.close();
	print "Write Remainder"
	outfile = open(output, 'w');
	outfile.write(json.dumps(allData, sort_keys=True, indent=4, separators=(',', ': ')));
	outfile.close();
	exit(0);

itemCount = len(allData);

if (size == 0):
	size = int(itemCount / chunks) + 1

size = int(size);

chunkNum = 1;
thisChunk = {}
	
while (len(allData)):
	# Pull 'size' pieces of data from the data and write them to the outfile
	for i in range(size):
		try:
			key, value = allData.popitem();
			thisChunk[key] = value;
		except:
			break;
	
	outputfile = path + "/" + str(chunkNum) + "-" + output;
	outfile = open(outputfile, 'w');
	outfile.write(json.dumps(thisChunk, sort_keys=True, indent=4, separators=(',', ': ')));
	outfile.close();
	print "Wrote " + outputfile;	
	thisChunk = {}
	chunkNum += 1;