#!/usr/bin/python
#	tool for selecting the top 1000 contig fragments of an assembly. 
#	meant as a preliminary action to antismash.  
import os as os

# add path of assembled contig fasta files
# path = 'afp://alex@dorresteinnas01.ucsd.edu/SharedFolder/Dimitri/Python'

# os.chdir(path)

infiles = []
for i in os.listdir('.'):
	if 'filtered_contigs' in i: pass
	elif '.fasta' in i: 
		infiles.append(i)
	else: pass


#outfile_path = os.mkdir('path to results file') # if blank will place them where the python script is being run from


size_cuttoff = 1 			# minimum contig length to include in the altered contig list
n_cuttoff = 1000			# maximum number of contigs to take forward


#these cuttoffs are applied in the following function that returns the longest 1000 contigs	

def get_sorted_contigs(str):		
	contigs = str.split('>')
	lens = []
	big_contigs = []
	print_tigs = []
	if len(contigs) <= n_cuttoff:	#in case there are less contigs than the cutoff, this will pass them all to the new fasta file
		for contig in contigs:
			if 'NODE' not in contig : pass
			elif 'NODE' in contig :
				print_tigs.append('>%s\n'%(contig.rstrip()))
	else:	
		for contig in contigs:
			if 'NODE' not in contig : pass	#safety for blank lines or comments (all  may not be compatible with other assemblers
			elif 'NODE' in contig :
				things = contig.split('_')
				if int(things[3]) >= size_cuttoff:
					lens.append(int(things[3]))
					big_contigs.append(contig)
				else : pass
				
		contig_touples = zip(big_contigs, lens)
		sorted_contigs = sorted(contig_touples, key=lambda contig: contig[1], reverse = True) #sorts the contigs based on length big to small
		
		for i in sorted_contigs[:n_cuttoff]:
			print_tigs.append('>%s\n'%(i[0].rstrip()))
	return print_tigs



for file in infiles:
	with open(file,'r') as infile:
		string = infile.read()
	contigs = get_sorted_contigs(string)
	header = "#\tdimitri's filtered contigs for use in antismash web\n#\tThis file was derived from '%s' and containts %i contigs of length %i or higher.\n\n" %(file, len(contigs), size_cuttoff)
	with open('%s_filtered_contigs.fasta' %(file.split('.')[0]), 'w') as outfile:
		outfile.write(header)
		outfile.write('\n'.join(contigs))


#end
