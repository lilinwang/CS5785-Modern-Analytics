# -*- coding: utf-8 -*-
'''
This simple file is using logistic regression to predict whether a passenger survived the titanic disaster.
Input file: http://www.kaggle.com/c/titanic-gettingStarted

__author__ = 'Lilin Wang'
__date__ = '2014/09/27'

'''
import csv as csv
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

#calculate the Pearson’s correlation coefficient between 2 vectors 
def pearson(x,y):
    n=len(x)
    vals=range(n)
    # Simple sums
    sumx=sum([float(x[i]) for i in vals])
    sumy=sum([float(y[i]) for i in vals])
    # Sum up the squares
    sumxSq=sum([x[i]**2.0 for i in vals])
    sumySq=sum([y[i]**2.0 for i in vals])
    # Sum up the products
    pSum=sum([x[i]*y[i] for i in vals])
    # Calculate Pearson score
    num=pSum-(sumx*sumy/n)
    den=((sumxSq-pow(sumx,2)/n)*(sumySq-pow(sumy,2)/n))**.5
    if den==0: return 0
    r=num/den
    return r


#print pearson correlation coefficient for Sibsp and Parch
csv_file_object = csv.reader(open('train.csv', 'rb')) 	# Load in the csv file
header = csv_file_object.next()     
pdata=[]
for line in csv_file_object: 
    a1=int(line[6])
    a2=int(line[7])
    pdata.append([a1,a2])    
pdata=np.array(pdata)  
print "Pearson’s correlation coefficient between Sibsp and Parch = "
print pearson(pdata[0],pdata[1])


#Train data
csv_file_object = csv.reader(open('train.csv', 'rb')) 	# Load in the csv file
header = csv_file_object.next() 						# Skip the fist line as it is a header
data=[] 												# Create a variable to hold the data
								
for line in csv_file_object:          
        survived=int(line[1])
        pclass = float(line[2])
        if (line[4]=='female'): 
            sex=1
        else :
            sex=0
        if (line[5]!=''): age = float(line[5])
        else :age=0
        relative = int(line[7])
        if (line[9]==''): fare=float(-1)
        else : fare = float(line[9])
        snum=0
        cnum=0
        qnum=0
        if (line[11]=='S'): 
            embarked=int(1)
            snum=snum+1
        elif (line[11]=='C'): 
            embarked=int(2)
            cnum=cnum+1
        elif (line[11]=='Q'): 
            embarked=int(3)
            qnum=qnum+1
        else :embarked=int(0)
        data.append([survived,pclass,sex,age,relative,fare,embarked])
        
data = np.array(data) 	    # Then convert from a list to an array.  


# Data cleanup
# All missing Age -> just assign the mean of all ages
data[(data[:,3] ==0),3]=np.mean(data[(data[:,3]!=0),3])
# All missing Embarked -> just make them embark from most common place
defaultembarked=1
if (snum<cnum):
    snum=cnum
    defaultembarked=2
if (snum<qnum):
    snum=qnum
    defaultembarked=3
data[(data[:,6]==0),6]=defaultembarked
# All missing Fare -> just assign the mean of all fares
data[(data[:,4] ==0),4]=np.mean(data[(data[:,4]!=0),4])


#Test Data
test_csv_file_object = csv.reader(open('test.csv', 'rb')) 	# Load in the csv file
header = test_csv_file_object.next() 						# Skip the fist line as it is a header
testdata=[] 												# Create a variable to hold the data
ids=[]								
for line in test_csv_file_object:
            ids.append(int(line[0]))                      
            pclass = float(line[1])
            if (line[3]=='female'): 
                sex=1
            else :
                sex=0
            if (line[4]!=''): age = float(line[4])
            else :age=0
            relative = int(line[6])           
            if (line[8]==''): fare=float(-1)
            else : fare = float(line[8])
            snum=0
            cnum=0
            qnum=0
            if (line[10]=='S'): 
                embarked=int(1)
                snum=snum+1
            elif (line[10]=='C'): 
                embarked=int(2)
                cnum=cnum+1
            elif (line[10]=='Q'): 
                embarked=int(3)
                qnum=qnum+1
            else :embarked=int(0)
            testdata.append([pclass,sex,age,relative,fare,embarked])

ids=np.array(ids)
testdata = np.array(testdata) 									# Then convert from a list to an array.  


# Data cleanup
# All missing Age -> just assign the mean of all ages
testdata[(testdata[:,2] ==0),2]=np.mean(testdata[(testdata[:,2]!=0),2])
# All missing Embarked -> just make them embark from most common place
defaultembarked=1
if (snum<cnum):
    snum=cnum
    defaultembarked=2
if (snum<qnum):
    snum=qnum
    defaultembarked=3
testdata[(testdata[:,5]==0),5]=defaultembarked
# All missing Fare -> just assign the mean of all fares
data[(data[:,3] ==0),3]=np.mean(data[(data[:,3]!=0),3])

target_data = data[:,0] #Survived
train_data = data[:,1:6]#Train data: Pclass, Sex, Age, Parch+Sibling, Fare, Embarked
test_data = testdata[:,0:5]#Test data: Pclass, Sex, Age, Parch+Sibling, Fare, Embarked


#logistic regression fit
print 'Training...'
clf = LogisticRegression().fit(train_data,target_data)

print 'Predicting...'
output = clf.predict(test_data)

predictions_file = open("hw1-2.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(ids, output))
predictions_file.close()
print 'Done.'