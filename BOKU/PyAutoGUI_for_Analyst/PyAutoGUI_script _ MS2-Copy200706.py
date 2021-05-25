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
# #+ -
from pandas.api.types import is_float_dtype
from pandas.api.types import is_string_dtype
from pandas.api.types import is_number
import time

## open the first df, name df
dfs = opendf('.')
negdf = dfs[list(dfs.keys())[0]]
posdf = dfs[list(dfs.keys())[1]]
negdf


# -


posdf


# +

def make_CE_MRMs(Q3, CErange='Both'):
	"""
	give this a range generator in 2arg to define the range and steps of CE. generates a list of masses differing by 0.01mz and associates them with each CE step
	could be used for any parameter...
	"""
	
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


# -

def fragment_cleaning(fl):
    for frag in fl:    
            if is_number(frag):
                if pd.isna(frag):
                    fl.remove(frag)
                    #print('1', fl)

            elif is_string_dtype(frag) ==  True:
                try:
                    Q3 = float(frag.strip("?. ,!")
                except: 
                    #print('2', fl)
                    fl.remove(frag)    
            else: 
                fl.remove(frag)
                #print('4', fl)

            if len(fl) >=1:
                if n == 0: 
                    best_list.append(frag)
                    n += 1
                else:
                    continue
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



# +


def generate_transitions(df, polarity = 'Pos'):
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
    polarity = polarity.capitalize()
    

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
        method_name = f'200706_CEDP_%s_%s_MZ%s_%s' %(inhouse, adduct, Q1s, polarity)

       ################ 

        for frag in fl[:6]:
            n = 0 


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
                if n == 0: 
                    best_list.append(frag)
                    n += 1
                else:
                    continue

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
            n=0


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
                if n == 0: 
                    best_list.append(frag)
                    n += 1
                else:
                    continue


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


    #		if len(fl) >= 1:
    #			best_list.append(fl[0])
    #		if len(fh) >= 1:
    #			best_list.append(fh[0])
        if len(best_list) >= 1:
            if len(best_list)>= 2:
                best_list = best_list[:2]
            CE = 35
            Q1 = Q1 +.01
            for frag in best_list :
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



                if len(best_list) >= 1:
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


methdict = generate_transitions(neg)
newdict = {}
for key in list(methdict.keys()):
	
	df = pd.DataFrame([i.split('\t') for i in methdict[list(methdict.keys())[0]].split('\n')], columns=['Q1','Q3','Time','ID','DP','EP','CE','CXP'])
	df = df.sort_values(['Q1', 'Q3']).dropna()
	newdict[key]=df_to_string(df)
newdict


##final implementation
def string_to_df_and_sort(methstring):
    try:
        df = pd.DataFrame([i.split('\t') for i in methstring.split('\n')], columns=['Q1','Q3','Time','ID','DP','EP','CE','CXP'])
        df = df.sort_values(['Q1', 'Q3'])#.dropna()
    except AssertionError:
        df  =  pd.DataFrame([i.split('\t') for i in methstring.split('\n')])
        #print(methstring[:20])
    return df


def df_to_string(df):
	x = ''
	df = df.astype(str)
	for i in range(len(df)):
		x = x + ('\t'.join(list(df.iloc[i]))) + '\n'
	return x


methods = generate_transitions(posdf)
files = list(methods.keys())
x = []
for file in files:
	methstring = methods[file]
	methstring = string_to_df_and_sort(methstring)
	methstring = df_to_string(methstring)
	print( file),  x.append(methstring)

x.index(min(x))

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


def SetMethod_MRM(methodstring):
	"""
	Names the File, and pastes a string into the MRM paramters field. 
	"""
	
	pyautogui.moveTo(Analystlocations['MethodFieldCorner'], duration = 1.5)
	pyautogui.click()
#	pyautogui.press('enter')
	pyautogui.press('delete')
	pyautogui.click(Analystlocations['NeutralLeft'])
	pyperclip.copy(methodstring)
	pyautogui.hotkey('ctrl', 'v')
#	pyautogui.press('enter')
#	pyautogui.hotkey('ctrl', 'v')
	#time.sleep(30)
	pyautogui.press('enter')
	
	pyautogui.click()

# +
#D:\Analyst Data\Projects\Corona\Acquisition Methods\neg 200708

fnames = os.listdir('D:\\Analyst Data\\Projects\\Corona\\Acquisition Methods\\neg 200708')
fnames = [f.split('.')[0] for f in fnames]
fnames
for f in fnames:
    if f in files:
        pass
    else: 
        print(f)


# +
dfs = opendf('.')
df = dfs[list(dfs.keys())[0]]

Methods_dict = generate_transitions(df)

Methods_dict
# -

fnames = os.listdir('D:\\Analyst Data\\Projects\\Corona\\Acquisition Methods\\neg 200708')
fnames = [f.split('.')[0] for f in fnames]
for f in fnames:
    print(f)
    print(df[f])


for pk in printkeys:
    try: 
        df = pd.DataFrame([i.split('\t') for i in Methods_dict[pk].split('\n')],
                        columns=['Q1','Q3','Time','ID','DP','EP','CE','CXP'])
    except:
        print(pk, )
        continue
    #print(Methods_dict[pk])
    df['Q1']=pd.to_numeric(df['Q1'])
    df['Q3'] = pd.to_numeric(df['Q3'])
    df = df.sort_values(by = ['Q1', 'Q3'], ascending = True).dropna()


# +
dfs = opendf('.')
df = dfs[list(dfs.keys())[0]]

Methods_dict = generate_transitions(df)

files = list(Methods_dict.keys())

sleep_time = 2
num_retries = 20

files = [file for file in files if file not in fnames]
for file in files:
    try:
        df = pd.DataFrame([i.split('\t') for i in Methods_dict[file].split('\n')],
                            columns=['Q1','Q3','Time','ID','DP','EP','CE','CXP'])
    except:
        print(file)
    df['Q1']=pd.to_numeric(df['Q1'])
    df['Q3'] = pd.to_numeric(df['Q3'])
    df = df.sort_values(by = ['Q1', 'Q3'], ascending = True).dropna()
    ##neg mode!!
    for i in ['DP','EP','CE','CXP']:
        df[i] = pd.to_numeric(df[i])
        df[i] = df[i].apply(lambda x: -x)
    
    ##neg mode close
    Methods_dict[file]=df_to_string(df)
 #   if df.DP[0 ] >= 0 :
  #      print('file')
   #     df.DP.apply(lambda x:-x, )
    #    zz = df
        
        


# +
###Final Method?

dfs = opendf('.')
df = dfs[list(dfs.keys())[0]]

Methods_dict = generate_transitions(df)

files = list(Methods_dict.keys())

sleep_time = 2
num_retries = 20

files = [file for file in files if file not in fnames]

for file in files:
#	if file not in fnames:
#		continue
#	else:
#		pass
#	if Methods_dict[file]: 

		
		try:
			df = pd.DataFrame([i.split('\t') for i in Methods_dict[file].split('\n')],
								columns=['Q1','Q3','Time','ID','DP','EP','CE','CXP'])
		except:
			print(Methods_dict[file])
		df['Q1']=pd.to_numeric(df['Q1'])
		df['Q3'] = pd.to_numeric(df['Q3'])
		df = df.sort_values(by = ['Q1', 'Q3'], ascending = True).dropna()
		##neg mode!!
		for i in ['DP','EP','CE','CXP']:
			df[i] = pd.to_numeric(df[i])
			df[i] = df[i].apply(lambda x: -x)
		##neg mode close
		Methods_dict[file]=df_to_string(df)

	
	
		n=1
		filename = file
		methodpaste = Methods_dict[file]
		n+=1
		     

		pyautogui.click(Analystlocations['NeutralLeft'])
		#pyautogui.hotkey('ctrl', 's')
		#change method
		SetMethod_MRM(methodpaste)
		time.sleep(10)
		#pyautogui.hotkey('ctrl', 's')
        
        
		for x in range(0, num_retries):
			try:
				pyperclip.copy(methodpaste)
				cpy_error = None
			except:
				cpy_error = True
				#pyautogui.hotkey('ctrl', 's')
				pass
			
			if cpy_error:
				time.sleep(sleep_time)
				print('copy error, retrying')
			else: 
				print('copy erorr resolved - saving')
				pass

		#save as new file
		pyautogui.click('file.png')
		pyautogui.moveTo(45, 266, duration=1, tween=pyautogui.easeInOutQuad)
		pyautogui.click()
		pyautogui.typewrite(filename)
		pyautogui.press('enter')
		time.sleep(0.5)
		#pyautogui.press('left')
		pyautogui.press('enter')
		pyautogui.press('enter')
		pyautogui.press('enter')


# +
dfs = opendf('.')
df = dfs[list(dfs.keys())[0]]

Methods_dict = generate_transitions(df)

files = list(Methods_dict.keys())


# +
###final implemention

def method_dic_clean_and_sort(df, polarity = 'pos', filepath = None):
    """Sorts by Q1, Q3. and sets CE,DP etc valued to opposite sign if set polarity to 'neg'.  """
    
    polarity = polarity.lower()
    
    Methods_dict = generate_transitions(df, polarity = polarity)
    files = list(Methods_dict.keys())
    
    for file in files:
        
        methstring = Methods_dict[file]

        df = string_to_df_and_sort(methstring)
        
        
      
        
        if polarity == 'neg':
            for i in ['DP','EP','CE','CXP']:
                df[i] = pd.to_numeric(df[i])
                df[i] = df[i].apply(lambda x: -x)

        elif polarity == 'pos':
            pass
        else:
            print('no polarity keyword passed - please choose set to neg, pos or leave blank for pos.')
        

        #Record methods to csv files
        if filepath:
            if os.path.exists(filepath) == False:
                os.mkdir(filepath)
            df.to_csv(f'%s\%s.csv' %(filepath, file), index= False)

        
        Methods_dict[file]=df_to_string(df)



        
        filename = file
        methodpaste = Methods_dict[file]


# -

method_dic_clean_and_sort(posdf, polarity='Pos', filepath='PosMethods_130720')

method_dic_clean_and_sort(negdf, polarity='Neg', filepath='NegMethods_130720')

negdf

# +

method_dic_clean_and_sort(negdf, polarity='Neg', filepath='testn_130720')


# +


method_dic_clean_and_sort(dfpos, polarity='Pos', filepath = 'testp_130720')

# +
polarity = 'pos'
polarity = polarity.lower()



if polarity == 'neg': 
        print('ow')
elif polarity == 'pos':
        print(polarity)    
else:
    print('moo')


# -

def stringify(a):
		if is_number(a):
			b = str(int(round(a,0)))
		elif type(a) == type([]):
			b = [str(int(round(i,0))) for i in a]
		return b

# +



a = fraglist_combiner([[163.2, 145.0, 91.1, 127.4, 181.2, 115.0, 102.8],[85.1, 97.4, 72.9, 61.0, 69.1, 91.3, 101.2, 80.7, 57.2
]])
sum([len(i) for i in a])

# -

def fraglist_clearner(fraglist):
	for frag in fraglist:
				n=0
			
			
				if is_number(frag) == True:
					if pd.isna(frag) == True:
						fraglist.remove(frag)
						#print('1', fraglist)
				elif is_string_dtype(frag) ==  True:
					try:
						float(frag)
					except: 
						#print('2', fraglist)
						fraglist.remove(frag)    
				else:
					try:
						frag = float(frag.strip("?. ,!"))
					except: 
						#print('3', fraglist)
						continue
							
				else: 
					fraglist.remove(frag)
					#print('4', fraglist)
					
	if len(fraglist) >= 1:
		return fraglist
	elif len(fraglist) == 1:
		return [fraglist]
	else:
		return None


def fraglist_combiner(fraglists, pick_best_by_order = True):
	"""fraglists should be 2 lists of fragment masses in increasing CE voltage - outputs [low, high, both, best] lists"""
	fl = fraglists[0]
	fh = fraglists[1]
	fboth = []
	best_list = []
	
	fraglists = [fl,fh, fboth, best_list]
	
	
	flset, fhset, fbset = set(stringify(fl)), set(stringify(fh)), set(stringify(fboth))
	
	for frag in fl:
		frtoken = stringify(frag)
		if frtoken in fhset:
			fboth.append(frag)
			fl.remove(frag)
			fh.remove(min(fh, key= lambda x:abs(x-frag)))
			flset, fhset, fbset = set(stringify(fl)), set(stringify(fh)), set(stringify(fboth))
		elif frtoken in fbset:
			fl.remove()
		
		else:
			if frag == fl[0]:
				best_list.append(frag)
			pass
	
	flset, fhset, fbset = set(stringify(fl)), set(stringify(fh)), set(stringify(fboth))
	
	for frag in fh:
		frtoken = stringify(frag)
		if frtoken in flset:
			fboth.append(frag)
			fh.remove(frag)
			fl.remove(min(fl, key= lambda x:abs(x-frag)))
			flset, fhset, fbset = set(stringify(fl)), set(stringify(fh)), set(stringify(fboth))
		elif frtoken in fbset:
			fh.remove()
		else:
			if frag == fh[0]:
				best_list.append(frag)
			pass
	
	if fboth:
		best_list.append(fboth[0])


	for fraglist in fraglists:
		if fraglist:
			pass
		else:
			fraglist = []
			
	if pick_best_by_order:	
		return fraglists
	else:
		return fraglists[:3]

if []:
    print(stringify([2]))

if __name__ == '__main__':
	print("writting MS1 methods from hard-coded input list\nMake sure Analyst is open, locked to left of primary monitor, and that at good template method is open.")

	#createMS2methods(InputList)

