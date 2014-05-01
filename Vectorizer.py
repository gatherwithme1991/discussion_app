# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 21:09:22 2014

@author: brkyvz
"""
import nltk.tokenize as nlt
import nltk.stem as nls
import numpy as np
import scipy
import re

from article import Article

stopwords = {}

# Use this for kmeans
class Vectorizer:
    def __init__(self):
        pass

    def vectorize(self, art_list):
        self.loadStopWords()
        print 'in'
        lem = nls.WordNetLemmatizer()
        allcombos = {}
        filecombos = {}
        cnt = 0
        artcnt=0;
        pattern = r'[a-zA-Z]'
        column = []
        row = []
        global stopwords
        senw={}
        for art in art_list:
            description = art.description
            print description
            for word in nlt.wordpunct_tokenize(description):
                if not re.search(pattern,word[0]):
                    continue
                if stopwords.has_key(word.lower()):
                    continue
                
                withoutSW = lem.lemmatize(word.lower())
                
                if not allcombos.has_key(withoutSW):
                    allcombos[withoutSW] = cnt
                    column.append(cnt)              
                    if not filecombos.has_key(art.id_num):  
                        filecombos[art.id_num] = artcnt
                            
                    row.append(filecombos[art.id_num])
                    senw[cnt] = 1
                    cnt += 1
                else:
                    if senw.has_key(allcombos[withoutSW]):
                        continue
                    column.append(allcombos[withoutSW])
                    senw[allcombos[withoutSW]] = 1
                    if not filecombos.has_key(art.id_num):  
                        filecombos[art.id_num] = artcnt
                            
                    row.append(filecombos[art.id_num])
            
            artcnt += 1
            senw={}
        
        value = [1]*len(column)
        
        nval = np.array(value)
        nc = np.array(column)
        nr = np.array(row)
        
        return scipy.sparse.coo_matrix((nval,(nr,nc)), shape=(artcnt,cnt)).todense().getA()
        
        
    def cosSim(self, a, b):
        mul = a.dot(b)
        denom = a.sum()*b.sum()
        return mul*1.0/denom

      
    def loadStopWords(self):
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


    def calculateSimilarities(self, articles):
        loadStopWords()
        matD = Vectorize(articles)

        for i in range(len(articles)):
            for j in range(i+1,len(articles)):
                sim = cosSim(matD[i,:],matD[j,:])
                if sim>0.012:
                    print str(i) + ',' + str(j) + '->' + str(sim)
                    print articles[i].description
                    print articles[j].description



        
    