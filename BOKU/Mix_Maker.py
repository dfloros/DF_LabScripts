#!/usr/bin/env python
# coding: utf-8

"""
Making_Mix_Methods.py Traff.xlsx Trans.xlsx Mixes.xlsx

where 'Traff' contains the names/abbreviations/inhouse numbers,
'Trans' contains all MRM transitions, and 'Mixes' contains a key of mixes.
Only excel files will work. A dictionary of class(Mixture) objects will be returned
"""

import pandas as pd
import os
import sys
import time
import pprint

import warnings
warnings.filterwarnings('ignore')




def round_string(x):
    return str(int(x.round(0)))


def get_the_date():
    y, m, d = time.localtime()[:3]
    y = str(y)[:-2]
    m = str(m)
    d = str(d).rjust(2, '0')
    ymd = (y + m + d)
    return ymd


ymd = get_the_date()


def get_num_ztrans(df):
    return len(df.loc[df.Q1 - df.Q3 < 1])


class Mixture:
    """self.comp are the inhouse numbers, self.trans are the transitions"""

    def __init__(self, InHouse, transitions):
        # self.name = str(self)
        self.comp = list(InHouse)
        self.trans = pd.DataFrame(transitions)

    def get_mixes(mix_containing_df, tranition_containing_df):
        m = sorted(list(set(mix_containing_df["Mixes"])))
        mixdict = {}

        for mix in m:
            # print list(mixes.loc[mixes['Mixes'].is mix]['InHouse'])
            c = mix_containing_df.loc[mix_containing_df['Mixes'] == mix]['InHouse']
            t = tranition_containing_df.loc[tranition_containing_df['InHouse'].isin(c)].sort_values(['Q1', 'Q3'])

            mixdict[str(mix)] = Mixture(c, t)

        return mixdict


mixes_file = 'Mixes_DF.xlsx'
traff_file = './201007/201007_TRAFFIC_LIGHT.xlsx'
trans_file = './201007/201007_Final transitions.xlsx'

mixes = pd.read_excel(mixes_file)
traff = pd.read_excel(traff_file)
trans = pd.read_excel(trans_file)


def load_and_clean_excels(mixes_file, traff_file, trans_file):
    mixes = pd.read_excel(mixes_file)
    traff = pd.read_excel(traff_file)
    trans = pd.read_excel(trans_file)

    # Clean Transitions
    # Add EP (entrance potential) with proper negative, round Q1,Q3

    try:
        len(trans.Inhouse)
    except:
        try:
            len(trans.InHouse)
        except KeyError:
            trans['Inhouse'] = trans['ID'].str[:4]

            print(
                "Warning: No 'InHouse' col in the transition excel file.\n\nFirst 4 characters of 'ID' will be used.\n")

    trans.rename(columns={'pos/neg': 'Pol',
                          'Inhouse': 'InHouse',
                          'Comment / Intensity': 'Intensity',
                          'Done by': 'Source'},
                 inplace=True)

    trans['Time'] = 5
    trans['EP'] = 10

    trans.loc[trans['Pol'] == 'neg']['EP'] = -10
    trans[['Q1', 'Q3']].round(1)

    trans_params_list = ['InHouse',
                         'Pol',
                         'Q1',
                         'Q3',
                         'Time',
                         'ID',
                         'DP',
                         'EP',
                         'CE',
                         'CXP',
                         'Intensity',
                         'Source']

    clean_trans_df = trans[trans_params_list]

    # Cleaning traffic light list

    traff.drop(traff.loc[traff['InHouse'].str.contains('(dup)')].index,
               inplace=True)
    traff.rename(columns={'Abbreviations': 'Abbr'},
                 inplace=True)
    traff['Abbr'] = traff['Abbr'].str.strip()

    traff_params_list = ['InHouse',
                         'ChemName',
                         'Abbr',
                         'Stereochem']

    clean_traff_df = traff[traff_params_list]

    # Merging abbreviations etc into transition list - merging on 'InHouse', all transitions need an 'Inhouse'

    merge_df = clean_trans_df.merge(clean_traff_df, on='InHouse')

    finaldf = merge_df.copy().sort_values('ID')

    for i in finaldf.index:
        row = finaldf.loc[i]
        Abbr = str(row['Abbr'])
        q1s = round_string(row['Q1'])
        q3s = round_string(row['Q3'])

        if row['Source'] == 'Biocrates':
            Abbr = str(Abbr + '(Bio)')

        finaldf.at[i, 'ID'] = "_".join([row['InHouse'], Abbr, q1s, q3s])

    finaldf = finaldf[
        ['Q1', 'Q3', 'Time', 'ID', 'DP', 'EP', 'CE', 'CXP', 'Pol', 'InHouse', 'Intensity', 'Source', 'ChemName', 'Abbr',
         'Stereochem']]

    final_trans_clean = finaldf.iloc[:, :10]

    return final_trans_clean


