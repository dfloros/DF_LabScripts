import os
import time
from itertools import product

import numpy as np
import pandas as pd
import rdkit as rd

import dtale as dt
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import plotly.express as px




def extractandaddInHouse(df, colnames=['InHouse', 'Name', 'Source', 'Transition']):
    """#imports and expands ID tab into Inhouse,Chem Name, etc  - TODO add Q1/Q3 to ID names - or make an ID out function."""
    tempdf = df['ID'].str.split('_', expand=True)
    tempcols = list(tempdf.columns)
    df[colnames[0]] = tempdf[0]  # .str.match('[a-zA-Z]{1}[0-9]{3}')
    df[colnames[1]] = tempdf[1]
    df[colnames[2]] = tempdf[3]
    df[colnames[3]] = tempdf[2]


def PolaritySplitter(df):
    """Takes df, returns two dfs split on pos/neg in the 'Pol' column. """
    df['Pol'] = df['Pol'].str.capitalize()
    
    dfPos = df.loc[df['Pol']=='Pos', :]
    dfNeg = df.loc[df['Pol'] == 'Neg', :]
    
    return [dfPos, dfNeg]


def CompareTransitions_DF(df1, df2, threshold=0.5, OutCols=["Literature Confirmed", 'Source(s)', "Unique Transition"], LitHasInHouse=True):
    """
    Uses two dfs looking for matching q1, q3 columns, reqires InHouse lables in both.
     
     Could also be used to return arbitrary list of attributes from df2.
     """""
    # TODO this is probably unneeded make an in-df compare-er instead

    outdf = df1  # .reindex(columns = df1.columns.tolist() + OutCols)

    if LitHasInHouse == True:
        Comps = set(list(df1['InHouse']))
        for comp in Comps:
            L1s = set(df2.loc[df2['InHouse'] == comp, "Q1"])
            L3s = set(df2.loc[df2['InHouse'] == comp, "Q3"])
            Sources = set(df2.loc[df2['InHouse'] == comp, "Source"])
            for i, j in product(L1s, L3s):
                outidx = df1.query("abs(`Q1`- @i) < @threshold & abs(`Q3`- @j) < @threshold").index
                # Notidx = df1.query("abs(`Q1`- @i) > @threshold").index
                uniqueidx = df1.query("abs(`Q1`- @i) < @threshold & abs(`Q3`- @j) > 2*@threshold").index

                outdf[OutCols[0]][outidx] = True
                outdf[OutCols[2]][uniqueidx] = True
                outdf[OutCols[1]][outidx] = str(Sources)

        return outdf

    if LitHasInHouse == False:
        L1s = set(df2["Q1"])
        L3s = set(df2["Q3"])
        for i, j in product(L1s, L3s):
            outidx = df1.query("abs(`Q1`- @i) < @threshold & abs(`Q3`- @j) < @threshold").index
            # Notidx = df1.query("abs(`Q1`- @i) > @threshold").index
            uniqueidx = df1.query("abs(`Q1`- @i) < @threshold & abs(`Q3`- @j) > 2*@threshold").index
            # outdf[OutCols[0]][Notidx] = False
            outdf[OutCols[0]][outidx] = True
            outdf[OutCols[2]][uniqueidx] = True

        return outdf
    
    
