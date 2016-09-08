def hashtag(words):
	feature =[] 	
	hashtags_part1 =0 
	hashtags_part2=0
	hashtags_part3 =0	

	for i in range(0,len(words)):
		#print words[i]
		if(words[i][0]=='#'):
			if(i< len(words)/3):
				hashtags_part1=hashtags_part1+1
			elif(i<( len(words)*2)/3): 
				hashtags_part2=hashtags_part2+1
			else:
				hashtags_part3=hashtags_part3+1 
	#trisecting the number of hashtags 	

	feature.append(hashtags_part1)
	feature.append(hashtags_part2)
	feature.append(hashtags_part3)

	return feature