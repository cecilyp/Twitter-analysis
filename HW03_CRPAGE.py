# Homework 03
# Cecily Page

import json
import gzip
from string import punctuation
import random
import datetime
import collections
from pandas import Series
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import numpy as np

######## Question 1

total = 0
all_tweets = []
tweets_ids = set()
obama = []
romney = []
open_error = 0
close_error = 0

for line in gzip.open("HW03_twitterData.json.txt.gz", 'rt', encoding='utf-8'):
    total += 1
    if not line.strip().startswith("{"):
        line = "{" + line
        open_error += 1

    if not line.strip().endswith("}"):
        line = line + "}"
        close_error += 1

    tweet = json.loads(line.strip())

    if tweet['id_str'] in tweets_ids:
        continue

    all_tweets.append(tweet)
    tweets_ids.add(tweet['id_str'])

    if 'obama' in tweet['text'].lower() or 'barack' in tweet['text'].lower() or 'barry' in tweet['text'].lower():
        obama.append(tweet)
    if 'romney' in tweet['text'].lower() or 'mitt' in tweet['text'].lower():
        romney.append(tweet)

print('Data Set Stats')
print('---------------')
print('Total Number of tweets: ', total)
print('open bracket Errors: ', open_error)
print('close bracket Errors: ', close_error)
print('Number of Duplicate Tweets: ', total - len(all_tweets))
print('Number of tweets about Obama: ', len(obama))
print('Number of tweets about Romney: ', len(romney))

print('Data is cleaned')

##### Question 2


def get_dates_from_tweet(topic_tweets):
    topic_tweet_dates = []

    for topic_tweet in topic_tweets:
        topic_tweet = topic_tweet['created_at']
        topic_tweet = topic_tweet.split(",")
        topic_tweet = topic_tweet[1]
        topic_tweet = topic_tweet[:-6]
        topic_tweet_date = datetime.datetime.strptime(topic_tweet, " %d %b %Y %H")
        topic_tweet_dates.append(topic_tweet_date)

    return topic_tweet_dates


romney_dates = get_dates_from_tweet(romney)
obama_dates = get_dates_from_tweet(obama)

obama_dates.sort()
romney_dates.sort()

rcounts_counter = collections.Counter(romney_dates)
ocounts_counter = collections.Counter(obama_dates)

rcounts = [rcounts_counter[date] for date in romney_dates]
ocounts = [ocounts_counter[date] for date in obama_dates]


plt.plot_date(romney_dates, rcounts, 'b-', color='red')
plt.plot_date(obama_dates, ocounts, 'b-', color='blue')

red_patch = mpatches.Patch(color='red', label='Romney Tweets')
blue_patch = mpatches.Patch(color='blue', label='Obama Tweets')
plt.legend(handles=[red_patch, blue_patch])

plt.title('Number of Tweets About Obama and Romney by Time')
plt.xlabel('Date')
plt.ylabel('Number Of Tweets')
plt.gcf().autofmt_xdate()
plt.show()

print('plot is created')

##### Question 3


def get_word_content(tweet_list):
    exclude = set(punctuation) # Keep a set of "bad" characters.

    all_words = []
    for tweet in tweet_list:
        tweet_text = tweet['text'].lower()
        tweet_text = [char for char in tweet_text if char not in exclude]
        tweet_text = "".join(tweet_text)
        [all_words.append(u_word) for u_word in tweet_text.split()]

    return collections.Counter(all_words)


all_word_counts = get_word_content(all_tweets)
obama_word_counts = get_word_content(obama)
romney_word_counts = get_word_content(romney)


words_in_both = obama_word_counts & romney_word_counts

word_scores = {}
for word, count, in words_in_both.items():
    o = obama_word_counts[word]
    r = romney_word_counts[word]
    score = (o-r)/(o+r)
    word_scores[word] = score


# print('counter ', word_scores)
scores_sorted = sorted(list(word_scores.items()), key=lambda x: x[1], reverse=False)

# print(scores_sorted)

with open('word_weights.txt', 'w', encoding='utf-8') as f:
    for i in range(0, 100):
        f.write("{:<20} {:<3.3f} {:<20} {:<3.3f} \n".format(scores_sorted[-(i+1)][0], scores_sorted[-(i+1)][1], scores_sorted[i][0], scores_sorted[i][1]))
