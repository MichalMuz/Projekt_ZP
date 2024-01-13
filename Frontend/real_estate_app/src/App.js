import React from 'react';
import ScrapeButtons from './ScrapeButtons';
import SearchComponent from "./SearchComponent";
import AppHeader from './AppHeader';

const App = () => {
  return (
    <div>
      <h1> Wybierz rodzaj nieruchomości</h1>
      <AppHeader appName="Aplikacja" />


      <ScrapeButtons />
        <SearchComponent />
    </div>
  );
};

export default App;
