import csv

dict2 =	{'CC' : 0 ,	'CD' : 1 ,'DT' : 2 ,'EX' : 3 ,'FW' : 4 ,'IN' : 5 ,'JJ' : 6 ,'JJR' : 7 ,	'JJS' : 8 ,	 'LS' : 9 ,		 
	'MD' : 10 ,'NN' : 11 ,'NNS' : 12 ,	'NNP' : 13 ,	 'NNPS' : 14 ,'PDT' : 15,'POS' : 16 ,'PRP' : 17 ,'PRP$' : 18 ,'RB' : 19 ,		
	'RBR' : 20 ,'RBS' : 21 ,'RP' : 22 ,'SYM' : 23 ,'TO' : 24 , 'UH' : 25 ,'VB' : 26 ,'VBD' : 27 ,'VBG' : 28 ,'VBN' : 29 ,	
	'VBP' : 30 ,'VBZ' : 31 ,'WDT' : 32 ,'WP' : 33 ,'WP$' : 34 ,'WRB' : 35 ,'None' : 36 }


tariningFile = open("./output.csv","r") 
reader = csv.reader(tariningFile)

file2 = open("output2.csv","w")
wr = csv.writer(file2)

for row in reader:
	for j,i in enumerate(row):
		try:
			float(i)
		except:
			row[j] = dict2[i]
	wr.writerow(row)
