# +
import pyautogui
import pyperclip
import os
import sys

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

if (w, h) == (W, H):
    pass
else: 
    dw, dh = W/w, H/h
    LocationKeys = Analystlocations.keys()
    NewLocations = [[w*dw, h*dh] for w,h in [Analystlocations[i] for i in Analystlocations]]
    NewAnalystLocations = dict(zip(LocationKeys, NewLocations))
    Analystlocations = NewAnalystLocations


FileButtonImagePath = 'file.png'
if os.path.exists(FileButtonImagePath) == False:
	print('no file button image. \n locate or use "FileButton" values in the "AnalystLocaitons" dictionary.')



InputList = [
		['testietest1', 123.053],['testietest2', 123.053],
		# ['A316', 225.058],
		# ['A327', 399.255],
		# ['A327', 423.278],
		# ['B133', 133.048],
		# ['B133', 175.093],
		# ['C246', 339.263],
		# ['C246', 679.533],
		# ['C252', 387.363],
		# ['D232', 168.993],
		# ['D232', 214.998],
		# ['D246', 161.078],
		# ['D247', 115.073],
		# ['D247', 161.078],
		# ['D249', 179.053],
		# ['E115', 105.018],
		# ['E115', 80.995 ],
		# ['E128', 115.073],
		# ['E128', 161.078],
		# ['F093', 259.023],
		# ['F093', 281.005],
		# ['F095', 163.063],
		# ['F095', 209.068],
		# ['G112', 105.023],
		# ['G112', 151.028],
		# ['G156', 259.023],
		# ['G156', 305.028],
		# ['G170', 193.033],
		# ['H151', 103.043],
		# ['H151', 149.048],
		# ['H153', 103.003],
		# ['H153', 149.008],
		# ['I037', 179.053],
		# ['I037', 225.058],
		# ['I045', 115.043],
		# ['I045', 161.048],
		# ['I053', 101.063],
		# ['I053', 147.068],
		# ['I071', 157.052],
		# ['I071', 175.063],
		# ['I072', 175.093],
		# ['I072', 87.043 ],
		# ['K115', 115.043],
		# ['K115', 161.048],
		# ['L061', 425.383],
		# ['L061', 471.388],
		# ['L069', 101.023],
		# ['L069', 147.028],
		# ['M003', 341.113],
		# ['M003', 387.118],
		# ['M162', 341.113],
		# ['M162', 387.118],
		# ['M188', 103.003],
		# ['M225', 179.053],
		# ['M225', 225.058],
		# ['M239', 115.073],
		# ['M239', 161.078],
		# ['M240', 115.073],
		# ['M240', 161.078],
		# ['M251', 129.053],
		# ['M251', 175.058],
		# ['O042', 112.992],
		# ['O042', 131.003],
		# ['O042', 263.013],
		# ['P248', 399.238],
		# ['P248', 707.473],
		# ['P254', 166.973],
		# ['P266', 746.573],
		# ['P266', 792.578],
		# ['P269', 119.078],
		# ['S222', 103.043],
		# ['S222', 149.048],
		# ['S223', 103.043],
		# ['S223', 149.048],
		# ['S225', 179.053],
		# ['S225', 225.058],
		# ['T242', 139.013],
		# ['T251', 179.053],
		# ['T251', 225.058],
		# ['V018', 147.068],
]



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

# +


    
# -

for i in InputList:
	inhouse = i[0]
	Q1 = i[1]
	Mmax = int((Q1 // 50 + 1) *50)
	Mmin = 45
	
	filename = "200701_MS2_DFI_%s_MZ%s_Neg" % (inhouse, str(int(Q1)))
	methodpaste = "%s\t%s" % (str(Mmin), str(Mmax))




	pyautogui.click(Analystlocations['NeutralLeft'])
	#pyautogui.hotkey('ctrl', 's')


	#save as new file
	pyautogui.click('file.png')
	pyautogui.moveTo(45, 266, duration=1, tween=pyautogui.easeInOutQuad)
	pyautogui.click()
	pyautogui.typewrite(filename)
	pyautogui.press('enter')

	#change method
	pyautogui.click(Analystlocations['MSmethod_1'])
	SetMethod()

	pyautogui.click(Analystlocations['MSmethod_2'])
	SetMethod()



	pyautogui.hotkey('ctrl', 's')


if __name__ == '__main__':
	print("writting MS1 methods from hard-coded input list\nMake sure Analyst is open, locked to left of primary monitor, and that at good template method is open.")

	#createMS2methods(InputList)

