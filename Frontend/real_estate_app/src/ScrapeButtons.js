import React, { useState } from 'react';

const ScrapeButtons = () => {
  const [isFetching, setIsFetching] = useState(false);

const handleScrape = async (url) => {
  try {
    setIsFetching(true);
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    setIsFetching(false);
  } catch (error) {
    console.error('Error fetching data:', error);
    setIsFetching(false);
  }
};

  return (
    <div>
      <button onClick={() => handleScrape('http://127.0.0.1:8000/ogloszenia_domow', 'last_retrieval_time_scrape.txt')} disabled={isFetching}>
        Pobierz oferty domów
      </button>
      <button onClick={() => handleScrape('http://127.0.0.1:8000/ogloszenia_mieszkan', 'last_retrieval_time_scrape2.txt')} disabled={isFetching}>
        Pobierz oferty mieszkań
      </button>
      <button onClick={() => handleScrape('http://127.0.0.1:8000/ogloszenia_kawalerek', 'last_retrieval_time_scrape3.txt')} disabled={isFetching}>
        Pobierz oferty kawalerek
      </button>
    </div>
  );
};

export default ScrapeButtons;
