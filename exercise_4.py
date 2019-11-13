# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 12:36:48 2019

@author: Nathan
"""

def longest_palindromic_subsequence(s): 
    
    n = len(s) 
  
    # We create a table to store the results of subproblems 
    L = [[0 for x in range(n)] for x in range(n)] 
  
    # Strings of length 1 are palindrome of length 1 
    for i in range(n): 
        L[i][i] = 1

    # cl is the length of substring 
    for cl in range(2, n+1): 
        for i in range(n-cl+1): 
            j = i+cl-1
            if s[i] == s[j] and cl == 2: 
                L[i][j] = 2
            elif s[i] == s[j]: 
                L[i][j] = L[i+1][j-1] + 2
            else: 
                L[i][j] = max(L[i][j-1], L[i+1][j])

    return L[0][n-1] 


txt = "DATAMININGSAPIENZA"

longest_palindromic_subsequence(txt)
