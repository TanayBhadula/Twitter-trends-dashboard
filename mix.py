import tweepy
import os
import json
import csv
import geocoder
import pandas as pd
import numpy as np
from secure_key import *  



# Authorization and Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

if __name__ == "__main__":
    # Available Locations
    available_loc = api.trends_available()
    # writing a JSON file that has the available trends around the world
    with open("json_files/available_locs_for_trend.json","w") as wp:
        wp.write(json.dumps(available_loc,ensure_ascii=False, indent=1))

    with open('json_files/available_locs_for_trend.json') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    df = df.drop({'placeType'}, axis=1)
    df = df['country'].unique()
    df = pd.DataFrame(df)

    

    print("Running...")
    df.to_csv("countries/country.csv", index=False)

    data = pd.read_csv("country.csv")
    loc = data['0'].tolist()
    print(loc)



    # Trends for Specific Country
    #loc = ["India","Japan","Canada"]  #sys.argv[1]     # location as argument variable 
    
    for i in range(1,len(loc)):
        g = geocoder.osm(loc[i]) # getting object that has location's latitude and longitude

        closest_loc = api.trends_closest(g.lat, g.lng)
        trends = api.trends_place(closest_loc[0]['woeid'])
        # writing a JSON file that has the latest trends for that location
        with open("json_files/twitter_{}_trend.json".format(loc[i]),"w") as wp:
            wp.write(json.dumps(trends,ensure_ascii=False, indent=1))

        with open("json_files/twitter_{}_trend.json".format(loc[i])) as file1:
            data1 = json.load(file1)

        df = pd.DataFrame(data1[0]['trends'])
        if not df.empty:
            df.drop(columns='promoted_content', inplace=True)
            df = df.dropna(how='any',axis=0) 
            df.insert(4, 'country', loc[i])
            df.to_csv("csv_files/twitter_{}_trend.csv".format(loc[i]),index=False)

        else:
            continue

        
        print(loc[i])

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
