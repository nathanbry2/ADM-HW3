# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 18:59:38 2019

@author: Nathan
"""

import itertools as iter

def palindrome(word):
    for i in range(len(word)//2):
         if word[i] != word[-1-i]:
                 return False
    return True

def poli(s):
    for i in range(0, len(s)):
        s1=[]
        temp = [list(x) for x in iter.combinations(s,len(s)-i)]
        s1.extend(temp)
    
        for j in range(0,len(s1)):
    
            if palindrome(s1[j])==True:
                c=len(s1[j])
                return c
            
            
print(poli("DATAMININGSAPIENZA"))