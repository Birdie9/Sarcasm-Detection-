from sklearn import svm
import csv


print "Training SVM"

clf = svm.LinearSVC()
trfile = open("./output1.csv","r")
reader = csv.reader(trfile)


X=[]
Y=[]

length = sum(1 for row in reader)
trfile.close()


trfile = open("./output1.csv","r")
reader = csv.reader(trfile)

i=0
for row in reader:
	if i<0.7*length:
		X.append( row[0:220] ) 	
		Y.append( row[len(row)-1] )
	i=i+1

clf.fit(X,Y)