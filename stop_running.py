"""
@author:
    Andy McMahon

Will look at the data being produced by Roland's inception and
then ascertain whether he's explored enough of the space to stop
running around.

"""

import pandas as pd


df = pd.read_json('dump.json', orient='records')

df['top_human_string'] = df['human_strings'].apply(lambda x: x[0])

test = df['top_human_string']

def intersect(a, b):
    return list(set(a) & set(b))

"""
Measures of similarity :

    are the items I've seen before similar?
    is the percentage of which I've seen them similar?
"""
stats = []
lens = []
size = 1

for i in range(0, len(test), size):
    
    lens.append(len(test[0:i].unique()))
    
pd.Series(lens).diff().plot()

for i in range(0, len(test), 2):
    
    stats.append( 1*test[i:i+50].value_counts()/50.0 )
    