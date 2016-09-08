# -*- coding: utf-8 -*-
import pandas
import pylab
import re
from pandas import *
from pylab import *
from datetime import datetime
from dateutil import relativedelta



#used to check if the tweet to be tested contains the swear words
def swearWord(tweet):
    feature3=False
    Swearwords =["shit","fuck","damn","bitch","crap","piss","dick","darn","cock","pussy","asshole","fag","bastard","slut","douche","bloody","cunt","bugger","bollocks","arsehole"]
    for item in Swearwords:
        if item in tweet:
            feature3=True
    return feature3
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
  #count of each word in a list
  tweet = tweet.replace("#sarcasm","")
  tweet = tweet.replace("#sarcastic","")
  tweet = re.sub(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)", "", tweet)
  tweet = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet, flags=re.MULTILINE)
  table = string.maketrans("","")
  tweet=tweet.translate(table, "?/:^&*()!@$%:;',<.>-+*\{\}[]\"#")
  stemmer = SnowballStemmer("english",ignore_stopwords=True)
  tokens = tweet.split()
  tokens = [ w for w in tokens if w not in stopwords]
  tokens = [item for item in tokens if item.isalpha()]
  tokens = [ stemmer.stem(w) for w in tokens ]
  return tokens

def TimeDifference(curTweet, prevTweet):
    date_1 = prevTweet
    date_2 = curTweet
    #This will find the difference between the two dates
    difference = relativedelta.relativedelta(date_2, date_1)
    details = []
    #details.append(difference.years)
    #details.append(difference.months)
    details.append(difference.days)
    details.append(difference.hours)
    details.append(difference.minutes)
    details.append(difference.seconds)
    #print "Difference is %s year, %s months, %s days, %s hours, %s minutes %s seconds" %(difference.years, difference.months, difference.days, difference.hours, difference.minutes,difference.seconds)

    #return a list containing details [years,months,days, hours, min, sec]
    return details


# Aims at deriving the probability distribution of tweeting pattern of the user, and other two features
def frustration(tweets,TestTweet):
    features = []
    '''feature1 : input for this feature would be last 2 months tweets with timestamps'''
    totalCount = len(tweets)

    times = tweets['time']
    intervals = {}
    for t in times:
        try:
            hr = t.hour
        except Exception as e:
            print e 
        if hr not in intervals:
            intervals[hr] = 0
        intervals[hr]+=1

    # print intervals
    # for k in sorted(intervals.keys()):
    #     print "%s:00-%s:00  %s" % (k,int(k)+1,intervals[k])

    testInterval = TestTweet.time.iloc[0].hour
    if testInterval not in intervals:
        features.append(0)
    else:    
        features.append(double(intervals[testInterval])/double(totalCount))

    '''feature2 : Input for this feature would be current tweet timestamp and previous tweet timesatmp'''
    details = TimeDifference(TestTweet.iloc[0].time, tweets.iloc[0].time)
    for values in details:
        features.append(values)

    '''Feature 3 checks if the tweet contain a swearword: boolean'''
    features.append(swearWord(TestTweet['tweet']))
    return features


# Tweet at the top that data[0] is considered as the tweet for testing
if __name__ == '__main__':
    tweets = read_csv('/home/jayati/Documents/sarcasmdet/Python Code/normal_with_past/user174.csv')   # creating a dataframe from a csv file
    data1 = tweets.ix[0:,['time','tweet']]
    #remove retweets from the dateset
    data2 = data1#[~data1['tweet'].str.contains('RT @')]
    data2.time = to_datetime(data2.time)
    tweets = data2[1:]
    TestTweet = data2.ix[0:0,['time','tweet']]
    #print len(TestTweet.index)
    features = frustration(tweets,TestTweet)
    print features
