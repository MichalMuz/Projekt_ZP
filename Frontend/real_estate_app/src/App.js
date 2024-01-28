import React from 'react';
import styled from 'styled-components';
import ScrapeButtons from './ScrapeButtons';

const AppWrapper = styled.div`
  font-family: 'Arial', sans-serif;
  background-color: #f4f4f4;
  padding: 20px;
  text-align: center;
`;

const AppHeader = styled.h1`
  color: #3498db;
  margin-bottom: 20px;
`;

const App = () => {
  return (
    <AppWrapper>
      <AppHeader>Aplikacja do zarządzania nieruchomościami</AppHeader>
      <ScrapeButtons />
    </AppWrapper>
  );
};

export default App;
