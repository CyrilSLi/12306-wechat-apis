import requests, time
def get(url):
    return requests.get(url).json()
def post(url):
    return requests.post(url).json()