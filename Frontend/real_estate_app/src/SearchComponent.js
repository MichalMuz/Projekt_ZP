import React, { useState } from "react";
import axios from "axios";

const SearchComponent = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

const handleSearch = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8005/search?query=${encodeURIComponent(query)}`);
    setResults(response.data.results);
  } catch (error) {
    if (error.response) {
      // The request was made, but the server responded with an error status code
      console.error("Server responded with an error:", error.response.status, error.response.data);
    } else if (error.request) {
      // The request was made, but no response was received
      console.error("No response received from the server");
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error("Error setting up the request:", error.message);
    }
  }
};

  return (
    <div>
      <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
      <button onClick={handleSearch}>Search</button>
      <ul>
        {results.map((result, index) => (
          <li key={index}>
            <strong>Title:</strong> {result.title}, <strong>Description:</strong> {result.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SearchComponent;
