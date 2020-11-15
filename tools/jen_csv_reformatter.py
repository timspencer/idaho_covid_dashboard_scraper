#!/usr/bin/env python3
#
# This script reformats a csv file according to requirements from Jen:
#   I have attached a csv with the headers and an example of the data formatting. I want to convert all of the dates to the format "yyyy-mm-dd" and convert the "Health District x" to just "x"
#

import csv
import sys
import os
import re
import datetime

# make sure we have all the proper commandline arguments
if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
	print('usage:  ' + sys.argv[0] + ' <inputfilename.csv> <outputfilename.csv>')
	exit(1)

with open(sys.argv[1]) as csvfile:
	# read in the csv file
	csvreader = csv.DictReader(csvfile)
	with open(sys.argv[2], 'w') as csvoutputfile:
		# write out the output file
		csvwriter = csv.DictWriter(csvoutputfile, fieldnames=csvreader.fieldnames)
		csvwriter.writeheader()

		for row in csvreader:
			# change date format here from 21-Mar-20 to yyyy-mm-dd by iterating across
			# all the values and if they match, convert them.
			for k, v in row.items():
				try:
					newdate = datetime.datetime.strptime(v, '%d-%b-%y').strftime('%Y-%m-%d')
				except ValueError as e:
					pass
				else:
					row[k] = newdate

			# get rid of Health District
			row['JURISDICTION_NM'] = re.sub(r'^Health District ', '', row['JURISDICTION_NM'])

			csvwriter.writerow(row)
