import itertools as iter

#define a function to find if a string is a palindrome or not
def palindrome(word):
    for i in range(len(word)//2):
         if word[i] != word[-1-i]:
                 return False
    return True
   
   
#we create combinations for each word with less than 1 letter each time 
#we don't find in all combinations with at least 1 palindrome word
#and we take the numbers of letter of this word
def poli(s):
    for i in range(0, len(s)):
        s1=[]
        temp = [list(x) for x in iter.combinations(s,len(s)-i)]
        s1.extend(temp)
    
        for j in range(0,len(s1)):
    
            if palindrome(s1[j])==True:
                c=len(s1[j])
                return(c)
#we test it           
print(poli("dataminingsapienza"))
