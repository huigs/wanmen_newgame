# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:09:27 2020

@author: wei.sun2
"""


import itertools as its
words = "0123456789abcdefghijklmnopqrstuvwxyz"
#r =its.product(words,repeat=4)
dic = open("d:\pass.txt","a")
#for num in range(8,11):
keys=its.product(words,repeat=8)
for key in keys:
    dic.write("".join(key)+"\n")
dic.close()
