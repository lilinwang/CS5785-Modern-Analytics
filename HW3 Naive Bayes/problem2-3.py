# -*- coding: utf-8 -*-
'''
This simple file is using naive bayes to guess a movie’s year and find ironic words for each decade.
Input file: download file 'plot.list.gz' from http://www.imdb.com/interfaces  

__author__ = 'Lilin Wang'
__date__ = '2014/12/03'

'''
import parse_movie_example as pm
import numpy as np
import matplotlib.pyplot as plt
import random
import string
import math
from copy import deepcopy
import time
from math import e

path='E:\Cornell\Modern Analytics\HW3\\' 

def plot_2a_2g(x,item,problem_name):
    plt.figure()
    bins = np.linspace(1930, 2010, 9)    
    plt.title('Probability Mass Function of '+item)
    plt.xlabel(item)
    plt.ylabel('P('+item+')')
    plt.hist(x, bins, weights=np.ones_like(x)/float(len(x)))
    plt.savefig(path+problem_name+'.png') 
    
def plot_2j(x,y,problem_name):
    plt.figure()
    total=float(0.0)
    for i in range(8):
        y[i]=e**(y[i]/float(1000))
    for i in range(8):
        total+=y[i]
    for i in range(8):
        y[i]=float(y[i])/total
    plt.title('P(Y=y|Movie='+problem_name+') over y')
    plt.xlabel('Y(year)')
    plt.ylabel('P(Y=y|Movie='+problem_name+')')
    plt.bar(x, y)
    plt.savefig(path+'2j_'+problem_name+'.png') 

def plot_2l(x,y,problem_name):
    plt.figure()
    plt.title('Cumulative Match Curve')
    plt.xlabel('k')
    plt.ylabel('accuracy')
    
    # calculate polynomial
    z = np.polyfit(x, y, 3)
    f = np.poly1d(z)

    # calculate new x's and y's
    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)

    plt.plot(x,y,'o', x_new, y_new)
    plt.xlim([x[0]-1, x[-1] + 1 ])
    plt.savefig(path+problem_name+'.png')
 
def plot_2m(matrix,problem_name):   
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean)
    plt.colorbar()
    plt.savefig(path+problem_name+'.png')
    
