#
#	python modular sorting animation
#	file: mod_gen.py
#       description: mod_gen contains array manipulation functions
#               to create datasets for the sort animation
#	license: py-mod-sort/LICENSE (Apache 2.0)
#	by: Patrick Stanislaw Hadlaw
#

import tkinter as tk
import random
import time
import math
import copy

#
# Array Generators
#

def randomArray(size, flip = False):
    arr = list(range(size))
    for i in range(0, size*10):
        r1 = random.randint(0, size-1)
        r2 = random.randint(0, size-1)
        tmp = arr[r2]
        arr[r2] = arr[r1]
        arr[r1] = tmp
    if flip:
        return list(reversed(arr))
    else:
        return arr

def randomElement(size, flip = False):
    arr = []
    for i in range(0, size):
        arr.append(random.randint(0, size-1))
    if flip:
        return list(reversed(arr))
    else:
        return arr

def block(size, blocks, flip = False):
    blockLen = int(size / blocks)
    arr = []
    for i in range(1, blocks+1):
        for j in range(0, blockLen):
            arr.append(i*blockLen)
        if i + 1 > blocks and len(arr)<size:
            for j in range(0, size - len(arr)):
                arr.append(i*blockLen)
    if flip:
        return list(reversed(arr))
    else:
        return arr
            
        

def functional(size, step, func, flip = False):
    arr = [func(step*i) for i in range(0, size)]
    if flip:
        return list(reversed(arr))
    else:
        return arr


def randomize(arr): #
    for i in range(0, len(arr)*10):
        r1 = random.randint(0, len(arr)-1)
        r2 = random.randint(0, len(arr)-1)
        tmp = arr[r2]
        arr[r2] = arr[r1]
        arr[r1] = tmp
    return arr
