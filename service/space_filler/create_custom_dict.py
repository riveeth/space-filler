"""
Custom dictionary with word probabilities was created using English Word Frequency dataset from
https://www.kaggle.com/datasets/rtatman/english-word-frequency

Download dataset from Kaggle and place it into "data" folder.
Any dataset can be used here. Make sure that data contains "count" and "word" columns, where count specifies the
frequency of a given word in the word corpus.

We assume that each word has the probability n/N where  N is the number of words in the text corpus and n is the
occurrence of a certain word. There are other approaches as well, e.g.
https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words/11642687#11642687

After getting word probabilities some custom modifications were made.
"""

import os
import json
import pandas as pd


# Read word frequencies dataframe and convert into probabilities dictionary
base_dir = os.path.abspath(os.path.join(__file__, "../../../data"))
dataset_path = os.path.join(base_dir, 'unigram_freq.csv')
data = pd.read_csv(dataset_path)

data['prob'] = data['count'] / data['count'].sum()
word_freq = dict(zip(data['word'], data['prob']))

# Remove dataframe and some confusing words
del data
del word_freq['ima']
del word_freq['sa']
del word_freq['helloworld']  # apparently this one is also considered as a valid word with frequency 145066,


# Adjust contraction probabilities
word_freq['hes'] = word_freq.get('he') * word_freq.get('is')
word_freq['shes'] = word_freq.get('she') * word_freq.get('is')
word_freq['youre'] = word_freq.get('you') * word_freq.get('are')
word_freq['theyre'] = word_freq.get('they') * word_freq.get('are')
word_freq['thats'] = word_freq.get('that') * word_freq.get('is')
word_freq['wheres'] = word_freq.get('where') * word_freq.get('is')
word_freq['icant'] = word_freq.get('i') * word_freq.get('cant') - 10e-10

# Add min value key to use it as a default dict.get(.., ..) value
word_freq['_min_value'] = word_freq.get(min(word_freq, key=word_freq.get)) * 0.99

# Save json file
dict_path = os.path.join(base_dir, 'word_probs.json')
with open(dict_path, 'w') as fp:
    json.dump(word_freq, fp)
    print(f"Dictionary saved at {dict_path}")
