#!/usr/bin/python
import json
import sys
import getopt;


def usage():
	print "Usage: writecsv.py [--input <inputfile>] [--output <outfile>] [-h]"

try:
	optlist, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['output=', 'input=', 'help'])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)
        usage()
        sys.exit(2)
outputfile="data.csv"
inputfile="data.json"
for o, a in optlist:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-o", "--output"):
		outputfile = a
	elif o in ("-i", "--input"):
		inputfile = a
	else:
		assert False, "unhandled option"


namedata = {}

json_data=open(inputfile)
namedata = json.load(json_data)
json_data.close()

csvfile=open(outputfile, 'w')
csvfile.write("name,created,modified\n")
for k in namedata.keys():
    line = k + ',' + namedata[k]['created'][:-9] + ',' + namedata[k]['updated'][:-9] + '\n'
    csvfile.write(line);
csvfile.close();
