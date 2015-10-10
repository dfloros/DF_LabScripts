#!/usr/bin/python
#metadata from filenames for Don

import os as os
import sys as sys

#grab filenames from the current directory 


filenames = os.listdir(‘.’)
filedata  = []

#split each name for separate metadata items, keep those together as a list of lists
#splits on underscore and excludes file extension
for filename in filenames:
	filedata.append(filename.split('.')[0].split('_'))

#metadatacategorit
metadata_1 = []
metadata_2 = []


#split each 

for i in filedata: