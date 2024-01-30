import React from 'react';
import ScrapeButtons from './ScrapeButtons';
import SearchComponent from './SearchComponent';
import AppHeader from './AppHeader';
import './App.css';

const App = () => {
  return (
    <div className="container">
      <h1>Aplikacja Wyszukiwania Nieruchomości</h1>
      <AppHeader appName="Aplikacja" />

      <ScrapeButtons />
      <SearchComponent />
    </div>
  );
};

export default App;
