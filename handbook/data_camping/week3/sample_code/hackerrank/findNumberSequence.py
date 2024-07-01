#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'findNumberSequence' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts STRING direction as parameter.
#

def findNumberSequence(direction):
    '''
    Description: Finding the sequence of numbers placed n the segment in the order of their placement points.
    Param:
        - direction (str): A string of length n where ('L' and 'R') idicate th direction of the turn. Ex: LRLLR
    Return:
        - result (list): An integer list of sequence of numbers placed on the segment after ordered by direction
    Time Complexity: O(n log n) due to sorting the positions
    '''
    n = len(direction)
    segment_start = 0
    segment_end = 2 ** n
    positions = []
    values = []
    
    if n < 1 or n > 10**5:
        raise ValueError("Input size exceeds the allowed limit")
    
    for i in range(n):
    
        center = (segment_start + segment_end) // 2 # Note: Change due to MemoryError
        # center = segment_start + (segment_end - segment_start) // 2
        positions.append(center)
        values.append(i + 1)
        
        if direction[i] == 'L':
            segment_end = center
        else:
            segment_start = center
            
    combined = list(zip(positions, values))
    combined.sort()
    
    result = [value for _, value in combined]

    return result

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    direction = input()

    result = findNumberSequence(direction)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
