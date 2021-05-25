# +
import pyautogui
import pyperclip
import os
import sys
import pandas as pd
from pandas.api.types import is_float_dtype
from pandas.api.types import is_string_dtype
from pandas.api.types import is_number


pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True


# +
## Move to MyTools folder to import DF's fileio solution. then move back. 
path  = os.path.abspath('.')
mytools = 'C:\\Users\\dfloros\\OneDrive\\Thesis\\Thesis\\Tools\\Mytools'
os.chdir(mytools)

from opendf import opendf

os.chdir(path)
# -

dfs = opendf('.')
df = dfs[list(dfs.keys())[0]]

df.loc[1]

# +

df['Fragments (low)'] = (df['Fragments (low)'].str.strip("?.! ,").str.split(','))
# -

[i.strip("?.! ,") for i if '?' not in i in in df['Fragments (low)'][22]]





from pandas.api.types import is_float_dtype
from pandas.api.types import is_string_dtype
from pandas.api.types import is_number


# +

def make_CE_MRMs(Q3, CErange='Both'):
	out = []
	if CErange == 'Both':
		rng = range(10, 120, 5)
	if CErange == 'low':
		rng = range(10, 50, 5)
	if CErange == 'High':
		rng = range(40, 120, 5)
	else: 
		rng = CErange
	#print(Q3)
	m = float(Q3) -0.1
	
	for i in rng:
		out.append([round(m,5),i])
		m+=0.01
	return out


# +


def generate_transitions(df):
	'''
	Remember to initialize a dictionary for the transitions
	'''
	try: 
		CEDP_methods
	except NameError:
		CEDP_methods = {}
	  

	EP = 10
	CXP = 4
	Time = 5
	
	
	for idx in range(len(df)):
		ln = df.loc[idx]
		inhouse = ln['inhouse'].strip()
		chemname = ln['name'].strip().capitalize()
		adduct = ln['Adduct'].strip()
		Q1 = ln['Q1'].round(5)
		Q1s = str(int(ln['Q1'].round()))
	  
		if is_number(ln['Fragments (low)']) == True:
			fl = [ln['Fragments (low)']]
		else: 
			fl = [i.strip("?!. ,") for i in ln['Fragments (low)'].split(',')]
				
		if is_number(ln['Fragments (High)']) == True:
			fl = [ln['Fragments (High)']]
		else: fh = [i.strip("?.! ,") for i in ln['Fragments (High)'].split(',')]
		
		best_list = []
		
		## CE optimizations
		
		DP = 50
		method_string = ''
		method_name = f'200706_CEDP_%s_%s_MZ%s_Pos' %(inhouse, adduct, Q1s)
		
	   ################ 
		
		for frag in fl[:6]:
			#print(frag)
			
			
			if is_number(frag) == True:
				if pd.isna(frag) == True:
					fl.remove(frag)
					#print('1', fl)
				if is_string_dtype(frag) ==  True:
					try:
						float(frag)
					except: 
						#print('2', fl)
						fl.remove(frag)    
				else:
					try:
						Q3 = float(frag.strip("?. ,!"))
					except: 
						#print('3', fl)
						continue
						
			else: 
				fl.remove(frag)
				#print('4', fl)
				
				
				
			if len(fl) >=1:
				#print(Q1, frag, pd.isna(frag))


				for Q3, CE in make_CE_MRMs(frag, range(10,50, 5)):
					try: 
						Q3s = str(int(Q3))
					except:
						continue


					ID = f'%s_%s_%s_%s_DP%s_CE%s' %(inhouse, chemname, Q1s, Q3s, DP, CE)


					lowfstr = '\t'.join([str(x) for x in (round(Q1,2),round(Q3,3),Time,ID,DP,EP,CE,CXP)])
					method_string = method_string + lowfstr + '\n'
					#print((method_string))
			else: pass
			CEDP_methods[method_name] = method_string
			
			###################
			
		for frag in fh[:6]:
		#print(frag)
		
		
			if is_number(frag) == True:
				if pd.isna(frag) == True:
					fh.remove(frag)
					#print('1', fh)
				if is_string_dtype(frag) ==  True:
					try:
						float(frag)
					except: 
						#print('2', fh)
						fh.remove(frag)    
				else:
					try:
						Q3 = float(frag.strip("?. ,!"))
					except: 
						#print('3', fh)
						continue
						
			else: 
				fh.remove(frag)
				#print('4', fh)
				
				
				
			if len(fh) >=1:
				#print(Q1, frag, pd.isna(frag))


				for Q3, CE in make_CE_MRMs(frag, range(40,90, 5)):
					try: 
						Q3s = str(int(Q3))
					except:
						continue


					ID = f'%s_%s_%s_%s_DP%s_CE%s' %(inhouse, chemname, Q1s, Q3s, DP, CE)


					lowfstr = '\t'.join([str(x) for x in (round(Q1,2),round(Q3,3),Time,ID,DP,EP,CE,CXP)])
					method_string = method_string + lowfstr + '\n'
					#print((method_string))
			else: pass
			CEDP_methods[method_name] = method_string
		
		########
		
		
		if len(fl) >= 1:
			best_list.append(fl[0])
		if len(fh) >= 1:
			best_list.append(fh[0])
		if len(best_list) >= 1:
		
			hlswitch = 0
			for frag in best_list :
				if hlswitch >=1 :
					CE = 50                    
				else:
					CE = 25
				if is_number(frag) == True:
					if pd.isna(frag) == True:
						best_list.remove(frag)
						#print('1', best_list)
				if is_string_dtype(frag) ==  True:
					try:
						float(frag)
					except: 
						#print('2', best_list)
						best_list.remove(frag)    
				else:
					try:
						Q3 = float(frag.strip("?. ,!"))
					except: 
						#print('3', best_list)
						continue
					#	
					#else: 
					#	best_list.remove(frag)
					#	#print('4', best_list)
					
					
					
				if len(best_list) >=1:
				#print(Q1, frag, pd.isna(frag))
					for Q3, DP in make_CE_MRMs(frag, range(10, 130, 10)):
						try: 
							Q3s = str(int(Q3))
						except:
							continue
					ID = f'%s_%s_%s_%s_DP%s_CE%s' %(inhouse, chemname, Q1s, Q3s, DP, CE)
					lowfstr = '\t'.join([str(x) for x in (round(Q1,2),round(Q3,3),Time,ID,DP,EP,CE,CXP)])
					method_string = method_string + lowfstr + '\n'
					#print((method_string))
				else: pass
				CEDP_methods[method_name] = method_string
	return(CEDP_methods)


