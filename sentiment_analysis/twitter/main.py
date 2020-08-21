import os
import json
import tweepy
from asari.api import Sonar

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
KEYS_PATH = os.path.join(BASE_PATH, ".keys.json")

def read_auth_keys(keys_path):
    with open(keys_path) as f:
        text = f.read()
    return json.load(text)

def setup_tweepy(auth_keys):
    auth = tweepy.OAuthHandler(auth_keys.consumer_key, auth_keys.consumer_secret)
    auth.set_access_token(auth_keys.access_token, auth_keys.access_token_secret)
    return tweepy.API(auth)

def search_tweets(tweepy_api, query_text, items_count=100):
    for tweet in tweepy.Cursor(api.search, q=query_text).items(items_count):
        yield tweet

AUTH_KEYS = read_auth_keys(KEYS_PATH)
tweepy_api = setup_tweepy(AUTH_KEYS)

sonar = Sonar()
result = sonar.ping(text="Starship、結構微妙じゃね。フラフラしてるし。")
