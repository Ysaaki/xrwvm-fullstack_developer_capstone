import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint
    print("GET from {} ".format(request_url))
    try:
        # Passing kwargs directly to params automatically handles URL encoding safely
        response = requests.get(request_url, params=kwargs)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return []


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"sentiment": "neutral"}


# Renamed from post_review to post_request to match your view proxy execution requirements
def post_review(endpoint, json_data):
    request_url = backend_url + endpoint
    print("POST to {} ".format(request_url))
    try:
        response = requests.post(request_url, json=json_data)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None
