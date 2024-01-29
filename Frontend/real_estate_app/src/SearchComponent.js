import React, { useState } from "react";
import axios from "axios";
import "./SearchComponent.css";

const SearchComponent = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [noResults, setNoResults] = useState(false);

  const handleSearch = async () => {
    try {
      setLoading(true);
      setNoResults(false);

      const response = await axios.get(
        `http://127.0.0.1:8005/search?query=${encodeURIComponent(query)}`
      );
      setResults(response.data.results);

      if (response.data.results.length === 0) {
        setNoResults(true);
      }
    } catch (error) {
      console.error("Error:", error.message);
    } finally {
      setLoading(false);
    }
  };

return (
  <div className="search-section">
    <input
      type="text"
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Wyszukaj..."
      className="search-input"
    />
    <button className="search-button" onClick={handleSearch}>
      Wyszukaj
    </button>

    {loading && <div className="loading-spinner"></div>}

    {noResults && !loading && <p className="no-results">Brak wyników.</p>}

    <ul className="results-list">
      {results.map((result, index) => (
  <li key={index} className="result-item">
    <div>
      <strong className="result-title">Tytuł oferty:</strong> {result.title}
      <br />
      <strong className="result-description">Opis:</strong>
      <div className="description">{result.description}</div>
      <br />
      <strong className="result-link-url">Link do oferty:</strong> <a href={result.link} target="_blank" rel="noopener noreferrer">{result.link}</a>
    </div>
  </li>
))}


    </ul>
  </div>
);
};

export default SearchComponent;
