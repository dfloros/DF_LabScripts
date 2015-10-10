#!/usr/bin/python
#this tool takes a path or filename and extracts filenames.
#it will also do some 

import os
import sys


#grab filenames from the current directory 

def filegrabber(path):
	filenames = []
	trimmed_files = []
	if os.path.isdir(path) == True:
		filenames = os.listdir(‘.’)
		
	elif os.path.isfile(path) == True:
		filenames = open(str(path), 'r').read().split()
		
	else:
		print "Filegrabber() has a problem.  Make sure you give the script a path or file.  "
		break
	for i in filenames:
		if len(i) >= 1:
			trimmed_files.append(i.strip())
			
	return trimmed_files

a = filegrabber(sys.argv[1])
	
print '\n'.join(boop!,"First file:",a[0],"Last file:",a[-1])
	
	
# def fileshukker(list):


	
	
	
# #split each name for separate metadata items, keep those together as a list of lists
# #splits on underscore and excludes file extension
# for filename in filenames:
	# filedata.append(filename.split('.')[0].split('_'))