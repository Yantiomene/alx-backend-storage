#!/usr/bin/env python3
"""implement a get_page function
(prototype: def get_page(url: str) -> str:).
The core of the function is very simple.
It uses the requests module to obtain the HTML
content of a particular URL and returns it.
"""
import requests
import redis
from functools import wraps
from typing import Callable

r = redis.Redis()
EXPIRATION_TIME = 10


def count_url_access(fn: Callable) -> Callable:
    """Decorator to count url access"""

    @wraps(fn)
    def wrapper(url):
        """Wrapper function for the decorator"""
        key = "cached:" + url
        if r.get(key):
            return r.get(key).decode("utf-8")

        url_key = "count:" + url
        html_content = fn(url)
        r.incr(url_key)
        r.setex(key, EXPIRATION_TIME, html_content)

        return html_content

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """Obtain the html content of a particular URL
    and returns it"""

    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    print(get_page(url))
