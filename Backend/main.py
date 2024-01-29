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


async def common_scrape_logic(start_url, background_tasks: BackgroundTasks, last_retrieval_file):
    last_retrieval_time = None

    # Read the last retrieval time from the file if available
    if os.path.exists(last_retrieval_file):
        with open(last_retrieval_file, "r") as file:
            last_retrieval_time = file.read()

    cache_expiration_time = 2592000  # 30 days in seconds

    background_tasks.add_task(
        get_listing_links_async,
        start_url,
        DiskCache(expiration_time=cache_expiration_time),
        tqdm(total=1, desc="Downloading the number of pages", position=0)
    )

    current_retrieval_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save the current retrieval time to the last_data_download_date
    with open(last_retrieval_file, "w") as last_data_download_date:
        last_data_download_date.write(current_retrieval_time)

    response_content = {
        "message": f"Web scraping started for {start_url}",
        "last_retrieval_time": last_retrieval_time or "Not available",
        "current_retrieval_time": current_retrieval_time
    }

    return JSONResponse(content=response_content)


@app.get("/ogloszenia_domow")
async def scrape_otodom(background_tasks: BackgroundTasks):
    return await common_scrape_logic(
        'https://www.otodom.pl/pl/wyniki/sprzedaz/dom/cala-polska', background_tasks,
        last_retrieval_files["ogloszenia_domow"]
    )


@app.get("/ogloszenia_mieszkan")
async def scrape_another_endpoint(background_tasks: BackgroundTasks):
    return await common_scrape_logic(
        'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska', background_tasks,
        last_retrieval_files["ogloszenia_mieszkan"]
    )


@app.get("/ogloszenia_kawalerek")
async def scrape_third_endpoint(background_tasks: BackgroundTasks):
    return await common_scrape_logic(
        'https://www.otodom.pl/pl/wyniki/sprzedaz/kawalerka/cala-polska', background_tasks,
        last_retrieval_files["ogloszenia_kawalerek"]
    )


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

            # Prioritize city information from the address
            city_keys = ["city", "town", "village", "county", "state_district"]
            city = next((address_details[key] for key in city_keys if key in address_details and address_details[key]),
                        None)

            # If no city information is found, fall back to other options
            if not city:
                city = address_details.get("municipality") or address_details.get("state")

            return city
        else:
            return None
    except Exception as e:
        print(f"Error extracting city from location: {e}")
        return None


def calculate_similarity(query_tokens, text_tokens):
    return len(query_tokens.intersection(text_tokens)) / len(query_tokens.union(text_tokens))


def compare_query_to_json(query, json_data):
    query_tokens = set(token.text.lower() for token in nlp(query))
    unique_links = set()

    matches = []

    for offer in json_data:
        title_tokens = set(token.text.lower() for token in nlp(offer["title"]))
        description_tokens = set(token.text.lower() for token in nlp(offer["description"]))
        location_tokens = set(token.text.lower() for token in nlp(offer.get("offer_location", "")))

        offer_city = extract_city_from_location(offer.get("offer_location", ""))

        # Calculate title similarity
        title_similarity = calculate_similarity(query_tokens, title_tokens)

        # Calculate description similarity
        description_similarity = calculate_similarity(query_tokens, description_tokens)

        # Include street address in location_tokens
        street_address_tokens = set(token.text.lower() for token in nlp(offer.get("offer_location", "")))

        # Combine location_tokens and street_address_tokens
        combined_location_tokens = location_tokens.union(street_address_tokens)

        # Recalculate location_similarity with combined_location_tokens
        location_similarity = calculate_similarity(query_tokens, combined_location_tokens)

        print(f"Query Tokens: {query_tokens}")
        print(f"Title Tokens: {title_tokens}")
        print(f"Description Tokens: {description_tokens}")
        print(f"Location Tokens: {location_tokens}")
        print(f"Offer City: {offer_city}")

        if offer_city:
            offer_city_tokens = set(token.text.lower() for token in nlp(offer_city))
            location_similarity_with_city = calculate_similarity(query_tokens, offer_city_tokens)
            location_similarity = max(location_similarity, location_similarity_with_city)

        # Calculate overall similarity considering title, description, and location
        overall_similarity = max(title_similarity, description_similarity, location_similarity)

        similarity_threshold = 0.4

        # Use overall_similarity directly in the decision
        if overall_similarity > similarity_threshold and offer["link"] not in unique_links:
            unique_links.add(offer["link"])
            matches.append({
                "title": offer["title"],
                "description": offer["description"],
                "link": offer["link"]
            })

    return matches


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005, reload=True)