#
#
# def Adduct_Calculator(df, AdductCSVpath = './Tools/simplifiedFiehnLabAdducts.csv'):
#     outDF = df
#
#     Adducts = PolaritySplitter(pd.read_csv(AdductCSVpath))
#     PosAdd = Adducts[0]
#     NegAdd = Adducts[1]
#
#     Trans = PolaritySplitter(df)
#     PosTrans = Trans[0]
#     NegTrans = Trans[1]
#
#     temp = []
#     mlist = []
#
#     for Polarity, AdductSubset in Trans, Adducts:
#         temp = []
#         mlist = []
#         for M in Polarity['Mono Mass']:
#             mlist = []
#             for form in AdductSubset['Formula']:
#                 mlist.append(eval(form))
#             temp.append(mlist)
#         tempdf = pd.DataFrame(temp, columns=list('Adduct_' + AdductSubset['Adduct']))
#         outDf.join(tempdf)
#
#     return outDF
#
#
#     outcol = []
#     Correctcol = []
#     Threshold = 2
#
#     for i in range(len(IFAdf)):
#
#
#         comp = IFAdf['InHouse'][i]
#         Q1 = IFAdf['Q1'][i]
#         output = []
#         Corrected = []
#         ppms = [Threshold * 2000000]
#
#         subDF = AttrWadductsdf.loc[Attrdf['InHouse'] == comp, Adducts]
#
#         for Add in Adducts:
#             # while len(output)<1:
#
#             if len(list(subDF[Add])) > 0:
#                 Tmass = list(subDF[Add])[0]
#                 ppm = round(abs(Tmass - Q1) * (1000000), 2)
#                 ppms.append(ppm)
#                 a = Add.split('_')[1]
#
#                 if abs(Tmass - Q1) < Threshold:
#
#                     if ppm <= min(ppms):
#                         output.insert(0, f'{a} :Q1 = {Q1}, Theoretical = {Tmass}, PPM = {ppm}')
#                         Corrected.insert(0, Tmass)
#                     else:
#                         output.append(f'{a} :Q1 = {Q1}, Theoretical = {Tmass}, PPM = {ppm}')
#                         if abs(Tmass - Q1) > 0.1:
#                             Corrected.append(Tmass)
#                         else:
#                             Corrected.append('')
#
#
#             else:
#                 pass
#         if len(output) > 0:
#             outcol.append(output[0])
#             Correctcol.append(Corrected[0])
#         else:
#             outcol.append('No Match')
#             Correctcol.append("")


def Adduct_Calculator(df, AdductCSVpath='./Tools/simplifiedFiehnLabAdducts.csv'):
    outdf = df
    temp = []
    Adducts = pd.read_csv(AdductCSVpath)
    for M in df['Mono Mass']:
        mlist = []
        for form in Adducts['Formula']:
            print
            mlist.append(eval(form))
        temp.append(mlist)
    tempdf = pd.DataFrame(temp, columns=list(Adducts['Pol'] + '_Adduct_' + Adducts['Adduct']))
    outdf.join(tempdf)
    
    return outdf

def GetMonoMass(df, Attrdf):
    masses = []
    Masslist = []
    for comp in df['InHouse']:
        masses.append(Attrdf.loc[Attrdf['InHouse']==comp, 'Mono Mass'])
    for mass in masses:
        Masslist.append(list(mass))
    df["Mono Mass"] = Masslist
    return df


def CorrectMassAndPPMfromAdducts(df, AdductCSVpath='../Tools/simplifiedFiehnLabAdducts.csv', Threshold=0.4):
    outcol = []
    Correctcol = []
    AddMasses = Adduct_Calculator(df, AdductCSVpath=AdductCSVpath)
    df = df.join(AddMasses)
    
    PosAdd = list(PolaritySplitter(Adducts)[0]['Adduct'])
    NegAdd = list(PolaritySplitter(Adducts)[1]['Adduct'])
    
    OutLables = ['Best Adduct', 'Theoretical Mass', 'Differnce(m/z)', 'ppm']
    
    for i in range(len(df)):
        Pol = df['Pol'][i]
        comp = df['InHouse'][i]
        Q1 = df['Q1'][i]
        
        output = []
        Corrected = []
        diffs = []
        
        if Pol == 'Pos':
            Adds = PosAdd
        if Pol == 'Neg':
            Adds = NegAdd
        
        for Add in Adds:
            diffs.append(abs(Q1 - df[Add][i]))
        a = Adds[diffs.index(min(diffs))]
        
        diff = min(diffs)
        Tmass = df.loc[i, a]
        ppm = round((abs(diff) / Tmass) * (1e6), 2)
        
        values = [a, Tmass, diff, ppm]
        
        if diff < Threshold:
            outcol.append(values)
        else:
            outcol.append(['No Match', '', '', ''])
    
    Outdf = pd.DataFrame(outcol, columns=OutLables)
    df = df.join(Outdf)
    
    return df



if __name__ == "__main__":
    CorrectMassAndPPMfromAdducts()



