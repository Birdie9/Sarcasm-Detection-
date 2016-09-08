from sklearn import svm 
import csv
import numpy as np






print "Training SVM"
clf = svm.LinearSVC()
tariningFile = open("./output2.csv","r") 
reader = csv.reader(tariningFile)
from sklearn.metrics import accuracy_score

X=[]
Y=[]
length = sum(1 for row in reader)
print length
tariningFile.close()
tariningFile = open("./output2.csv","r") 
reader = csv.reader(tariningFile)

for i, row in enumerate(reader):
	#print row
	if ( (i<0.35*length) or (i>0.5*length and i<0.85*length) ):
		X.append(row[0:len(row)-1])
		Y.append(row[len(row)-1] )
		#print row[len(row)-1:]
#print Y
print len(X[0])
print len(Y)
clf.fit(X,Y)
tariningFile.close()
tariningFile = open("./output2.csv","r") 
reader = csv.reader(tariningFile)
num =0 
num2=0
test_predict=[]
test_real=[]
for i, row in enumerate(reader):
	if ( (i>=0.35*length and i<0.5*length) or (i>=0.85*length) ):
		num2=num2+1
		prediction = clf.predict( np.array(row[0:len(row)-1] ,dtype=float) )
		test_predict.extend(prediction)
		test_real.append( row[len(row)-1]  )
		if(prediction == row[len(row)-1:] ):
			num = num +1
print num2
print 0.3*length
accuracy =   (num*1.0)/(0.3*length) 

#print "The training accuracy is" +  str( clf.accuracy() ) 
print "The testing accuracy is " + str( accuracy )
print accuracy_score(test_real, test_predict)


#print clf.predict(...)
