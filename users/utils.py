from django.urls import resolve
from urllib.parse import urlparse

def is_last_url_named(url_name, last_url): #checks wether last url corresponds to name of django url
    try:
        path = urlparse(last_url).path
        last_url = resolve(path)
        if last_url.url_name == url_name:
            return True
        else:
            return False
    except Exception as e:
        return False