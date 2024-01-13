import React from 'react';
import ScrapeButtons from './ScrapeButtons';
import SearchComponent from "./SearchComponent";
const App = () => {
  return (
    <div>
      <h1>Aplikacja do zarządzania nieruchomościami</h1>
      <ScrapeButtons />
        <SearchComponent />
    </div>
  );
};

export default App;
