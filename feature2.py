# -*- coding: utf-8 -*-
import pandas
import pylab
from pandas import *
from pylab import *
import statistics as st
import re
import string
import sys
import math
import sys 
from string import ascii_lowercase 
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
from collections import Counter
from nltk.corpus import cmudict

stopwords1 = set(stopwords.words('english'))
d = cmudict.dict()
def nsyl(word):
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
    except Exception:
        #print "got exception in nsyl"
        pass
        return 0

def mode(list):
    data = Counter(list)
    data.most_common()
    value=data.most_common(1)
    return value[0][0]

#this is the final function which caluclates the divergence of current tweest from past tweets
def JS_function(d1,d2):
    mean = [(float(x)+ float(y))/2 for x,y in zip(d1, d2)]
    div1 = KL_function(d1,mean)
    div2 = KL_function(d2,mean)
    return float(0.5*div1) + float(0.5*div2)

def KL_function(t1,t2):
    sum1=0
    for i in range(len(t1)):
        x = float(t1[i])/float(t2[i])
        if x >0:
          value = math.log(x)*t1[i]
        else:
          value =0  
        sum1 =sum1+value
    return sum1

def feature2Extractor(list):
  ls=[]
  ls.append(st.mean(list))
  ls.append(st.median(list))
  try:
      ls.append(st.mode(list))
  except Exception as e:
      # print "exception in mode"
      ls.append(mode(list)) 
      
  if len(list)==1:
    ls.append(0)
  else:   
    ls.append(st.stdev(list))
  ls.append(min(list))
  ls.append(max(list))
  featureList = ls
  return featureList

def preprocessing(tweet):
  # #remove punctuation marks
  # tweet1 = tweet.translate(string.maketrans("",""), string.punctuation)
  # #remove any hyperlinks if present from the string.
  # URL_Less_tweet = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))''', '', tweet1)
  # #seperate into words
  # wordlist1 = re.split(" +",URL_Less_tweet)
  # #remove empty strings from list
  # wordlist1 = [i for i in wordlist1 if i != '']
  # #remove @"username" from tweet
  # wordlist = [word for word in wordlist1 if not word.startswith('@')]
  # # list should contain only words no numbers no links etc
  # my_list = [item for item in wordlist if item.isalpha()]
  # #count of each word in a list
  tweet = tweet.replace("#sarcasm","")
  tweet = tweet.replace("#sarcastic","")
  tweet = re.sub(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)", "", tweet)
  tweet = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet, flags=re.MULTILINE)
  table = string.maketrans("","")
  tweet=tweet.translate(table, "?/:^&*()!@$%:;',<.>-+*\{\}[]\"#")
  stemmer = SnowballStemmer("english",ignore_stopwords=True)
  tokens = tweet.split()
  tokens = [ w for w in tokens if w not in stopwords1]
  tokens = [item for item in tokens if item.isalpha()]
  tokens = [ stemmer.stem(w) for w in tokens ]
  #print tokens
  preproTweet=[len(i) for i in tokens]
  return preproTweet

def feature2(tweets,TestTweet):
    features = []
    feature2 = [0,0,0,0,0,0]
    totalCount = len(tweets)

    for i in range(totalCount):
        preproTweet = preprocessing(tweets.iloc[i].tweet)
        #print preproTweet
        if preproTweet == []:
          continue
        featureList = feature2Extractor(preproTweet)
        #print featureList
        for i in range(len(featureList)):
            feature2[i] = feature2[i]+featureList[i]
    d2=[]
    for i in feature2:
        d2.append(double(i)/double(totalCount)) #average distribution of the past data
    #calculating the feature list for TestTweet
    #print TestTweet.dtypes
    d1=[0,0,0,0,0,0]
    if len(TestTweet.index) > 0:
      tempList = re.findall("[a-zA-Z_]+",TestTweet.iloc[0].tweet)
      #number of words
      features.append(len(tempList))
      #number of syllables
      syllables =0
      polysyllables=0
      for word in tempList:
          numsyllables = nsyl(word)
          #number of polysyllables
          if numsyllables > 2:
              polysyllables = polysyllables+1
          syllables = syllables + numsyllables

      features.append(syllables)
      features.append(polysyllables)
      preproTweet = preprocessing(TestTweet.iloc[0].tweet)
      d1 = feature2Extractor(preproTweet)
      for feature in d1:
          features.append(feature)
    else:
      features.extend([0,0,0,0,0,0,0,0,0])
    
    divergence = JS_function(d1,d2)
    #print divergence
    features.append(divergence)
    return features

# #assuming already preprocessed tweets in a csv file are read, comment the preporcessing part
# if __name__ == '__main__':
#     tweets = read_csv('/home/jayati/Documents/sarcasmdet/Python Code/normal_with_past/user164.csv')
#     data1 = tweets.ix[0:,['time','tweet']] #ignore the first tweet
#     #remove retweets from the dataset
#     data2 = data1#2[~data1['tweet'].str.contains('RT @')]
#     data2.time = to_datetime(data2.time)
#     tweets = data2[1:]
#     TestTweet = data2.ix[0:0,['time','tweet']]
#     #print TestTweet
#     features = feature2(tweets,TestTweet)
#     print features
