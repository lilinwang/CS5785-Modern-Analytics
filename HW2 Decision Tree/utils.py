# decision tree stuff
import math
def entropy(a,b):
    '''numEntries = len(dataset)  
    labelCounts = {}  
    for currentLabel in dataset:    
        if currentLabel not in labelCounts.keys():  
            labelCounts[currentLabel] = 0  
        labelCounts[currentLabel] += 1  
    shannonEnt = 0.0  
  
    for key in labelCounts:  
        prob = float(labelCounts[key])/numEntries  
        if prob != 0:  
            shannonEnt -= prob*math.log(prob,2)  '''
            
    shannonEn=0.0
    if a==0 or a==b:
        return shannonEn
    prob=float(a)/b
    shannonEn-=prob*math.log(prob,2)
    prob=float(b-a)/b    
    shannonEn-=prob*math.log(prob,2)
    return shannonEn

def information_gain(a,b,c,d):
    total=b+d    
    return float(b/total)*entropy(a,b)+float(d/total)*entropy(c,d)

# natural language processing stuff
def freq(lst):
    freq = {}
    length = len(lst)
    for ele in lst:
        if ele not in freq:
            freq[ele] = 0
        freq[ele] += 1
    return (freq, length)

def get_unigram(review):
    return freq(review.split())

def get_unigram_list(review):
    return get_unigram(review)[0].keys()