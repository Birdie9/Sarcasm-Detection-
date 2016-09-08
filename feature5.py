import nltk
#from feature1 import *
def structuralVariations(words , affectdict , sentidict):
	feature = []
	tags = nltk.pos_tag(words)
	#print tags
	try:
		feature.append( tags[0][1] )
	except:
		feature.append('None')
	
	try:
		feature.append( tags[1][1] )
	except:
		feature.append('None')
	
	try:
		feature.append( tags[2][1] )
	except:
		feature.append('None')
	
	try:
		feature.append( tags[len(words)-3][1] )
	except:
		feature.append('None')
	
	try:
		feature.append( tags[len(words)-2][1] )
	except:
		feature.append('None')
	
	try:
		feature.append( tags[len(words)-1][1] )
	except:
		feature.append('None')

	flag=0
	for i in range (0,len(words)):
		if( words[i] in affectdict):
			feature.append(i+1)
			flag=1
			break
	if(flag==0):
		feature.append(0)
	
	flag=0
	for i in range (0,len(words)):
		if( words[i] in sentidict):
			feature.append(i+1)
			flag=1
			break
	if(flag==0):
		feature.append(0)


	
	#print feature
	return feature




#a = []
#b = []
#structuralVariations(["hello" , "bye" ],a,b)
