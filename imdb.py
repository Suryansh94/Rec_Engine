from main_tweet import Detail
from datetime import datetime
import re
import json
import glob
import os

def extractRating(text):
    pattern = '([0-9]+)/10' 
    p = re.compile(pattern,re.M | re.I)
    matches = p.findall(text)
    if len(matches) != 0:
        rating = matches[0] 
    else:
        rating = ''
    return rating

def get_IMDB_id(imdb_link):    
    #http://www.imdb.com/title/tt0970866
    pattern = '.*?/tt([0-9]*)/*$' 
    p = re.compile(pattern,re.M | re.I)
    matches = p.findall(imdb_link)
    if len(matches) > 0:
        return matches[0]
    else:
        return -1    
    
def extractDataFromTweet(tweet):
    user = -1
    movie = -1
    rating = -1
    timestamp = -1
    try:
        #user
        print type(tweet)
        user = tweet['user']['id']
        #imdb id = movie id
        url = tweet['entities']['urls'][0]['expanded_url']
        movie = get_IMDB_id(url)
        #rating 
        rating = extractRating(tweet['text'])
        #timestamp
        timestamp = tweet['created_at']
        the_time = datetime.strptime(timestamp.replace(' +0000',''), '%a %b %d %H:%M:%S %Y')
        timestamp = (the_time-datetime(1970,1,1)).total_seconds()
        timestamp = int(timestamp)
        line = str(user) + '::'  + str(movie) + '::' + str(rating) +  '::' + str(timestamp) 
        # print line
    except:
        return user, movie, rating, timestamp    
    return user, movie, rating, timestamp
    
def extractDataset(tweets):
    dataset = list()
    for tweet in tweets:
        try:
            user, movie, rating, timestamp = extractDataFromTweet(tweet)
            if user == -1 or movie == -1 or rating == -1 or timestamp == -1:
                continue
            dataset.append((user, movie, rating, timestamp))
        except:
            continue
    return dataset
    
def writeDataset(dataset, filename):
    lines = list()
    for ((user, movie, rating, timestamp)) in dataset:
        line = str(user) + '::'  + str(movie) + '::' + str(rating) +  '::' + str(timestamp) + '\n'
        line = line.encode('UTF-8')
        lines.append(line)
    with file(filename, 'a') as outfile:
        outfile.writelines(lines)
    
def writeTweets(tweets, filename):
    line = json.dumps(tweets, ensure_ascii = False).encode('UTF-8')
    with file(filename, 'w') as outfile:
        outfile.writelines(line)
        
def get_since_id(path):
    since_id  = 0
    for infile in glob.glob( os.path.join(path, 'tweets_*.json') ):
        pattern = 'tweets_([0-9]*).json'
        p = re.compile(pattern,re.M | re.I)
        matches = p.findall(infile)
        id = int(matches[0])
        #keep maximum id
        since_id = max(id, since_id)
    return since_id

if __name__ == "__main__":        
    b = Detail()

    datasetpath = './'
    since_id = get_since_id(datasetpath)

    tweets, new_since_id =  b.searchTweets('I rated #IMDB', since_id)
    print "ji ",type(tweets)
    dataset = extractDataset(tweets)
    writeDataset(dataset, datasetpath + '/ratings.dat')
    writeTweets(tweets,datasetpath + '/tweets_' + str(new_since_id) + '.json')