#!/usr/bin/python
import json;
import sys;
import getopt;

def usage():
	print "Usage: createpossibilities.py [--output <filename>] [-h]"

try: 
	optlist, args = getopt.getopt(sys.argv[1:], 'ho:', ['output=', 'help'])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) 
        usage()
        sys.exit(2)
outputfile = 'possibilities.json';
for o, a in optlist:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-o", "--output"):
		outputfile = a
	else:
		assert False, "unhandled option"        
        

if (len(sys.argv) == 2):
	outputfile = sys.argv[1];
	


domainnames = {};

# select 4 random letters
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
           'n','o','p','q','r','s','t','u','v','w','x','y','z'];
           
second = 'i';

possibilities = 0;
for first in letters:
	for third in letters:
		for forth in letters:
			for fifth in letters:
				name = first + second + third + forth + fifth;
				domainnames[name] = {'checked': 0, 'updated':'', 'created':''}; 

outfile = open(outputfile, 'w');
outfile.write(json.dumps(domainnames, sort_keys=True, indent=4, separators=(',', ': ')));
outfile.close();

