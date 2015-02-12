#!/usr/bin/python
import json
import whois;
import signal
import sys
import getopt;

def usage():
	print "Usage: checkdomains.py [--output <filename>] [--input <filename>] [-h]"

try: 
	optlist, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['output=', 'input=', 'help'])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) 
        usage()
        sys.exit(2)
inputfile = 'possibilities.json';
outputfile = 'possibilities-filtered.json';
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
	if (namedata[k]['checked'] == 1):
		checked += 1;
	else:
		tocheck += 1;

print str(checked) + "/" + str(len(namedata)) + " completed."; 
print str(tocheck) + "/" + str(len(namedata)) + " remain."; 

checkCount = 0;
for k in namedata.keys():
	if (namedata[k]['checked'] == 1):
		continue
	checkCount += 1;
	domain = whois.query(str(k) + ".com");
	if (domain):
		namedata[k]['checked'] = 1;
		namedata[k]['created'] = domain.creation_date.isoformat();
		namedata[k]['updated'] = domain.last_updated.isoformat();
		print k + " found.";
	else:
		del namedata[k];
	print "Completed " + str(checkCount) + "/" + str(tocheck)


print "Starting to write outputfile.";
outfile = open(outputfile, 'w');
outfile.write(json.dumps(namedata, sort_keys=True, indent=4, separators=(',', ': ')));
print "Done writing ouput file";
outfile.close();			
		
	
	
		


