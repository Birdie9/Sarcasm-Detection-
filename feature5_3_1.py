import time
import datetime
from time import mktime
from datetime import datetime
def getnegscore(tweet, sentidict):
	ret=0.0
	for word in tweet:
		if word in sentidict:
			if sentidict[word]<0:
				ret+=sentidict[word]
	return -ret
def getposscore(tweet,sentidict):
	ret=0.0
	for word in tweet:
		if word in sentidict:
			if sentidict[word]>0:
				ret+=sentidict[word]
	return ret
def mood(tweet,past_data, sentidict,times):

	features=[]
	pos_score={}
	neg_score={}
	
	bucket_size=[1,2,5,10,20,len(past_data)]
	buckets=[]
	for pastt in past_data:
		pos_score[''.join(pastt)]=getposscore(pastt,sentidict)
		neg_score[''.join(pastt)]=getnegscore(pastt,sentidict)
	for n in bucket_size:
		buckets.append(past_data[0:n])
	for buck in buckets:
		pos_sum=0
		neg_sum=0
		p=1
		q=0
		n_pos=0
		n_neg=0
		n_neut=0
		for past_tweet in buck:
			pos_sum += pos_score[''.join(past_tweet)]
			neg_sum += neg_score[''.join(past_tweet)]
			if pos_score[''.join(past_tweet)]>neg_score[''.join(past_tweet)]:
				n_pos +=1
			elif pos_score[''.join(past_tweet)]<neg_score[''.join(past_tweet)]:
				n_neg +=1
			else:
				n_neut +=1
		if pos_sum<neg_sum:
			p=-1
		maxn = max(n_neg,n_pos,n_neut)
		if maxn==n_pos:
			q=1
		elif maxn==n_neg:
			q=-1
		else:
			q=0
		features.extend((pos_sum, neg_sum, p, max(pos_sum,neg_sum), n_pos,n_neg,n_neut,n_neg+n_pos+n_neut,q,maxn))
	
	time_intervals=[1, 2, 5, 10, 20, 60, 720, 1440] #minutes
	buckets=[]
	for interval in time_intervals:
		buck=[]
		for i in range(1,len(past_data)):
			if (datetime.fromtimestamp(mktime(times[0]))-datetime.fromtimestamp(mktime(times[i]))).seconds<=(interval*60):
				buck.append(past_data[i])
		buckets.append(buck)
	for buck in buckets:
		pos_sum=0
		neg_sum=0
		p=1
		q=0
		n_pos=0
		n_neg=0
		n_neut=0
		for past_tweet in buck:
			pos_sum += pos_score[''.join(past_tweet)]
			neg_sum += neg_score[''.join(past_tweet)]
			if pos_score[''.join(past_tweet)]>neg_score[''.join(past_tweet)]:
				n_pos +=1
			elif pos_score[''.join(past_tweet)]<neg_score[''.join(past_tweet)]:
				n_neg +=1
			else:
				n_neut +=1
		if pos_sum<neg_sum:
			p=-1
		maxn = max(n_neg,n_pos,n_neut)
		if maxn==n_pos:
			q=1
		elif maxn==n_neg:
			q=-1
		else:
			q=0
		features.extend((pos_sum, neg_sum, p, max(pos_sum,neg_sum), n_pos,n_neg,n_neut,n_neg+n_pos+n_neut,q,maxn))
	
	return features


