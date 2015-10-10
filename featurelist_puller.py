import glob
import os

#feature_directory = "C:\Users\Dorrestein lab\Desktop\UCSD_LC-MS_Toolbox_Projects\UCSD_Amina_2D_mapping_Trace_Detection\Processing_150616_ALL_Time1_2\TOPPAS_out\004-FeatureFinderCentroided"

#os.chdir(feature_directory)

filenames = os.listdir('.')
things_i_want = []

for file in filenames[1:]:
	filelines = open(file,"r").readlines()
	
	for line in filelines:
		if "featureList count" in line:
			things_i_want.append(str("File %s has %s features." %(file, line[-6:-3])))
		
with open('outfile.txt', 'w') as outfile:
	outfile.write('\n'.join(things_i_want))