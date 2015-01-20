# -*- coding: utf-8 -*-
'''
This simple file is using decision trees to predict ratings from Amazon food reviews.
Input file: http://snap.stanford.edu/data/web-FineFoods.html

__author__ = 'Lilin Wang'
__date__ = '2014/10/26'

'''
import decision_tree as dt
import scan
import utils
import operator
def column(matrix, i):
    return [row[i] for row in matrix]
def B(data,flag):     
    lst=[]
    for ele in data :        
        if flag>0 and ele[1]>0 or flag<0 and ele[1]<1 or flag==0:    
            tem=ele[0].split()
            lst.extend(tem)
    dic=utils.freq(lst)[0]
    sorted_x = sorted(dic.items(), key=operator.itemgetter(1),reverse=True)
    for i in range (0,30):
        print sorted_x[i]       
    
def main():
    binary_label = True
    exclude_stopwords = False
    Path='E:\Cornell\Modern Analytics\HW2\\'
    
    print "#### Solution for (b) ####################"
    data = scan.scan(Path+'foods.txt', exclude_stopwords, binary_label)    
    print "30 most popular unigrams among all reviews: "         
    B(data,0)
    print "30 most popular unigrams among positive reviews: "
    B(data,1)
    print "30 most popular unigrams among negative reviews: "
    B(data,-1)
    
    print "#### Solution for (c) ####################"
    exclude_stopwords = True
    data = scan.scan(Path+'foods.txt', exclude_stopwords, binary_label)
    print "30 most non-stopword popular unigrams among all reviews: "         
    B(data,0)
    print "30 most non-stopword popular unigrams among positive reviews: "
    B(data,1)
    print "30 most non-stopword popular unigrams among negative reviews: "
    B(data,-1)    
    
    print "#### Solution for (d & e & f) ####################"
    exclude_stopwords = True
    data = scan.scan(Path+'foods.txt', exclude_stopwords, binary_label)
    length=len(data)
           
    train_data = data[:int(length*.8)]
    test_data = data[int(length*.8):]    
    
    decision_tree = dt.train(train_data)
    test_results = dt.test(decision_tree, test_data)
    

    print test_results
    

if __name__ == '__main__':
    main()
