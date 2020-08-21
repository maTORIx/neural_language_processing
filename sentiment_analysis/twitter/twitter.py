import os
import json
import requests


FIELD_TYPES = set([
    "attachments",
    "author_id",
    "context_annotations",
    "conversation_id",
    "created_at",
    "entities",
    "geo",
    "id",
    "in_reply_to_user_id",
    "lang",
    "non_public_metrics",
    "organic_metrics",
    "possibly_sensitive",
    "promoted_metrics",
    "public_metrics",
    "referenced_tweets",
    "source",
    "text",
    "withheld"
])


# source from https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
MAX_RESULTS = 100 # max results per 1 request
MAX_ACCESS = 180
INTERVAL = 15 * 60 * 1000 # 5 minutes


def create_search_url(query, fields=["text", "created_at"], exclude_retweet=True, max_results=100, next_token=None):
    if type(query) is not str or len(query) < 1:
        raise ValueError("Invalid query. Query require string longer than 1.")
    elif len(fields) < 1:
        raise ValueError("Invalid fields. No field selected.")
    elif max_results > MAX_RESULTS:
        raise ValueError("Invalid max_value, Max value max is 100")

    # validate fields
    fields_set = set(fields)
    unknown_types = fields_set - FIELD_TYPES & fields_set
    if len(unknown_types) > 0:
        raise ValueError("Invalid fields. {} is not found.".format(str(unknown_types)))

    # when exclude retweet
    if exclude_retweet:
        query = query + " -is:retweet"

    BASE_URL = "https://api.twitter.com/2/tweets/search/recent"
    url =  BASE_URL + "?query={}&tweet.fields={}&max_results={}".format(
        query,
        ",".join(fields),
        str(max_results)
    )

    # when next token is not None
    if next_token is not None:
        url = url + "&next_token={}".format(next_token)

    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def search_twitter(bearer_token, query, fields=["text", "created_at"], exclude_retweet=True, max_results=100, next_token=None):
    url = create_search_url(query, fields, exclude_retweet, max_results, next_token)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    return json_response
