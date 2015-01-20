# -*- coding: utf-8 -*-
'''
This simple file is using logistic regression to predict whether a passenger survived the titanic disaster.
Input file: http://www.kaggle.com/c/titanic-gettingStarted

__author__ = 'Lilin Wang'
__date__ = '2014/09/27'

'''
import scan
import utils
import operator

class DecisionTree:
    node_label = None  # takes the values 0, 1, None. If has the values 0 or 1, then this is a leaf
    left = None #using its presence
    right = None #using its absence
    feature = None

def decision(tree, data):
    lst=data.split()
    try:
        lst.index(tree.feature)
        return tree.left
    except:
        return tree.right

def go(tree, data):
    #print tree.node_label,tree.feature
    if tree.node_label != None:
        return tree.node_label
    return go(decision(tree,data),data)

# http://en.wikipedia.org/wiki/ID3_algorithm
def choose_bestfea(feature, data):
    min_entro=1
    length=len(data)
    index=-1    
    for i in range(len(feature)):
        ele=feature[i]
        hit=0
        pre_pos=0
        abs_pos=0
        for line in data:            
            lst=line[0].split()
            try:
                lst.index(ele)
                hit+=1
                pre_pos+=line[1]
            except:
                abs_pos+=line[1]
                pass                    
        gain=utils.information_gain(pre_pos,hit,abs_pos,length-hit)
        #print now, min_entro
        if min_entro>gain:
            min_entro=gain
            index=i
    return index

def split_data(bestfea,data):
    idx_less = [] #create new list including data with feature less than pivot  
    idx_greater = [] #includes entries with feature greater than pivot      
    for line in data:    
        lst=line[0].split()
        try:
            lst.index(bestfea)
            idx_less.append(line)            
        except:
            idx_greater.append(line)
    return idx_less,idx_greater  
    
def build_tree(feature, data):   
    tree=DecisionTree()    
    label=0
    for line in data:
        label+=line[1]
    if label==len(data) or label==0:        
        tree.node_label=data[0][1]
        return tree
    
    label=0
    common=0
    for line in data:
        label+=line[1]
    tem=float(label)/len(data)
    if tem>0.5:
        common=1
        
    if len(feature)==0:        
        tree.node_label=common
        return tree
    
    bestfea=choose_bestfea(feature,data)    
    data_pre,data_abs=split_data(feature[bestfea],data) 
    
    tree.feature=feature[bestfea]
    del(feature[bestfea])
    
    #print len(data_pre),len(data_abs),len(feature)
    if len(data_pre)==0:
        ltree=DecisionTree()
        ltree.node_label=common
        tree.left=ltree
    else:        
        tree.left=build_tree(feature,data_pre)
        
    if len(data_abs)==0:
        rtree=DecisionTree()
        rtree.node_label=common
        tree.right=rtree
    else:        
        tree.right=build_tree(feature,data_abs) 
    return tree
    
def train(data):   
    positive_list=[]
    negative_list=[]
    for ele in data :
        tem=ele[0].split()        
        if ele[1]>0:            
            positive_list.extend(tem)
        else:            
            negative_list.extend(tem)    
    dic = utils.freq(positive_list)[0]
    positive_words = sorted(dic.items(), key=operator.itemgetter(1),reverse=True)
    dic = utils.freq(negative_list)[0]
    negative_words = sorted(dic.items(), key=operator.itemgetter(1),reverse=True)
    #tree=DecisionTree()
    tdata=[]
    for i in range(500):
        try:
            tdata.index(positive_words[i][0])
        except:
            tdata.append(positive_words[i][0])
    for i in range(500):
        try:
            tdata.index(negative_words[i][0])
        except:
            tdata.append(negative_words[i][0])        
    tree=build_tree(tdata,data)    
    return tree    

def test(tree, data):
    hit=0
    for line in data:
        if go(tree,line[0])==line[1]:
            hit+=1
    accuracy=float(hit)/len(data)
    return accuracy
'''dt=train([['aaa',1],['bbb',1]])
print test(dt,[['aaa',1],['bbb',1]])'''