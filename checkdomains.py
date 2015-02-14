#!/usr/bin/python
import json
import whois;
import signal
import sys
import getopt;
import re;

companyName = re.compile('^.i.v.$');

def usage():
	print "Usage: checkdomains.py [--output <filename>] [--input <filename>] [--in-place <filename>][-h] [--nowhois]"

try:
	optlist, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['output=', 'input=', 'help', 'in-place=', 'nowhois'])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)
        usage()
        sys.exit(2)
inputfile = 'possibilities.json';
outputfile = 'possibilities-filtered.json';
dowhois = 1
for o, a in optlist:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-o", "--output"):
		outputfile = a
	elif o in ("-i", "--input"):
		inputfile = a
	elif o in ("--in-place"):
		inputfile = a
		outputfile = a
	elif o in ("--nowhois"):
		dowhois = 0
	else:
		assert False, "unhandled option"

namedata = {};

def signal_handler(signal, frame):
    global namedata;
    print('You pressed Ctrl+C!')
    print "Starting to write outputfile.";
    outfile = open(outputfile, 'w');
    outfile.write(json.dumps(namedata, sort_keys=True, indent=4, separators=(',', ': ')));
    print "Done writing ouput file";
    outfile.close();
    exit(0);

signal.signal(signal.SIGINT, signal_handler)


json_data=open(inputfile)
namedata = json.load(json_data)
json_data.close()

print "Finished reading input file.";


tocheck = 0;
checked = 0;
for k in namedata.keys():
	if (len(namedata[k]['updated']) > 0):
		checked += 1;
	else:
		tocheck += 1;

print str(checked) + "/" + str(len(namedata)) + " completed.";
print str(tocheck) + "/" + str(len(namedata)) + " remain.";

startlength = len(namedata)
checkCount = 0;

knownstuck = ['likvc',
              'aiivs',
			  'tikvx',
			  'tikvs',
			  'tikvr',
			  'sicvo',
			  'micve',
			  'zivvi',
			  'yicvs',
			  'vitvb',
			  'aiove',
			  'xinve',
			  'bitvv',
			  'riqvy',
			  'uimvp',
			  'yixve',
			  'oiyvf',
			  'milvs',
			  'tibvb',
			  'divvv',
			  'ticvo',
			  'pinvs',
			  'rivvu',
			  'giova',
			  'giovo',
			]

for k in namedata.keys():
	checkCount += 1;

	print "Consider: " + str(checkCount) + " of " + str(startlength) + " " + k
	# If the name doesn't match *i*v* then remove it
	if (not companyName.match(k)):
		del namedata[k]
		continue

	# Known stuck hostname
	if (k in knownstuck):
		continue;
	if ('checked' in namedata[k]):
		del namedata[k]['checked']
	if (len(namedata[k]['updated']) > 0):
		continue
	if (dowhois == 0):
		continue

	try:
		domain = whois.query(str(k) + ".com", ignore_returncode=1);
	except:
		e = sys.exc_info()[1]
		print "Whois exception: " + str(e);
		outfile = open(outputfile, 'w');
		outfile.write(json.dumps(namedata, sort_keys=True, indent=4, separators=(',', ': ')));
		print "Done writing ouput file";
		outfile.close();
		exit(0);

	if (domain):
		if ('checked' in namedata[k]):
			del namedata[k]['checked']
		namedata[k]['created'] = domain.creation_date.isoformat();
		namedata[k]['updated'] = domain.last_updated.isoformat();
		print k + " found.";
	else:
		del namedata[k];



print "Starting to write outputfile.";
outfile = open(outputfile, 'w');
outfile.write(json.dumps(namedata, sort_keys=True, indent=4, separators=(',', ': ')));
print "Done writing ouput file";
outfile.close();
