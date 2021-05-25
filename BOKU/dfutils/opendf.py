import os
import pandas as pd

def opendf(path = '.', n = 0 ):
    """Shortcut for opening all csv and excel dfs. Returns a dict of names and dfs. """
    frame = []
    keys = []
    for file in os.listdir(path):
        ext = file.split('.')[-1]
        name = file.split('.')[0]
        if ext == 'xlsx':
            frame.append(pd.read_excel(file))
            keys.append(name)
        if ext == 'csv':
            frame.append(pd.read_csv(file))
            keys.append(name)
        if ext == 'pickle' or ext =='pkl':
            frame.append(pd.read_pickle(file))
        if ext == 'txt' or ext == 'tsv':
            frame.append(pd.read_csv(file, sep='\t'))
        else:
            pass
    return dict(zip(keys, frame))




if __name__ == '__main__':
    print("Running opendf in this directory. \n"
          "Will retrun an array of pandas dataframes from any csv, xlsx, and pickle data. ")
    opendf()





