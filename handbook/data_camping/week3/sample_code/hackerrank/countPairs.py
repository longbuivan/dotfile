#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'countPairs' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY numbers
#  2. INTEGER k
#

def countPairs(numbers, k):
    '''
    Description: Counting the number of distinct valid pairs of integers (a,b) in the list for which a + k = b
    Param:
        - number (str): list of integer
        - k (integer) : target offset
    Return:
        - result (integer): Number of valid pairs (a,b) in the numbers array that have a offset k
    Time Complexity: O(n)
    '''
    
    # Check input values for constraints
    if not (2 <= len(numbers) <= 2 * 10**5):
        raise ValueError("Number of elements in 'numbers' list must be between 2 and 2*10^5")
    
    for num in numbers:
        if not (0 <= num <= 10**9):
            raise ValueError("Each element in 'numbers' list must be between 0 and 10^9")
    
    if not (0 <= k <= 10**9):
        raise ValueError("Value of 'k' must be between 0 and 10^9")
    
    
    num_set = set(numbers)  # Create a set if distinct numbers, without repeative lookup
    pair_count = 0
    
    for num in num_set:
        if num + k in num_set:
            pair_count += 1
    result = pair_count

    return result
    
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    numbers_count = int(input().strip())

    numbers = []

    for _ in range(numbers_count):
        numbers_item = int(input().strip())
        numbers.append(numbers_item)

    k = int(input().strip())

    result = countPairs(numbers, k)

    fptr.write(str(result) + '\n')

    fptr.close()
