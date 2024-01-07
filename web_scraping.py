import aiohttp
from aiohttp.client_exceptions import ClientResponseError
from bs4 import BeautifulSoup

class AsyncWebScraper:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers or {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    async def fetch_page(self, session):
        for attempt in range(3):
            try:
                async with session.get(self.url, headers=self.headers, timeout=100000) as response:
                    response.raise_for_status()
                    return await response.text()
            except ClientResponseError as e:
                print(f'Error during download {self.url}: {e}. Re-attempting ... Attempt {attempt + 1}')
            except aiohttp.ClientConnectionError as e:
                print(f"Error during download {e}")

        print(f'Failed to download {self.url} after multiple attempts.')
        return None