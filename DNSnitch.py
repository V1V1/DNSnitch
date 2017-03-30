#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################################
# DNSnitch.py:	Uses viewdns.info to perform a reverse NS lookup on a specified nameserver 
#		and attempts zone transfers on discovered domains.
# Example:	$ DNSnitch.py -n nameserver.target.com -zt
# Author:	VIVI | <Website: thevivi.net> | <Email: gabriel@thevivi.net> | <Twitter: @_theVIVI>
###################################################################################################

import argparse
import urllib
import time
import sys
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE, STDOUT

# Console colors
W = '\033[0m'     #white (normal)
R = '\033[31m'    #red
T = '\033[93m'    #tan
G = '\033[32m'    #green
LG = '\033[1;32m' #light green

class Logger:

    def __init__(self, stdout, filename):
        self.stdout = stdout
        self.logfile = file(filename, 'w')

    def write(self, text):
        self.stdout.write(text)
        self.logfile.write(text)

    def close(self):
        self.stdout.close()
        self.logfile.close()

def parse_args():

    # Arguments

    parser = argparse.ArgumentParser(description="Reverse nameserver lookups " +
    	"using http://viewdns.info.")

    parser.add_argument(
        "-n",
        "--nameserver",
        help="Name server e.g. ns1.target.com",
        required=True
    )
    parser.add_argument(
        "-zt",
        "--zonetransfer",
        help="Attempt zone transfers on discovered domains",
        action='store_true'
    )

    parser.add_argument(
    	"-o",
    	"--output",
    	help='Destination output file')

    return parser.parse_args()

def shutdown():

	 print '\n[' + R + '!' + W + '] Closing'
	 sys.exit()

def reverseNS():

	#Request URL
	lookup = urllib.urlopen('http://viewdns.info/reversens/?ns='+str(nameServer))

	#Get the results table
	response =  lookup.read()
	html = BeautifulSoup(response, "lxml")
	tables = html.findChildren('table')
	resultsTable = tables[3]

	#Parse results
	domains = []

	rows = resultsTable.find_all('tr')
	for row in rows:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		domains.append([ele for ele in cols if ele])

	#Remove column title
	del domains[0]

	#Count results
	domainCount = len(domains)

	#Print results
	print '[' + G + '+' + W + '] %d domains found using ' % domainCount + LG + \
	'' +nameServer+"\n"+W
	time.sleep(2)

	for results in domains:
		print '\n'.join(results)

	if args.zonetransfer == True:
		print '\n==============================\n'
		zoneTransfer(domains)

def zoneTransfer(domains):

	count = 0
	ns = "@" + nameServer

	#Attempt zone transfers 
	print ('\n[' + G + '+' + W + '] Attempting zone transfers on discovered '+
	'domains...\n \n')
	time.sleep(2)

	for line in domains:

		count +=1

		print '[' + T + str(count) + W + '] Domain Name:  ' + LG + \
		str(line).join(line) +W
		p = Popen(['dig', 'axfr', str(ns), str(line).join(line)], stdin=PIPE,\
		 stdout=PIPE, stderr=STDOUT, close_fds=True)
		output = p.stdout.read()
		print output
		print "-------------------------------------------------------------\n"

# Main section
if __name__ == "__main__":

	print """
	▗▄▄  ▗▄ ▗▖ ▗▄▖        █            ▗▖   
	▐▛▀█ ▐█ ▐▌▗▛▀▜        ▀   ▐▌       ▐▌   
	▐▌ ▐▌▐▛▌▐▌▐▙   ▐▙██▖ ██  ▐███  ▟██▖▐▙██▖
	▐▌ ▐▌▐▌█▐▌ ▜█▙ ▐▛ ▐▌  █   ▐▌  ▐▛  ▘▐▛ ▐▌
	▐▌ ▐▌▐▌▐▟▌   ▜▌▐▌ ▐▌  █   ▐▌  ▐▌   ▐▌ ▐▌
	▐▙▄█ ▐▌ █▌▐▄▄▟▘▐▌ ▐▌▗▄█▄▖ ▐▙▄ ▝█▄▄▌▐▌ ▐▌
	▝▀▀  ▝▘ ▀▘ ▀▀▘ ▝▘ ▝▘▝▀▀▀▘  ▀▀  ▝▀▀ ▝▘ ▝▘
	"""
	
	#Timer
	start = time.time()

	# Parse args
	args = parse_args()
	nameServer = args.nameserver

	if args.output != None:
		logger = Logger(sys.stdout, args.output)
		sys.stdout = logger

	try:
		reverseNS()
		print 'Finished. \nScript runtime: '+ T \
		, time.time()-start, 'seconds'
	except KeyboardInterrupt:
		shutdown()