def main():
    time1=time.time()
    all_movies = list(pm.load_all_movies(path+"plot.list.gz")) 
        
    #===================================
    #Solution of problem 2a-ad 
    #
    print '#============================================='
    print '### Solution of problem 2a & 2b & 2c & 2d ###'
    print 'Please check 2a.png, 2b.png, 2c.png and 2d.png'   
    x = [row['year'] for row in all_movies if row['year']<2010]         
    plot_2a_2g(x,'Y','2a')    
    x = [row['year'] for row in all_movies if row['year']<2010 and 'radio' in row['summary']]     
    plot_2a_2g(x,'Y|X_radio>0','2b')
    x = [row['year'] for row in all_movies if row['year']<2010 and 'beaver' in row['summary']]     
    plot_2a_2g(x,'Y|X_beaver>0','2c')
    x = [row['year'] for row in all_movies if row['year']<2010 and 'the' in row['summary']]     
    plot_2a_2g(x,'Y|X_the>0','2d')   
    
    
    #===================================
    #Solution of problem 2e-2g
    #
    print '#========================================='
    print '### Solution of problem 2e & 2f & 2g ###'
    print 'Please check 2e.png, 2f.png, and 2g.png'   
    #sample 6000 rows for each decade
    sample_size=6000
    x = [row for row in all_movies if row['year']==1930]      
    sample_movies = random.sample(x,sample_size)        
    x = [row for row in all_movies if row['year']==1940]  
    sample_movies.extend(random.sample(x,sample_size))
    x = [row for row in all_movies if row['year']==1950]  
    sample_movies.extend(random.sample(x,sample_size))
    x = [row for row in all_movies if row['year']==1960]  
    sample_movies.extend(random.sample(x,sample_size))
    x = [row for row in all_movies if row['year']==1970]  
    sample_movies.extend(random.sample(x,sample_size))
    x = [row for row in all_movies if row['year']==1980]  
    sample_movies.extend(random.sample(x,sample_size))
    x = [row for row in all_movies if row['year']==1990]  
    sample_movies.extend(random.sample(x,sample_size))
    x = [row for row in all_movies if row['year']==2000]  
    sample_movies.extend(random.sample(x,sample_size))   
     
    x = [row['year'] for row in sample_movies if 'radio' in row['summary']]     
    plot_2a_2g(x,'Y|X_radio>0','2e')
    x = [row['year'] for row in sample_movies if 'beaver' in row['summary']]     
    plot_2a_2g(x,'Y|X_beaver>0','2f')
    x = [row['year'] for row in sample_movies if 'the' in row['summary']]     
    plot_2a_2g(x,'Y|X_the>0','2g') 
    
    size=sample_size*8
    #split this dataset into training and test sets
    train_data = [sample_movies[i] for i in range(size) if i%2==0]
    test_data = [sample_movies[i] for i in range(size) if i%2==1]
    print 'train dataset size is: ',len(train_data)
    print 'test dataset size is:',len(test_data)
    
    
    #===================================
    #Solution of problem 2i
    #
    #train the data
    words={}  #all words  
    words_by_year={1930:{},1940:{},1950:{},1960:{},1970:{},1980:{},1990:{},2000:{}}
    movies_count_by_year={1930:0,1940:0,1950:0,1960:0,1970:0,1980:0,1990:0,2000:0}    
    years=[1930,1940,1950,1960,1970,1980,1990,2000]
    delset = string.punctuation

    for row in train_data:    
        words_tmp=row['summary'].replace('\n\n',' ').replace('\n',' ').translate(None,delset).lower().split(' ')        
        words_count={}
        for word in words_tmp:
            if words_count.has_key(word)==False:
                words_count[word]=1
            else:
                words_count[word]+=1
        
        for word in words_count:              
            if words.has_key(word)==False:
                words[word]=0
            if words_by_year[row['year']].has_key(word)==True:
                if words_by_year[row['year']][word].has_key(words_count[word])==True:
                    words_by_year[row['year']][word][words_count[word]]+=1
                else:
                    words_by_year[row['year']][word][words_count[word]]=1
            else:
                words_by_year[row['year']][word]={}
                words_by_year[row['year']][word][words_count[word]]=1     
        movies_count_by_year[row['year']]+=1
    print 'Total size of words is: ',len(words)
    
    #calculate conditional probability
    for year in years:
        for word in words_by_year[year]:
            positive=0.0
            for count in words_by_year[year][word]:                  
                words_by_year[year][word][count]=float(words_by_year[year][word][count])/movies_count_by_year[year]                
                positive+=words_by_year[year][word][count]
            words_by_year[year][word][0]=1.0-positive
            
    
    #===================================            
    #Solution of problem 2k & 2l & 2m
    #
    #test the data   
    print '#==================================='
    print '### Solution of problem 2k ###'    
    
    #count of movies which is predicted right for each decade                                            
    right_count_k={1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    
    #confusion matrix
    matrix=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    
    #map decade to 0-7
    year_to_index={1930:0,1940:1,1950:2,1960:3,1970:4,1980:5,1990:6,2000:7} 
    
    Dirichlet_min=0.00001
    
    for row in test_data:
        words_tmp=row['summary'].replace('\n\n',' ').replace('\n',' ').translate(None,delset).lower().split(' ')        
        words_count={}
        for word in words_tmp:
            if words_count.has_key(word)==True:
                words_count[word]+=1
            else:
                words_count[word]=1
                
        #posterior probability for each decade
        prob_years={}        
        for year in years:
            prob=0.0
            for word in words: 
                if words_count.has_key(word)==True:
                    if words_by_year[year].has_key(word)==True and words_by_year[year][word].has_key(words_count[word])==True:
                        prob+=math.log(max(words_by_year[year][word][words_count[word]],Dirichlet_min))                        
                    else:
                        prob+=math.log(Dirichlet_min)
                else:
                    if words_by_year[year].has_key(word)==True:              
                        prob+=math.log(max(words_by_year[year][word][0],Dirichlet_min))
                    else:
                        prob+=math.log(1.0)
            prob+=math.log(float(movies_count_by_year[year])/(sample_size*4))
            prob_years[year]=prob
        
        #posterior probability for each decade sorted by probability
        sorted_prob=sorted(prob_years.iteritems(), key=lambda d:d[1], reverse = True)
        if row['year']!=sorted_prob[0][0]:
            matrix[year_to_index[row['year']]][year_to_index[sorted_prob[0][0]]]+=1
        for k in range(1,8):            
            if sorted_prob[k-1][0]==row['year']:
                for kk in range(k,8):
                    right_count_k[kk]+=1
                break
                
    #accuracy for each decade
    accuracy=[]
    for k in range(1,8):
        accuracy.append(float(right_count_k[k])/len(test_data))
    print 'Accuracies are: ',accuracy
    accuracy.append(1.0)
    print '#==================================='
    print '### Solution of problem 2j & 2m ###'
    print 'Please check 2l.png and 2m.png'
    x=[1,2,3,4,5,6,7,8]
    plot_2l(x,accuracy,'2l')
    plot_2m(matrix,'2m')
    
    
    #===================================
    #Solution of problem 2j
    #
    print '#==================================='
    print '### Solution of problem 2j ###'
    movies_2j=["Finding Nemo","The Matrix","Gone with the Wind","Harry Potter and the Goblet of Fire","Avatar"]    
    for row in all_movies:
        if row['title'] in movies_2j:
            #print row['title']
            words_tmp=row['summary'].replace('\n\n',' ').replace('\n',' ').translate(None,delset).lower().split(' ')        
            words_count={}
            for word in words_tmp:
                if words_count.has_key(word)==False:
                    words_count[word]=1
                else:
                    words_count[word]+=1
            predict_year=1930
            predict_prob=-2**100
                            
            prob_years=[]      
            for year in years:
                prob=0.0
                for word in words: 
                    if words_count.has_key(word)==True:                        
                        if words_by_year[year].has_key(word)==True and words_by_year[year][word].has_key(words_count[word])==True:
                            prob+=math.log(max(words_by_year[year][word][words_count[word]],Dirichlet_min))                        
                        else:
                            prob+=math.log(Dirichlet_min)
                    else:
                        if words_by_year[year].has_key(word)==True:              
                            prob+=math.log(max(words_by_year[year][word][0],Dirichlet_min))
                        else:
                            prob+=math.log(1.0)
                prob+=math.log(float(movies_count_by_year[year])/(sample_size*4))                                            
                prob_years.append(prob)
                if prob>predict_prob:
                    predict_prob=prob
                    predict_year=year
            #print prob_years
            plot_2j(years,prob_years,row['title'])
            if predict_year==row['year']:
                print row['title']+': predict right'
                  
    
    #===================================
    #Solution for problem 3a
    #
    print '#==================================='
    print '### Solution for problem 3a ###'
    f={1930:{},1940:{},1950:{},1960:{},1970:{},1980:{},1990:{},2000:{}}
    for word in words:
        min_prob=1.0
        for year in years:
            if (words_by_year[year].has_key(word)==False):
                min_prob=min(min_prob,Dirichlet_min)
            else:
                min_prob=min(min_prob,1.0-words_by_year[year][word][0])
        for year in years:
            if (words_by_year[year].has_key(word)==False):
                f[year][word]=Dirichlet_min/min_prob
            else:
                f[year][word]=(1.0-words_by_year[year][word][0])/min_prob
    for year in years:
        row=f[year]
        f[year]=sorted(row.iteritems(), key=lambda d:d[1], reverse = True)
        print 'The 10 most informative words for decade ',year,' are:'
        for i in range(10):
            print f[year][i][0]
            
    #===================================        
    #Solution for problem 3b
    #
    print '#==================================='
    print '### Solution for problem 3b ###'
    words_by_year_copy=deepcopy(words_by_year)
    for year in years:        
        for word in words_by_year_copy[year]:            
            if word in f[year][:100][0]:
                del words_by_year[year][word]            
    del words_by_year_copy
    
    right_count_k={1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    matrix=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]    
    for row in test_data:
        words_tmp=row['summary'].replace('\n\n',' ').replace('\n',' ').translate(None,delset).lower().split(' ')        
        words_count={}
        for word in words_tmp:
            if words_count.has_key(word)==True:
                words_count[word]+=1
            else:
                words_count[word]=1                
        prob_years={}        
        for year in years:
            prob=0.0
            for word in words: 
                if words_count.has_key(word)==True:
                    if words_by_year[year].has_key(word)==True and words_by_year[year][word].has_key(words_count[word])==True:
                        prob+=math.log(max(words_by_year[year][word][words_count[word]],Dirichlet_min))                        
                    else:
                        prob+=math.log(Dirichlet_min)
                else:
                    if words_by_year[year].has_key(word)==True:              
                        prob+=math.log(max(words_by_year[year][word][0],Dirichlet_min))
                    else:
                        prob+=math.log(1.0)
            prob_years[year]=prob
        sorted_prob=sorted(prob_years.iteritems(), key=lambda d:d[1], reverse = True)
        if row['year']!=sorted_prob[0][0]:
            matrix[year_to_index[row['year']]][year_to_index[sorted_prob[0][0]]]+=1
        for k in range(1,8):            
            if sorted_prob[k-1][0]==row['year']:
                for kk in range(k,8):
                    right_count_k[kk]+=1
                break
    accuracy=[]
    for k in range(1,8):
        accuracy.append(float(right_count_k[k])/len(test_data))    
    print 'Accuracies are: ',accuracy 
    accuracy.append(1.0)
    x=[1,2,3,4,5,6,7,8]
    plot_2l(x,accuracy,'3b_2l')
    plot_2m(matrix,'3b_2m')
        
    print 'Total time cost:',time.time()-time1
    
if __name__ == '__main__':
    main()