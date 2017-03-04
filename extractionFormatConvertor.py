#!/usr/bin/python

#  This script is used to convert dependency file with CoNLL format
#  to extraction file that could be used in Basilisk.
#
#   Author: Haibo Ding
#   Email: haibonlp@gmail.com
#   Data: July 2013
#
# edited 2017-03-03 for python3



import sys
import os


def readStopWords(stopfile):
	In = open(stopfile)
	stopwords = {line.strip() for line in In}
	return stopwords


def extract(infile, stopfile, outfile):
	stopwords = readStopWords(stopfile)
	IN = open(infile)
	Out = open(outfile, 'w')
	sentlist = []
	sent = []
	for line in IN:
		line = line.strip()
		if len(line) > 0:
			sent.append(line)
		else:
			sentlist.append(sent)
			sent = []
	IN.close()
	if len(sent) > 0:
		sentlist.append(sent)

	for sent in sentlist:
		if len(sent) == 0:
			continue

		for line in sent:
			terms = line.split()
			if len(terms) != 10:
				print('Error  term size  :      ', line)
				continue
			tId = terms[0].strip()
			word = terms[1].strip()
			pos = terms[4].strip()
			dId = int(terms[6].strip())
			dpTag = terms[7].strip()

			if dId != 0:
				dId -= 1
				try:
					dpline = sent[dId]
				except:
					print('here')
				dpTerms = dpline.split()
				if len(dpTerms) != 10:
					print('Error  terms size  :   ', dpline)
					continue

				dpWord = dpTerms[1].strip()
				dpPos = dpTerms[4].strip()
				if pos.startswith('NOUN') and word not in stopwords:
					dpPattern = word + ' *  ' + '<GDep>:' + '<' + dpTag + '>:<dependent>:' + dpWord
					Out.write(dpPattern + '\n')
				if dpPos.startswith('NOUN') and dpWord not in stopwords:
					dpPattern = dpWord + ' * ' + '<GDep>:' + '<' + dpTag + '>:<head>:' + word
					Out.write(dpPattern + '\n')

if __name__ == '__main__':

	# if len(sys.argv) != 4:
	# 	print('usage :  ./program   datalistfile   stopfile   outputfile')
	# 	# os.abort()
	listfile = 'western.parse'
	stopfile = 'stopwords.dat'
	outfile = 'western.extractionpattern'
	extract(listfile, stopfile, outfile)







