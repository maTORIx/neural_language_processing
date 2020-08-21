import os
import json
import math
import requests
import tqdm
from asari.api import Sonar

import twitter

def fetch_tweets(bearer_token, query, max_search=1000):
    tweets = []
    next_token = None
    max_result = 100
    if max_search < max_result:
        max_result = max_search
    for i in tqdm.tqdm(range(math.ceil(max_search / max_result))):
        result = twitter.search_twitter(
            bearer_token,
            query,
            fields=["text", "created_at", "public_metrics"],
            next_token=next_token
        )
        next_token = result["meta"]["next_token"]
        tweets += result["data"]
    return tweets

def analyze_tweets(tweets):
    sonar = Sonar()
    results = []
    for tweet in tqdm.tqdm(tweets):
        result = sonar.ping(tweet["text"])
        results.append({
            "top_class": result["top_class"],
            "negative": result["classes"][0]["confidence"],
            "positive": result["classes"][1]["confidence"],
            "retweet_count": tweet["public_metrics"]["retweet_count"],
            "like_count": tweet["public_metrics"]["like_count"],
            "created_at": tweet["created_at"],
            "text": tweet["text"]
        })
    return results

if __name__ == "__main__":
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    KEYS_PATH = os.path.join(BASE_PATH, "keys.json")
    with open(KEYS_PATH) as f:
        text = f.read()
    keys = json.loads(text)
    bearer_token = keys['bearer_token']
    query = input("Search: ")

    tweets = fetch_tweets(bearer_token, query, max_search=100)
    analyzed_results = analyze_tweets(tweets)

    result = ""
    result += "top_class,negative,positive,retweet_count,like_count,created_at\n"
    for item in analyzed_results:
        result += "{},{},{},{},{},{}\n".format(
            item["top_class"],
            str(float(item["negative"])),
            str(float(item["positive"])),
            str(item["retweet_count"]),
            str(item["like_count"]),
            item["created_at"]
        )
    with open("{}.csv".format(query), "w") as f:
        f.write(result)
