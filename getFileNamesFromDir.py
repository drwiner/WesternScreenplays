import os
from os import listdir
from os.path import isfile, join
mypath = os.getcwd()
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

fn = open('file_names.txt', 'w')

for file in onlyfiles:
	fn.write(file)
	fn.write('\n')

fn.close()