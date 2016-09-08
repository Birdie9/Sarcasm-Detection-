# -*- coding: utf-8 -*-
import sys 
from string import ascii_lowercase 
import codecs
import string
reload(sys)  
sys.setdefaultencoding('utf8')
import string
import time
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
from nltk import pos_tag
from nltk import FreqDist
from sklearn import svm
import os
import csv

from preproc import *
from feature1 import *
from feature3 import *
from feature2 import *
from feature4 import *
from feature5 import *
from feature5_3_1 import *
from feature5_3_3 import *
stopwords = set(stopwords.words('english'))
affectdict ={}
sentidict={}
bidict={}
tridict={}
 
#X = [[0,0] , [1,1] ]
#Y = [0,1]


def init_dicts():
	global affectdict
	global sentidict
	global bidict
	global tridict
	with open('affectscores.txt','r') as file1:
		for line in file1:
			temp = line.split()
			affectdict[temp[0]]=float(temp[1])
	with open('senti.txt','r') as file2:
		for line in file2:
			temp = line.split()
			sentidict[temp[0]]=float(temp[1])
	with open('bigramscore.txt','r') as file2:
			for line in file2:
				temp = line.split()
				bidict[temp[0]]=float(temp[1])
	with open('trigramscore.txt','r') as file2:
		for line in file2:
			temp = line.split()
			tridict[temp[0]]=float(temp[1])
	print 'initialised dictionaries!'

def emojiFeatures(raw_tweet):
	features=[]
	possum=0
	posnum=0
	negsum=0
	negnum=0
	emoji={'😜':2,'😂':6, '😀':3, '😷':-1, '♥':5, '😡':-4, '😍':5,'😌':3,'👀':1,'😝':2,'😘':4.5,'😁':5,'😆':6,'😢':-6,'😓':-5,'😎':4.5,'😞':-3,'💔':-7,'😚':4, '😕':-2,'😩':-5,'👌':4,'😭':-6}
	punct=['?','!','\"']
	for emo in emoji.keys():
		#features.append(raw_tweet.count(emo))
		if raw_tweet.count(emo)>0:
			if emoji[emo]<0:
				negnum += raw_tweet.count(emo)
				negsum += raw_tweet.count(emo)*emoji[emo]
			else:
				posnum += raw_tweet.count(emo)
				possum += raw_tweet.count(emo)*emoji[emo]
	features.extend((possum,negsum))
	for p in punct:
		features.append(raw_tweet.count(p))
	features.append(len(filter(lambda x:x.isupper(),list(raw_tweet))))
	return features

def getFeatureHelper(tweet ,past_data,times, file_path):
	features = []
	try:
		tweets = read_csv(file_path)
		data1 = tweets.ix[0:,['time','tweet']] #ignore the first tweet
		#remove retweets from the dataset
		data2 = data1#[~data1['tweet'].str.contains('RT @')]
		data2.time = to_datetime(data2.time)
		tweets = data2[1:]
		TestTweet = data2.ix[0:0,['time','tweet']]
		features1 = feature2(tweets,TestTweet)
		features.extend(features1)
		features2 = frustration(tweets,TestTweet)
		features.extend(features2)
		#print len(features)
	except Exception as e:
		print e
		os.remove(file_path)
		print file_path

		print"error in feature 2 or 5.3.3"
		

	try:
		features.extend(contrastingFeatures(tweet,affectdict,sentidict,bidict,tridict))
		#print len(features)
	except Exception as e:
		print e
		print "error in feature 1"
	try:
		features.extend(affectSentiment(tweet,affectdict,sentidict))
		#print len(features)
	except Exception as e:
		print e
		print "error in feature3"
	try:
		features.extend(familiarityLanguage(tweet,past_data))
		#print len(features)
	except Exception as e:
		print e

		print "error in feature4"
	try:
		features.extend(structuralVariations(tweet,affectdict,sentidict))
		#print len(features)
	except Exception as e:
		print e
		print "error in feature5"

	try:
		features.extend(mood(tweet,past_data, sentidict,times))
		#print len(features)
	except:
		print "error in feature 5.3.1"

	#add other functions
	#print 'features=' 
	#print features
	return features
	#call the list of features
	# the list of feature will be written into a file directly 
	


def main():

	init_dicts()  #initialize the dictionaries 

	trainingFile = open("output.csv",'a')
	wr = csv.writer(trainingFile, quoting=csv.QUOTE_ALL)

	path_sarcastic = os.path.abspath("/home/jayati/Documents/sarcasmdet/Python Code") + "/sarcastic_with_past"
	fileListSarcastic = os.listdir(path_sarcastic)
	c=0
	for i in fileListSarcastic:
		print c
		c+=1
		list_tweets = []
		features = []
		tweet_times=[]
		hashf=[]
		try:
			with open(path_sarcastic+'/'+i) as tweet_file:
				hashf=[]
				file_reader = csv.DictReader(tweet_file)
				firstrowdone=False
				for row in file_reader:
						try:

							words = preprocess(row['tweet'],stopwords)
							if words==[]:
								if firstrowdone:
									continue
								else:
									break
							if hashf != []:
								hashf = hashtag(row['tweet'])
							removed_timezone=row['time'].replace('IST','')
							removed_timezone=removed_timezone.replace('+0000 ','')
							tweet_times.append(time.strptime(removed_timezone))
							list_tweets.append(words)
							firstrowdone=True
						except Exception as e:
							if firstrowdone:
								continue
							else:
								break
							print 'exception'
							print e
			if firstrowdone:
				try:
					words = list_tweets[0]
					past = list_tweets[1:]
					features = getFeatureHelper(words , past,tweet_times, path_sarcastic+'/'+i)
					features.extend(emojiFeatures(row['tweet']))
					features.extend(hashf)
					features.append(1)
					wr.writerow(features) 
				except Exception as e:
					print e
					print i
			else:
				os.remove(path_sarcastic+'/'+i)
				print 'sample '+i+' discarded'
		except Exception as e:
			print e
		
	
	path_normal = os.path.abspath("/home/jayati/Documents/sarcasmdet/Python Code") + "/normal_with_past"
	fileListNormal  = os.listdir(path_normal)
	for i in fileListNormal:
		list_tweets = []
		features = []
		tweet_times=[]
		hashf=[]
		try:
			with open(path_normal+'/'+i) as tweet_file:
				hashf=[]
				file_reader = csv.DictReader(tweet_file)
				firstrowdone=False
				for row in file_reader:
						try:
							words = preprocess(row['tweet'],stopwords)
							if words==[]:
								if firstrowdone:
									continue
								else:
									break
							if hashf != []:
								hashf = hashtag(row['tweet'])
							removed_timezone=row['time'].replace('IST','')
							removed_timezone=removed_timezone.replace('+0000 ','')
							tweet_times.append(time.strptime(removed_timezone))
							list_tweets.append(words)
							firstrowdone=True
						except Exception as e:
							if firstrowdone:
								continue
							else:
								break
							print 'exception'
							print e
			if firstrowdone:
				try:
					words = list_tweets[0]
					past = list_tweets[1:]
					features = getFeatureHelper(words , past,tweet_times,path_normal+'/'+i )
					features.extend(emojiFeatures(row['tweet']))
					features.extend(hashf)
					features.append(0)
					wr.writerow(features) 
				except Exception as e:
					print e
					print i
			else:
				os.remove(path_normal+'/'+i)
				print 'sample '+i+' discarded'
		except Exception as e:
			print e


if __name__=="__main__":
	main()
	# main function for the whole project 
	# command line argument format 
	# positivetweets negativetweets
