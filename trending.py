import tweepy
import os
import json
import csv
import sys
import geocoder
import pandas as pd
import numpy as np
from secure_key import *  

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

trends = api.trends_place(1)
        # writing a JSON file that has the latest trends for that location
with open("json_files/twitter_global_trend.json","w") as wp:
    wp.write(json.dumps(trends,ensure_ascii=False, indent=1))

with open("json_files/twitter_global_trend.json") as file1:
    data1 = json.load(file1)

df = pd.DataFrame(data1[0]['trends'])
if not df.empty:
    df.drop(columns='promoted_content', inplace=True)
    df = df.dropna(how='any',axis=0) 
    df.insert(4, 'country', 'Worldwide')
    df.to_csv("csv_files/twitter_global_trend.csv",index=False)


