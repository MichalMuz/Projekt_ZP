import aiohttp
from aiohttp.client_exceptions import ClientResponseError
from bs4 import BeautifulSoup

class AsyncWebScraper:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers or {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }