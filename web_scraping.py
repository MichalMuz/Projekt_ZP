import aiohttp
from aiohttp.client_exceptions import ClientResponseError
import asyncio
from bs4 import BeautifulSoup
import diskcache
from tqdm import tqdm
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

    async def fetch_with_retry(self, session, url, headers, timeout=100000, retries=3):
        for _ in range(retries):
            try:
                async with session.get(url, headers=headers, timeout=timeout) as response:

                    return await response.text()
            except aiohttp.ClientConnectionError as e:
                print(f"Błąd połączenia: {e}")
                await asyncio.sleep(2)
            except asyncio.TimeoutError:
                print(f'Błąd czasu oczekiwania podczas pobierania {url}. Ponawianie próby...')

        return None
    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, "lxml")
        return soup

async def fetch_and_parse(session, url, cache, pbar=None):
    html_content = cache.get(url)

    if html_content is None:
        while html_content is None:
            html_content = await AsyncWebScraper(url).fetch_with_retry(session, url, AsyncWebScraper(url).headers)
            cache.set(url, html_content)

    if pbar:
        pbar.update(1)
    return AsyncWebScraper(url).parse_html(html_content)
async def get_number_of_pages(session, start_url, cache, pbar=None):
    html_content = await fetch_and_parse(session, start_url, cache, pbar)
    if html_content:
        last_page_links = html_content.find_all('a', {'class': 'eo9qioj1 css-pn5qf0 edo3iif1'})
        if last_page_links:
            last_page_number = int(last_page_links[-1]['href'].split('=')[-1])
            if pbar:
                pbar.set_postfix(pages=last_page_number)  # Display total pages in postfix
            print('Number of pages to be analyzed:', last_page_number)
            return last_page_number
    return 0
async def get_listing_links_async(start_url, cache, pbar_total):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000)) as session:
        async with asyncio.Semaphore(500):  # Limit concurrent requests to 500
            num_pages_to_scrape = await get_number_of_pages(session, start_url, cache, pbar_total)

            if num_pages_to_scrape > 0:
                all_links = []
                tasks = [fetch_and_parse(session,
                                         f'{start_url}?ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing&page={page_num}/',
                                         cache, pbar_total)
                         for page_num in range(1, num_pages_to_scrape + 1)]

                with tqdm(total=num_pages_to_scrape, desc="Fetching pages", position=1,
                          unit=' page') as pbar_fetch_pages:
                    soup_list = await asyncio.gather(*tasks)
                    for soup in soup_list:
                        if soup:
                            page_links = get_listing_links(soup)
                            all_links.extend(page_links)
                            pbar_fetch_pages.update(1)


                print('Number of offers found:', len(all_links))
                return all_links
            else:
                print("Error: Unable to determine the number of pages.")
                return []
def get_listing_links(soup):
        home_elements = soup.findAll('li', attrs={'class': 'css-o9b79t e1dfeild0'})
        links = []

        for info in home_elements[3:]:  # Skip the first three elements
            link_element = info.find('a', class_='css-lsw81o e1dfeild2')
            if link_element:
                link = link_element.get('href')
                full_link = 'https://www.otodom.pl' + link
                links.append(full_link)

        return links
class DiskCache:
    def __init__(self, cache_directory='./cache', expiration_time=86400):
        self.cache_directory = cache_directory
        self.expiration_time = expiration_time
        self.cache = diskcache.Cache(self.cache_directory, expire=self.expiration_time)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache.set(key, value)