import asyncio
import json
import os
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import spacy
from geopy.geocoders import Nominatim
import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from tqdm import tqdm
from web_scraping import get_listing_links_async, DiskCache

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

last_retrieval_files = {
    "ogloszenia_domow": "data_ostatniego_pobierania_domow.txt",
    "ogloszenia_mieszkan": "data_ostatniego_pobierania_mieszkan.txt",
    "ogloszenia_kawalerek": "data_ostatniego_pobierania_kawalerek.txt",
}

try:
    nlp = spacy.load("pl_core_news_sm")
except OSError:
    async def load_spacy_model():
        spacy.cli.download("pl_core_news_sm")
        return spacy.load("pl_core_news_sm")


    nlp = asyncio.run(load_spacy_model())

geolocator = Nominatim(user_agent="your_app_name")


class DataStore:
    def __init__(self, all_json_data):
        self.all_json_data = all_json_data


def read_last_retrieval_time(last_retrieval_file):
    last_retrieval_time = None

    if os.path.exists(last_retrieval_file):
        with open(last_retrieval_file, "r") as file:
            last_retrieval_time = file.read()

    return last_retrieval_time


def save_current_retrieval_time(last_retrieval_file):
    current_retrieval_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(last_retrieval_file, "w") as last_data_download_date:
        last_data_download_date.write(current_retrieval_time)


def clean_invalid_json_records(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        data = ''.join(char for char in data if (ord(char) > 31 or ord(char) == 9) and char != '\x0b')

        cleaned_data = json.loads(data)

        cleaned_data = [record for record in cleaned_data if
                        isinstance(record, dict) and 'title' in record and 'description' in record]

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(cleaned_data, file, ensure_ascii=False, indent=2)

        return cleaned_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {file_path}: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


async def load_and_clean_json_file_async(json_file):
    return clean_invalid_json_records(json_file)


async def get_all_json_data():
    json_files = ["wyniki_sprzedaz_dom_cala-polska.json", "wyniki_sprzedaz_kawalerka_cala-polska.json",
                  "wyniki_sprzedaz_mieszkanie_cala-polska.json"]

    cleaned_data = await asyncio.gather(*(load_and_clean_json_file_async(json_file) for json_file in json_files))

    all_json_data = []
    for records in cleaned_data:
        if records:
            all_json_data.extend(records)

    return all_json_data


async def scrape_otodom_logic(url, last_retrieval_file, background_tasks):
    return await common_scrape_logic(url, last_retrieval_file, background_tasks)


@app.get("/ogloszenia_domow")
async def scrape_otodom_domow(background_tasks: BackgroundTasks):
    url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/dom/cala-polska'
    return await scrape_otodom_logic(url, last_retrieval_files["ogloszenia_domow"], background_tasks)


@app.get("/ogloszenia_mieszkan")
async def scrape_otodom_mieszkan(background_tasks: BackgroundTasks):
    url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska'
    return await scrape_otodom_logic(url, last_retrieval_files["ogloszenia_mieszkan"], background_tasks)


@app.get("/ogloszenia_kawalerek")
async def scrape_otodom_kawalerek(background_tasks: BackgroundTasks):
    url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/kawalerka/cala-polska'
    return await scrape_otodom_logic(url, last_retrieval_files["ogloszenia_kawalerek"], background_tasks)


@app.get("/search")
async def search(query: str):
    print(f"Received search query: {query}")

    all_json_data = await get_all_json_data()

    if not all_json_data:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    json_data_for_comparison = [data for data in all_json_data if data is not None]

    # Determine the type of property (dom, mieszkanie, kawalerka) based on the query
    property_type = None
    if any(word in query.lower() for word in ["dom", "domu", "domem", "domach"]):
        property_type = "dom"
    elif any(word in query.lower() for word in ["mieszkanie", "mieszkania", "mieszkaniem", "mieszkaniach"]):
        property_type = "mieszkanie"
    elif any(word in query.lower() for word in ["kawalerka", "kawalerki", "kawalerką", "kawalerkach"]):
        property_type = "kawalerka"

    if property_type:
        filtered_json_data = [data for data in json_data_for_comparison if
                              property_type in data.get("title", "").lower()]
    else:
        filtered_json_data = json_data_for_comparison

    results = compare_query_to_json(query, filtered_json_data)
    print(f"Returning search results: {results}")
    return JSONResponse(content={"results": results})


def extract_city_from_location(location):
    try:
        # Use geopy to extract location details
        location_info = geolocator.geocode(location, language='pl', addressdetails=True)

        if location_info and location_info.raw.get("address"):
            address_details = location_info.raw["address"]

            city_keys = ["city", "town", "village", "county", "state_district"]

            city = next((address_details[key] for key in city_keys if key in address_details and address_details[key]),
                        None)

            if not city:
                city = address_details.get("municipality") or address_details.get("state")
            return city
        else:
            return None
    except Exception as e:
        print(f"Error extracting city from location: {e}")
        return None


def compare_query_to_json(query, json_data):
    query_tokens = set(token.text.lower() for token in nlp(query))

    matches = []
    for offer in json_data:
        title_tokens = set(token.text.lower() for token in nlp(offer["title"]))
        description_tokens = set(token.text.lower() for token in nlp(offer["description"]))
        location_tokens = set(token.text.lower() for token in nlp(offer.get("offer_location", "")))

        offer_city = extract_city_from_location(offer.get("offer_location", ""))
        print(f"Offer City: {offer_city}")

        # Use a Jaccard similarity threshold for partial matching
        title_similarity = len(query_tokens.intersection(title_tokens)) / len(query_tokens.union(title_tokens))
        description_similarity = len(query_tokens.intersection(description_tokens)) / len(
            query_tokens.union(description_tokens))
        location_similarity = len(query_tokens.intersection(location_tokens)) / len(query_tokens.union(location_tokens))

        if offer_city:
            offer_city_tokens = set(token.text.lower() for token in nlp(offer_city))
            location_similarity_with_city = len(query_tokens.intersection(offer_city_tokens)) / len(
                query_tokens.union(offer_city_tokens))
            location_similarity = max(location_similarity, location_similarity_with_city)

        similarity_threshold = 0.4

        if title_similarity > similarity_threshold or description_similarity > similarity_threshold or location_similarity > similarity_threshold:
            matches.append((max(title_similarity, description_similarity, location_similarity), offer))

    sorted_matches = sorted(matches, key=lambda x: x[0], reverse=True)
    top_matches = sorted_matches[:5]

    results = [{"title": offer["title"], "description": offer["description"]} for _, offer in top_matches]

    return results


async def common_scrape_logic(start_url, last_retrieval_file, background_tasks):
    last_retrieval_time = read_last_retrieval_time(last_retrieval_file)
    cache_expiration_time = 2592000

    progress_bar = tqdm(total=1, desc="Downloading the number of pages", position=0, dynamic_ncols=True)

    async def task_wrapper():
        await get_listing_links_async(
            start_url,
            DiskCache(expiration_time=cache_expiration_time),
            progress_bar.update
        )

    background_tasks.add_task(task_wrapper)

    current_retrieval_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_current_retrieval_time(last_retrieval_file)

    while progress_bar.n < progress_bar.total:
        await asyncio.sleep(1)

    progress_bar.close()

    print(f"Web scraping completed. Time: {current_retrieval_time}")

    response_content = {
        "message": f"Web scraping started for {start_url}",
        "last_retrieval_time": last_retrieval_time or "Not available",
        "current_retrieval_time": current_retrieval_time
    }

    return JSONResponse(content=response_content)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005, reload=True)
