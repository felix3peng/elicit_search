# -*- coding: utf-8 -*-
"""
Script to compile search results
Created on Tue Jun 14 12:46:14 2022

@author: Felix
"""

import pandas as pd
import os
import glob
try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    no_openai = False
except ModuleNotFoundError:
    print('OpenAI library not installed')
    no_openai = True
    pass

# set up paths
master_path = os.getcwd()
result_folder = os.path.join(master_path, 'results')
subtopics = [1, 2, 3]


# function to compile all csv files for a subtopic into a single dataframe
def load_df_from_folder(ind):
    folder = os.path.join(result_folder, 'subtopic' + str(ind))
    files = glob.glob(os.path.join(folder, '*'))
    dfs = [pd.read_csv(f, header=0, index_col=None) for f in files]
    compiled_df = pd.concat(dfs, ignore_index=True)
    return compiled_df


# create a compiled df for each subtopic
try:
    all_dfs
    pass
except NameError:
    all_dfs = []
    for i in subtopics:
        all_dfs.append(load_df_from_folder(i))

# for each subtopic, identify number of unique results
all_dfs_dedup = []
n_uniques = []
for i in range(len(all_dfs)):
    df = all_dfs[i]
    num_records = len(df)
    df_dedup = df.drop_duplicates()
    num_unique = len(df_dedup)
    print('Subtopic', i+1, 'unique results: ', num_unique)
    all_dfs_dedup.append(df_dedup)
    n_uniques.append(num_unique)

# across all subtopics, identify number of unique results
master_df = pd.concat(all_dfs, ignore_index=True)
master_df_dedup = master_df.drop_duplicates()
num_unique_total = len(master_df_dedup)

# put together keyword prompt
keyword_prompt = 'Extract keywords from this text:\n\n'
all_titles = master_df_dedup['Paper title']
# separate list of titles into chunks that can be handled by OpenAI caller
chunks = [all_titles[i:i + 10] for i in range(0, len(all_titles), 10)]

'''
OpenAI API calls
'''
if no_openai is False:
    # perform keyword extraction on titles using OpenAI API
    keywords = []
    for i in range(len(chunks)):
        if (i+1) % 10 == 0:
            print('Processing chunk', i+1, '/', len(chunks))
        kprompt = keyword_prompt + '. '.join(chunks[i].values)
        kprompt = kprompt.replace('..', '.')
        response = openai.Completion.create(
            model='text-davinci-002',
            prompt=kprompt,
            temperature=0.2,
            top_p=1.0,
            frequency_penalty=0.8,
            presence_penalty=0.0)
        keywords.append(response['choices'][0]['text'].split('\n\n')[1])
else:
    pass
