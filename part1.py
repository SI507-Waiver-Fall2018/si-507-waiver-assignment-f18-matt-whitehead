# these should be the only imports you need
import tweepy
import nltk
import json #don't think I need this, but ¯\_(ツ)_/¯. maybe UMSI people are used to dealing with json instead of tweepy classes?
import sys

# write your code here
# usage should be python3 part1.py <username> <num_tweets>
#Grab the args
arg_user = sys.argv[1]
arg_num = int(sys.argv[2])

#open connection to Twitter API & pull data
auth = tweepy.OAuthHandler("tFswh787HlGNHMMomxsLVbdpe", "CZhxukWhlUbqUkiZ0RPMRxp1vYfyz7sBp4FA1uViuDJhYHcQAP")
auth.set_access_token("1007399022968098816-3aYCpcR0Sn0HbcNyiw5TkHEFldl8lF", "ZzN97o5CCRmyfPObskMN3tWVlJtvOErNzr06b6Q6urDFl")
api = tweepy.API(auth)
all_tweets = api.user_timeline(screen_name = arg_user, count = arg_num, tweet_mode = "extended")
no_rt = api.user_timeline(screen_name = arg_user, count = arg_num, tweet_mode = "extended", include_rts = False)

#Calculate basic counts
fav_count = 0
rt_count = 0
for i in range(0, len(no_rt)):
    fav_count += no_rt[i].favorite_count
    rt_count += no_rt[i].retweet_count
num_analyzed = len(all_tweets) #arg_num could be > user's tweet count, we want actual API response tweets
og_tweet_count = len(no_rt)

#Grab all the text data & filter out stop words
raw_text_data = ""
for i in range(0, len(all_tweets)):
    #this stops retweets from getting truncated
    try:
        raw_text_data += all_tweets[i].retweeted_status.full_text + " " #the full text of retweets is stored in a different part of the API response – intuitive!
    except:
        raw_text_data += all_tweets[i].full_text + " "
raw_list = raw_text_data.split()
abc_list = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") #gross work around since I can't use regex for this or string.ascii_lowercase
filtered_list = list(filter(lambda x: x[0] in abc_list and 'http' not in x and x != 'RT', raw_list))

#POS tagging
filtered_string = " ".join(filtered_list)
tokens = nltk.word_tokenize(filtered_string)
tags = nltk.pos_tag(tokens)
nouns_list = []
verbs_list = []
adj_list = []
for k,v in tags:
    if v[0:2] == "NN":
        nouns_list.append(k)
    elif v[0:2] == "VB":
        verbs_list.append(k)
    elif v[0:2] == "JJ":
        adj_list.append(k)
nouns_list = list(filter(lambda x: x != "’", nouns_list)) #nltk keeps tagging ’ as a noun

#Calculate all the NLP counts
noun_counts = {x:nouns_list.count(x) for x in nouns_list}
verb_counts = {x:verbs_list.count(x) for x in verbs_list}
adj_counts = {x:adj_list.count(x) for x in adj_list}
popular_nouns = sorted(noun_counts.items(), key = lambda x: (-x[1],x[0]))
popular_verbs = sorted(verb_counts.items(), key = lambda x: (-x[1],x[0]))
popular_adjs = sorted(adj_counts.items(), key = lambda x: (-x[1],x[0]))

#Write to csv
import csv
with open("noun_data.csv", "w") as csv_file:
    csv_out = csv.writer(csv_file)
    csv_out.writerow(['Noun', 'Number'])
    csv_out.writerows(popular_nouns[0:5])

#Print out everything
def print_words(word_list):
    for w,c in word_list[0:5]:
        print(w + "(" + str(c) + ")", end=" ")
    return None
print("USER: ", arg_user)
print("TWEETS ANALYZED: ", num_analyzed)
print("VERBS: ", end=" ")
print_words(popular_verbs)
print("\nNOUNS: ", end=" ")
print_words(popular_nouns)
print("\nADJECTIVES: ", end=" ")
print_words(popular_adjs)
print("\nORIGINAL TWEETS: ", og_tweet_count)
print("TIMES FAVORITED (ORIGINAL TWEETS ONLY): ", fav_count)
print("TIMES RETWEETED (ORIGINAL TWEETS ONLY): ", rt_count)
