#!/bin/python3

import math
import os
import random
import re
import sys
import pandas as pd

#
# Complete the 'schoolCount' function below.
#
# The function is expected to return a pandas dataframe.
#

def schoolCount(df):
    
    df['subject_count'] = df['subjects'].apply(lambda x: len(x.split()))
    df = df[df['subject_count']> 3].copy()
    
    # Clean state code
    df['state_code'] = df['state_code'].apply(lambda x: re.sub(r'[^a-zA-Z0-9]', '', x))
    
    # Split subjects and adding columsn Languages
    subject_list = df['subjects'].str.split(expand=True)
    df = pd.concat([df, subject_list], axis=1)
    df.rename(columns={0: 'english', 1: 'maths', 2: 'physics', 3: 'chemistry'}, inplace=True)
    
    # Count subjects and group by state code
    result_df = df.groupby('state_cide').agg({'english': 'sum', 'maths': 'sum', 'physics': 'sum', 'chemistry': 'sum'}).reset_index()
    
    return result_df

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    df = pd.read_csv('/dev/stdin')
    
    result = schoolCount(df)
    fptr.write(result.to_csv(index=False))

    fptr.close()
