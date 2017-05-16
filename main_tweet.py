from twitter import *
import sys

class Detail:
    t = None
    def __init__(self):
        token = 'YOUR_KEY'
        token_secret = 'YOUR_KEY'
        con_key = 'YOUR_KEY'
        con_secret = 'YOUR_KEY'
        
        try:        
            self.t = Twitter(auth=OAuth(token, token_secret, con_key, con_secret)) 
        except:
            print 'Error connecting to twitter' 
            sys.exit()
        
    def searchTweets(self, query, since):
        tweets = list()
        the_max_id = None #start with empty max
        the_max_id_oneoff = None
        new_since_id = since   
        
        number_of_iterations = 0
        while (number_of_iterations <= 1):
            number_of_iterations += 1
            count = 1 #maximum number of tweets allowed in one result set
            try:
                if the_max_id != None:
                    the_max_id_oneoff = the_max_id -1
                    res = self.t.search.tweets(q=query, result_type='recent', count=count,since_id=since,max_id=the_max_id_oneoff)
                else:
                    res = self.t.search.tweets(q=query, result_type='recent', count=count,since_id=since)
            except:
                print 'Error searching for tweets'
                return tweets, new_since_id
            
            try:
                # Extract the tweets from the results
                num_results = len(res['statuses'])
                print '  Found ' + str(num_results) + ' tweets.'
                for d in res['statuses']:    
                    tweets.append(d)
                    tweetid = d['id']
                    print d

                    if the_max_id == None or the_max_id > tweetid:
                        the_max_id = tweetid
    
                    if new_since_id < tweetid:
                        new_since_id = tweetid
                    
                #end the while loop if no more tweets were found
                if len(res['statuses']) == 0:
                    break
                #break #for debug (quits after 1 iteration of count tweets)
            except ValueError:
                print 'Error ', sys.exc_info()[0]
                traceback.print_exc(file=sys.stdout)
                return tweets, new_since_id
        return tweets, new_since_id