# -
generate_transitions(df)


# +



# -

fl = [float(i) for i in ln['Fragments (low)'].split(',')]
[make_CE_MRMs(i) for i in fl]





# +
W, H = 2560, 1440 #size of DF's monitor 
w, h = pyautogui.size() # Get the size of the primary monitor.


Analystlocations = {
	'FileButton'       : [40 , 40 ],
	'Saveas'           : [45 , 266], 
	'MSmethod_1'       : [255, 229],
	'MSmethod_2'       : [255, 250],
	'ProductOf'        : [516, 380], 
	'MethodFieldCorner': [616, 332], 
	'NeutralLeft'      : [841, 686]
}
# -

"""

if (w, h) == (W, H):
	pass
else: 
	dw, dh = w/W, h/H
	LocationKeys = Analystlocations.keys()
	NewLocations = [[int(w*dw), int(h*dh)] for w,h in [Analystlocations[i] for i in Analystlocations]]
	NewAnalystLocations = dict(zip(LocationKeys, NewLocations))
	Analystlocations = NewAnalystLocations
Analystlocations


"""

pyautogui.position()

FileButtonImagePath = 'file.png'
MSmethodButtonImagePath = 'MSmethod.png'
if os.path.exists(MSmethodButtonImagePath) == False:
	print('no file button image. \n locate or use "FileButton" values in the "AnalystLocaitons" dictionary.')



def SetMethod():
	"""
	Types the Q1 mass into the product field, then pastes at string into the 
	"""
	pyautogui.moveTo(Analystlocations['ProductOf'])
	pyautogui.doubleClick()
	pyautogui.typewrite(str(Q1))
	pyautogui.moveTo(Analystlocations['MethodFieldCorner'])
	pyautogui.click()
	pyperclip.copy(methodpaste)
	pyautogui.hotkey('ctrl', 'v')
	pyautogui.click()

import time


def SetMethod_MRM():
	"""
	Names the File, and pastes a string into the MRM paramters field. 
	"""
	
	pyautogui.moveTo(Analystlocations['MethodFieldCorner'], duration = 1.5)
	pyautogui.click()
#	pyautogui.press('enter')
	pyautogui.press('delete')
	pyperclip.copy(methodpaste)
	pyautogui.hotkey('ctrl', 'v')
	pyautogui.press('enter')
	pyautogui.hotkey('ctrl', 'v')
	time.sleep(40)
	pyautogui.press('enter')
    
	pyautogui.click()









# +
 print(
    Methods_dict[list(Methods_dict.keys())[0]],
"\n\n\n\n\n\n",

Methods_dict[list(Methods_dict.keys())[1]])

# +
Methods_dict = generate_transitions(df)

files = list(Methods_dict.keys())

for file in files:
	n=1
	filename = file
	methodpaste = Methods_dict[file]
	n+=1




	#pyautogui.click(Analystlocations['NeutralLeft'])
	#pyautogui.hotkey('ctrl', 's')


	#save as new file
	pyautogui.click('file.png')
	pyautogui.moveTo(45, 266, duration=1, tween=pyautogui.easeInOutQuad)
	pyautogui.click()
	pyautogui.typewrite(filename)
	pyautogui.press('enter')
	time.sleep(0.5)
	pyautogui.press('left')
	pyautogui.press('enter')

	#change method
	SetMethod_MRM()

	time.sleep(10)


	pyautogui.hotkey('ctrl', 's')


# +
## pyautogui.click('MSmethod.png')
# -

if __name__ == '__main__':
	print("writting MS1 methods from hard-coded input list\nMake sure Analyst is open, locked to left of primary monitor, and that at good template method is open.")

	#createMS2methods(InputList)

