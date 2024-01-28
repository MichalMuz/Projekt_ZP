import React, { useState } from 'react';
import styled from 'styled-components';

const Button = styled.button`
  background-color: #3498db;
  color: #ffffff;
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 5px;
  &:disabled {
    background-color: #bdc3c7;
    cursor: not-allowed;
  }
`;

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
      <Button onClick={() => handleScrape('http://127.0.0.1:8000/ogloszenia_domow', 'last_retrieval_time_scrape.txt')} disabled={isFetching}>
        Pobierz oferty domów
      </Button>
      <Button onClick={() => handleScrape('http://127.0.0.1:8000/ogloszenia_mieszkan', 'last_retrieval_time_scrape2.txt')} disabled={isFetching}>
        Pobierz oferty mieszkań
      </Button>
      <Button onClick={() => handleScrape('http://127.0.0.1:8000/ogloszenia_kawalerek', 'last_retrieval_time_scrape3.txt')} disabled={isFetching}>
        Pobierz oferty kawalerek
      </Button>
    </div>
  );
};

export default ScrapeButtons;