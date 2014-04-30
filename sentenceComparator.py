# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 14:38:27 2014

@author: brkyvz




"""
"""stop words
"""

stopwords = {}

import nltk.tokenize as nlt
import nltk.stem as nls

"""Output all n-grams in a sentence.  """

def ngram(n, a):

    grams = {}
    
    lem = nls.WordNetLemmatizer()

    split_line = nlt.word_tokenize(a)
    global stopwords
    title = [s for s in split_line if not stopwords.has_key(s.lower())]
    for i in range(len(title)-n+1):
        ngr = ''
        for j in range(i,n+i):
            if len(title[j])>0:
                ngr += ' ' + lem.lemmatize(title[j].lower())
            
        if ngr.strip().__len__()>0:
            grams[ngr.strip()] = 1
            
            
    return grams
  
def secPass(n,a,frequent):
    
    g = ngram(n,a)
    out = {}
    for i, w1 in enumerate(g.iterkeys()):
        if w1 not in frequent:
            continue
        for j, w2 in enumerate(g.iterkeys()):
            if w2 not in frequent:
                continue
            if i==j:
                continue
            out[(w1,w2)] = 1
            out[(w2,w1)] = 1
            
            
    return out      

""" Return a list of tuples containing common words and urls"""
def listNgram(n,k,l):
    firstPass = {}
    for i, (sent1,url1) in enumerate(l):
        grams = ngram(n,sent1)
        for k in grams.iterkeys():
            if firstPass.has_key(k):
                firstPass[k] += grams[k]
            else:
                firstPass[k] = grams[k]
        
    print firstPass
    """commonSingles = [key for (key,val) in firstPass.items() if val > k]"""
    commonSingles = [None]*len(firstPass.items())
    cnt = 0
    for (key,val) in firstPass.items():
        print key + " " + str(val)
        if val>k:
            commonSingles[cnt] = key
            cnt += 1
            
    print commonSingles
    secondPass = {}
    
    for i, (sent1,url1) in enumerate(l):
        pairs = secPass(n,sent1, commonSingles)
        for k in pairs.iterkeys():
            if secondPass.has_key(k):
                secondPass[k] += pairs[k]
            else:
                secondPass[k] = pairs[k]
            
            """
    common = aggregate(couples,3)
    """
    
    tuplesList = [None]*(len(secondPass.keys())/2)
    
    for i,(w1,w2) in enumerate(secondPass.keys()):
        tuplesList[i] = ((w1,w2), [url for j,(sent,url) in enumerate(l) if j in secondPass[(w1,w2)]])
        
    return tuplesList
    
    
"""Merge common words
def aggregate(dic, support):
    mainlist = {}    
    for key in dic.keys():
        val = dic[key]
        for word in val.keys():
            if mainlist.has_key(word):
                l = mainlist[word]
                if not l.__contains__(key[0]):
                    l.append(key[0])
                if not l.__contains__(key[1]):
                    l.append(key[1])
                    mainlist[word] = l
            else:
                mainlist[word] = [key[0], key[1]]
                
    dictionary that will return words with frequencies over some support
    retdic = {}
    for key,val in mainlist.iteritems():
        if (val.__len__()>= support):
            retdic[key] = val
            
    return retdic
"""


def loadStopWords():
    dic = {}
    with open('stop.txt','r') as f:
        for line in f:
            words = line.split()
            for w in words:
                if (w[0] == '|'):
                    break
                else:
                    dic[w.lower()] = 1
                    
    global stopwords
    stopwords = dic             
    
    
def init(n, k, articles):
    loadStopWords()
    print listNgram(n, k, articles)
  
  