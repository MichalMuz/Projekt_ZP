from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from web_scraping import get_listing_links_async, DiskCache
from tqdm import tqdm
import uvicorn
from datetime import datetime
import os


app = FastAPI()

last_retrieval_file = "last_retrieval_time.txt"

# Read the last retrieval time from the file if available
if os.path.exists(last_retrieval_file):
    with open(last_retrieval_file, "r") as file:
        last_retrieval_time = file.read()
else:
    last_retrieval_time = None


@app.get("/scrape")
async def scrape_otodom(background_tasks: BackgroundTasks):
    global last_retrieval_time

    last_retrieval_time = last_retrieval_time or "Not available"

    # Set your desired start URL and cache expiration time
    start_url = 'https://www.otodom.pl/pl/wyniki/wynajem/dom/cala-polska'
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
        "message": "Web scraping started",
        "last_retrieval_time": last_retrieval_time,
        "current_retrieval_time": current_retrieval_time
    }

    return JSONResponse(content=response_content)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005, reload=True)
