#   Aplikacja do Wyszukiwania Nieruchomości

To jest prosta aplikacja internetowa oparta na bibliotece React, służąca do wyszukiwania ofert nieruchomości oraz do pobierania danych z określonych punktów końcowych. Aplikacja składa się z trzech głównych komponentów: `ScrapeButtons`, `SearchComponent` oraz głównego komponentu `App`.


### Komponent ScrapeButtons

Komponent `ScrapeButtons` dostarcza przyciski do pobierania danych dotyczących nieruchomości z różnych kategorii. Wykorzystuje zarządzanie stanem w React do obsługi procesu pobierania danych, a przyciski są dezaktywowane podczas trwania tego procesu. Pobrane dane są logowane do konsoli.

### Komponent SearchComponent

Komponent `SearchComponent` umożliwia użytkownikom wyszukiwanie ofert nieruchomości. Komunikuje się z serwerem backendowym za pomocą biblioteki Axios do asynchronicznych żądań. Wyniki są wyświetlane dynamicznie, a doświadczenie użytkownika poprawia animowany spinner podczas ładowania danych.

### Komponent App

Główny komponent `App` pełni rolę punktu wejścia do aplikacji. Zawiera nagłówek aplikacji, komponent `ScrapeButtons` oraz komponent `SearchComponent`.

##### Jak Uruchomić Aplikację?

1.  Sklonuj repozytorium na swój lokalny komputer.
2.  Stwórz projekt w folderze Frontend np. `npx create-react-app my-react-app`
3. Podmień folder src pobrany z repozytorium z tym wygenerowanym 
4.  Zainstaluj niezbędne zależności przy użyciu `npm install` {axios}.
5.  Uruchom aplikację przy użyciu `npm start`.
6.  Otwórz przeglądarkę i przejdź pod adres `http://localhost:3000`, aby zobaczyć aplikację.