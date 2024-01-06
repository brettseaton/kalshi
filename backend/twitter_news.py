# import requests

# def get_tweets(bearer_token, query, tweet_fields):
#     headers = {
#         "Authorization": f"Bearer {bearer_token}"
#     }
#     params = {
#         "query": query,
#         "tweet.fields": tweet_fields
#     }
#     response = requests.get("https://api.twitter.com/2/tweets/search/recent", headers=headers, params=params)
    
#     if response.status_code != 200:
#         raise Exception(f"Request returned an error: {response.status_code} {response.text}")

#     return response.json()

# # Your Bearer Token
# bearer_token = "AAAAAAAAAAAAAAAAAAAAAIX8rQEAAAAAEejjZwm4S1Onh6uRcY6LxWJGIBg%3D43tud6IO4WrQj4OK0qoZx1VORT2PG3qEcrQyREPQIrzcdLZwd2"

# # Define your keywords
# keywords = ["kanye", "vultures", "release", "date"]  # Replace with your keywords

# # Constructing the query with keywords
# # Spaces between keywords imply logical 'AND'
# query = " ".join(keywords)

# # Fields you want to retrieve
# tweet_fields = "created_at,author_id,text"

# # Get tweets
# tweets = get_tweets(bearer_token, query, tweet_fields)

# # Process the received tweets
# for tweet in tweets.get("data", []):
#     print(f"{tweet['id']}: {tweet['created_at']}: {tweet['text']}")



# def get_rules():
#     response = requests.get(
#         "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
#     )
#     if response.status_code != 200:
#         raise Exception(
#             f"Cannot get rules (HTTP {response.status_code}): {response.text}"
#         )
#     print(json.dumps(response.json()))
#     return response.json()


# def delete_all_rules(rules):
#     if rules is None or "data" not in rules:
#         return None

#     ids = [rule["id"] for rule in rules["data"]]
#     payload = {"delete": {"ids": ids}}
#     response = requests.post(
#         "https://api.twitter.com/2/tweets/search/stream/rules",
#         auth=bearer_oauth,
#         json=payload
#     )
#     if response.status_code != 200:
#         raise Exception(
#             f"Cannot delete rules (HTTP {response.status_code}): {response.text}"
#         )
#     print(json.dumps(response.json()))

import requests
import json
import base64

# Your consumer key and secret
consumer_key = "bGp0eWtQQnNiamVZT21IVWhLUFQ6MTpjaQ"
consumer_secret = "iFbNb1BZtLxVcejbWjpiwaskW8Vv51PiaOg2jlpi83lZDG4CxQ"

def get_bearer_token(consumer_key, consumer_secret):
    # URL encode the consumer key and secret
    encoded_key_secret = f"{consumer_key}:{consumer_secret}".encode('ascii')
    # Base64 encode the string
    b64_encoded_key_secret = base64.b64encode(encoded_key_secret)

    headers = {
        "Authorization": f"Basic {b64_encoded_key_secret}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }

    response = requests.post(
        "https://api.twitter.com/oauth2/token",
        headers=headers,
        data={'grant_type': 'client_credentials'}
    )

    if response.status_code != 200:
        raise Exception(f"Cannot get token (HTTP {response.status_code}): {response.text}")

    return response.json()["access_token"]

# Get the Bearer Token
bearer_token = get_bearer_token(consumer_key, consumer_secret)

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def set_rules():
    # Adjust the rules as needed
    sample_rules = [
        {"value": "Kanye Vultures Release Date Changed", "tag": "Kanye release updates"}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            f"Cannot add rules (HTTP {response.status_code}): {response.text}"
        )
    print(json.dumps(response.json()))


def get_stream():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            f"Cannot get stream (HTTP {response.status_code}): {response.text}"
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))


def main():
    # rules = get_rules()
    # delete = delete_all_rules(rules)
    set_rules()
    get_stream()


if __name__ == "__main__":
    main()
