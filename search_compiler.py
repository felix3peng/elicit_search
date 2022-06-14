# -*- coding: utf-8 -*-
"""
Script to compile search results
Created on Tue Jun 14 12:46:14 2022

@author: Felix
"""

import pandas as pd
import os
import glob

# for each subtopic, load all csv files and join into a dataframe
master_path = os.getcwd()
result_folder = os.path.join(master_path, 'results')
subtopics = [1, 2, 3]


def load_df_from_folder(ind):
    folder = os.path.join(result_folder, 'subtopic' + str(ind))
    files = glob.glob(os.path.join(folder, '*'))
    dfs = [pd.read_csv(f, header=0, index_col=None) for f in files]
    compiled_df = pd.concat(dfs, ignore_index=True)
    return compiled_df


try:
    all_dfs
    pass
except NameError:
    all_dfs = []
    for i in subtopics:
        all_dfs.append(load_df_from_folder(i))

# for each subtopic, identify number of duplicates and number unique results
all_dfs_dedup = []
n_uniques = []
for i in range(len(all_dfs)):
    df = all_dfs[i]
    num_records = len(df)
    df_dedup = df.drop_duplicates()
    num_unique = len(df_dedup)
    all_dfs_dedup.append(df_dedup)
    n_uniques.append(num_unique)

# across all subtopics, identify number of unique results
master_df = pd.concat(all_dfs, ignore_index=True)
master_df_dedup = master_df.drop_duplicates()
num_unique_total = len(master_df_dedup)
