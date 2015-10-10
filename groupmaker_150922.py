#!/usr/bin/python
#this tool takes a path or filename and extracts filenames.
#it will also do some 

import os
import sys

inpath = sys.argv[1]
outpath = sys.argv[2]

#grab filenames from the current directory 


def filegrabber(path):
	filenames = []
	trimmed_files = []
	if os.path.isdir(path) == True:
		filenames = os.listdir('.')
		
	elif os.path.isfile(path) == True:
		filenames = open(str(path), 'r').read().split()
		
	else:
		print "Filegrabber() has a problem.  Make sure you give the script a path or file.  "
		
	for i in filenames:
		if len(i) >= 1:
			trimmed_files.append(i.strip())
			
	return trimmed_files

#confirmation
a = filegrabber(inpath)
print '\n'.join(["%i files found\n" %(len(a)),"First file: %s\n" %(a[0]),"Last file:%s\n" %(a[-1])])



def fileshukker(list):
	
	original = list
	nAttributes = 0
	Things = [[],[],[]]
	for i in list:
		nAttributes = max(nAttributes,len(i.split('_')))
	
	for n in range(nAttributes):
		Things[0].append(str('Attribute_' + n))
		templist = []
		for i in list
		
		
	for filenames in original:
		
		


	
	
	
#split each name for separate metadata items, keep those together as a list of lists
#splits on underscore and excludes file extension



for filename in filenames:
	# filedata.append(filename.split('.')[0].split('_'))