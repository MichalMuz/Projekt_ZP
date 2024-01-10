from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from web_scraping import get_listing_links_async, DiskCache
from tqdm import tqdm
import uvicorn
from datetime import datetime
import os

app = FastAPI()

last_retrieval_files = {
    "ogloszenia_domow": "data_ostatniego_pobierania_domow.txt",
    "ogloszenia_mieszkan": "data_ostatniego_pobierania_mieszkan.txt",
    "ogloszenia_kawalerek": "data_ostatniego_pobierania_kawalerek.txt",
}


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
        'https://www.otodom.pl/pl/wyniki/sprzedaz/dom/cala-polska', background_tasks, last_retrieval_files["ogloszenia_domow"]
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005, reload=True)
