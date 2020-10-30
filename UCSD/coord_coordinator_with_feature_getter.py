#! usr/bin/python

import os
import sys

infofile = sys.argv[1]
featurefile = sys.argv[2]
outputfile = sys.argv[3]

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
        
        line_splits = line.split('\t')
        column_count = 0
        for line_split in line_splits:
			header_name = index_to_header_map[column_count]
			column_count += 1

			if len(header_name) < 1:
				#print index_to_header_map
				continue
			column_values[header_name].append(line_split.strip())
    return (line_count-1, column_values)

def getpoints(file):
	points = []
	with open(file, 'r') as infile:
		points = infile.readlines()
	return points
	return
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
	return
	
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
	


def get_all_features(file):
		lines = open(file, 'r').readlines()
		feats = []
		sampleinfo = {}
		tableinfo = parse_table_with_headers(file)[1]
		# for name in tableinfo:
			# sampleinfo['_'.join(name.split('_')[:6])] = tableinfo[name]
		for line in lines[1:]:
			feats.append(line.split('\t')[0])
		tableinfo['features'] = feats
		return tableinfo

def generate_lines_persample(n):
	blah = zip(points_per_sample, file_per_sample, SampleID_per_sample, radii_per_sample, test_intensity)
	lines = compile_points_per_sample(int(blah[n][0]), blah[n][1])
	newlines = []
	pointlines = []
	newline = []
	feats = get_all_features(featurefile)
	for line in lines:
		newline.append(blah[n][2])
		newline.extend(xyz_from_line(line))
		newline.extend([blah[n][3],blah[n][4]])
		for feat in feats:
			if blah[n][2] in feat:
				newline.extend(get_all_features(featurefile)[feat])
		newlines.append(str(','.join(newline)))
		newline=[]
	return newlines	
			
# things = open(featurefile,'r').readlines()[2]
# stuff = parse_table_with_headers(featurefile)[1]
# print things, stuff 

final_lines = []
ili_headers = ['Name', 'x','y','z','radii', 'intensity']
ili_headers.extend(get_all_features(featurefile)['features'])
final_lines.append(','.join(ili_headers))	

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