def zero_trans_constructor(df):
    df2 = df.copy()
    for a in list(set(df.Q1)):
        test = df.loc[df.Q1 == a].head(1).copy()
        test['Q3'] = test.Q1
        x, y, z, bla = list(test.ID.str.split('_'))[0]
        test['ID'] = '_'.join([x, y, z, z])
        if (test.Pol == 'pos').any():
            test['CE'] = 5
        elif (test.Pol == 'neg').any():
            test['CE'] = -5
        df2 = df2.append(test)
        df2 = df2.reset_index().drop(['index'], axis=1)

    return df2


def fix_duplicate_masses(df, limit=300, increment=0.001):
    origcols = list(df.columns)
    df['trans'] = ''
    for i in df.index:
        df['trans'][i] = str(df['Q1'][i]) + '_' + str(df['Q3'][i])

    counter = 0
    duplist = df.duplicated(subset='trans', keep='first')

    while duplist.any():
        counter += 1

        df2 = df.loc[duplist]['Q3'].apply(lambda x: x + increment)
        df.Q3[duplist] = df2

        for i in duplist.index:
            df['trans'][i] = str(df['Q1'][i]) + '_' + str(df['Q3'][i])

        duplist = df.duplicated(subset='trans', keep='first')

        # print(counter)
        if counter >= limit:
            print(f'there are more than {limit} duplicates.\nSomething is wrong.')
            break

    print(
        f'There were {counter} sets of duplicates.\n {increment} was added to each Q3 until there were no collisions.')

    return df[origcols]


def save_full_clean_transitions(final_trans_clean):
    ymd = get_the_date()
    filename = f'Final_Transitions_Cleaned_{ymd}.csv'
    final_trans_clean.to_csv(filename, index=False)
    return filename


def make_and_save_the_mixes(mixes, final_trans):
    ymd = get_the_date()

    mixdict = Mixture.get_mixes(mixes, final_trans)

    keys = list(mixdict.keys())

    m = sorted(list(set(mixes["Mixes"])))

    for key in keys:
        df = mixdict[key].trans
        dfp = df.loc[df.Pol == 'pos'].iloc[:, :8]
        dfn = df.loc[df.Pol == 'neg'].iloc[:, :8]
        if len(dfp) > 0:
            dfp.to_csv(f'{key}_pos_methods_{ymd}.csv', index=False)
        if len(dfn) > 0:
            dfn.to_csv(f'{key}_neg_methods_{ymd}.csv', index=False)

    return mixdict


if __name__ == '__main__':
    if len(sys.argv) != 4 and sys.argv[1] == '--help':
        print(__doc__)


    else:
        print('If there are any issues, please run as a notebook.')
        args = sys.argv[1:]

        mixes_file = args[0]
        traff_file = args[1]
        trans_file = args[2]

        ymd = get_the_date()
"""
        mixes = pd.read_excel(mixes_file)
        traff = pd.read_excel(traff_file)
        trans = pd.read_excel(trans_file)
"""
        merged_dataframe = load_and_clean_excels(mixes_file, traff_file, trans_file)
        print("Data Loaded...\n\n")

        merged_dataframe = zero_trans_constructor(merged_dataframe)
        print("Zero Transitions Constructed...\n\n")

        merged_dataframe = fix_duplicate_masses(merged_dataframe)
        print("Duplicate Masses dealt with...\n\n")

        full_tr_file = save_full_clean_transitions(merged_dataframe)

        print(f"Merged transitions saved locally in {full_tr_file}...\n\n")

        mixdict = make_and_save_the_mixes(mixes, merged_dataframe)

        mixes = list(mixdict.keys())

        for mix in mixes:
            M = mixdict[mix]
            if len(M.trans) == 0:
                pass
            else:
                print(f"{mix} is made of {len(M.comp)} compounds and {len(M.trans)} transitions... \n")

        mixdict

else:
    print("Running with default filepaths.")

