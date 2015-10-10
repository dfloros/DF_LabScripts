#! usr/bin/python
#syntax takes two arguments.
#	1 - input file.  format: tab separated and headers must include exactly  'SampleID','n_points','files', 'Radius', 'TestIntensity'
#			n_points in the number of points picked for each sample, files is the .txt file that contains those xyz coords
#			at the moment, I think it will break if anything is missing
#			these coords are expected to be from geomagic without header with whitespace seperated xyz values in the second-fourth columns (first is says 'pt1')
			
#	2 - output file - filename.csv -> should be `ili compatabile  
#


import os
import sys

infofile = sys.argv[1]
outputfile = sys.argv[2]

wanted_info_persample = ['SampleID','n_points','files', 'Radius', 'TestIntensity']


def parse_table_with_headers(filename):  #from ming
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
			if len(line_split) > 0:
				header_name = index_to_header_map[column_count]
				if len(header_name) < 1:
					continue
				column_values[header_name].append(line_split.strip())
				column_count += 1
    return (line_count-1, column_values)

def getpoints(file):
	points = []
	with open(file, 'r') as infile:
		points = infile.readlines()
	return points
	
def dereplicate_list(ls):
	newls = []
	for i in ls:
		if i in newls:
			pass
		elif len(i) == 0:
			pass
		else: 
			newls.append(i)
	return newls
	
def build_point_dict(filelist):
	point_values = {}
	for file in filelist:
		filename = ''.join([file,'.txt.'])
		with open(filename, 'r') as infile:
			point_values[file] = infile.readlines()
	return point_values

def sample_info(i):
		info_list = parse_table_with_headers(infofile)[1][wanted_info_persample[i]]
		return info_list

number_of_samples =  parse_table_with_headers(infofile)[0]

SampleID_per_sample = sample_info(0)
points_per_sample = sample_info(1)
file_per_sample = sample_info(2)
radii_per_sample = sample_info(3)
test_intensity = sample_info(4)

point_files = dereplicate_list(parse_table_with_headers(infofile)[1][wanted_info_persample[2]])

point_dict = build_point_dict(point_files)


def compile_points_per_sample(n_points, file):
	sample_points = []
	point_list = point_dict[file]
	count = 0
	thingsOK = True
	for point in range(n_points):
		sample_points.append(point_list.pop(0))
		
		count += 1
	return sample_points
	

def xyz_from_line(line):
	newline = line.rstrip().split()[1:]
	return newline
	
def generate_lines_persample(n):
	blah = zip(points_per_sample, file_per_sample, SampleID_per_sample, radii_per_sample, test_intensity)
	lines = compile_points_per_sample(int(blah[n][0]), blah[n][1])
	newlines = []
	pointlines = []
	newline = []
	for line in lines:
		newline.append(blah[n][2])
		newline.extend(xyz_from_line(line))
		newline.extend([blah[n][3],blah[n][4]])
		newlines.append(str(','.join(newline)))
		newline=[]
	return newlines

final_lines = []
final_lines.append(str(','.join(['SampleID', 'x','y','z','radius', 'intensity'])))	

for i in range(number_of_samples):
	final_lines.append('\n'.join(generate_lines_persample(i)))

	

with open(outputfile, 'w') as outfile:
	outfile.write('\n'.join(final_lines))

quit()

	
	
# x = 1
# for i in points_per_sample:
	# x += int(i)
# diff = x-len(final_lines.readlines())
# if diff == 0:
	# print('boop')
# else:
	# print 'checsum = %d'%x, diff