// ScrapeButtons.js

import React, { useState } from 'react';
import './ScrapeButtons.css';

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
    <div className={'scrape_section'}>
      <button className="dom" onClick={() => handleScrape('http://127.0.0.1:8005/ogloszenia_domow', 'last_retrieval_time_scrape.txt')} disabled={isFetching}>
        Dom
      </button>
      <button className="mieszkanie" onClick={() => handleScrape('http://127.0.0.1:8005/ogloszenia_mieszkan', 'last_retrieval_time_scrape2.txt')} disabled={isFetching}>
        Mieszkanie
      </button>
      <button className="kawalerka" onClick={() => handleScrape('http://127.0.0.1:8005/ogloszenia_kawalerek', 'last_retrieval_time_scrape3.txt')} disabled={isFetching}>
        Kawalerka
      </button>
    </div>
  );
};

export default ScrapeButtons;
