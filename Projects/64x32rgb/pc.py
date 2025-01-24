import requests
def get(url):
    print("GET: " + url)
    return requests.get(url).json()
def post(url):
    print("POST: " + url)
    return requests.post(url).json()