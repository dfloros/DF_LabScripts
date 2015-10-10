#!/usr/bin/python
#Generate random sampletables in xml -> syntax is python DF_sampletablemaker.py <anyoldxmlfile.xml> <yournewinfo-tabseperated.txt>
#caveats: headers of new info must match the parameter you want to replace in the xml and cannot be found twice.  
# ex: Method will match to <Method=''> and <MS_Method+''> so this will cause problems.  


import os as os
import sys as sys
import random as random


#automation
#sys.argv[1] = infile



inputxml = sys.argv[1]
infofile =  sys.argv[2]

infile = open(inputxml,'r')
outputxml = open(''.join(['new',inputxml]), 'w')



def rowsandthings(filename, delimiter = ' '):
	with open(filename, 'r') as infile:
		rows = infile.readlines()
		things = []
		RnT = [rows,things]
		for i in rows:
			things.append(i.split(delimiter))
	return RnT

def getheaders(f):
	headers = []
	with open(f,'r') as infile:
		line = infile.readlines()[0].split('\t')
		for thing in line: headers.append(thing.strip())
	return headers
	
#pass me an iterable, will return a replaced iterable
def replacething(rowthings, attribute, value):
	for thing in rowthings:
		if str(attribute+'=') in thing:
			newthing = ''.join([attribute,'="',value,'"'])
			yield newthing
		else: yield thing
	


def xmlsorter(f):
	r = rowsandthings(f)[0]
	t = rowsandthings(f)[1]
	headRows = []
	SampleRows = []
	SampleThings = []
	xmlparts = [headRows, SampleRows, SampleThings]
	for i in range(len(r)):
		if '<Sample ' in r[i]:
			SampleRows.append(r[i])
			SampleThings.append(t[i])
		else: headRows.append(r[i])
	return xmlparts
		
##From ming:
def get_header_mappings(header_str):
    header_mapping = {}
    header_splits = header_str.rstrip().split("\t")
    index_count = 0
    for header in header_splits:
        header_mapping[header] = index_count
        index_count += 1
    return header_mapping

#Parses a filename and returns 2 things
#first is the number of lines, and then a map to lists with the key being the column. 
def parse_table_with_headers(filename):
    input_file = open(filename, "r")
    
    line_count = 0
    headers = []
    index_to_header_map = {}
    column_values = {}
    for line in input_file:
        line_count += 1
        if line_count == 1:
            headers = line.rstrip().split("\t")
            header_idx = 0
            for header in headers:
                index_to_header_map[header_idx] = header
                header_idx += 1
                if len(header) > 0:
                    column_values[header] = []
            
            continue
        
        line_splits = line.split("\t")
        column_count = 0
        for line_split in line_splits:
			header_name = index_to_header_map[column_count]
			#if len(header_name) < 1:
				#continue
			column_values[header_name].append(line_split.strip())
			column_count += 1

    return (line_count-1, column_values)
#end from ming


	
def generate_new_sample_line(example_line_things, attributes, col_values, sample):
	tempthings = example_line_things
	for attribute in attributes:
		tempthings = replacething(tempthings, attribute, col_values[attribute][sample])
	
	return ' '.join(tempthings)
		
def xmlConstructor(headlines, samplelines, tail):
	xmlstring = '\n'.join(['\n'.join(headlines), '\n'.join(samplelines), tail])
	return xmlstring	
	


attributes = parse_table_with_headers(infofile)[1].keys()


attributevalues = parse_table_with_headers(infofile)[1]


n_samples = parse_table_with_headers(infofile)[0]



	
example_sample_things = xmlsorter(inputxml)[2][0]

example_head_lines = xmlsorter(inputxml)[0][:-1]
example_tail_line = xmlsorter(inputxml)[0][-1]

New_sample_lines = []

for i in range(n_samples):
	newline = generate_new_sample_line(example_sample_things, attributes, attributevalues, i)
	New_sample_lines.append(newline)

random.shuffle(New_sample_lines)

with outputxml as out:
	out.write(xmlConstructor(example_head_lines, New_sample_lines, example_tail_line))

	


