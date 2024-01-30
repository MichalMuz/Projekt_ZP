# Projekt Aplikacja Nieruchomości

![Aplikacja Nieruchomości](Photos of the application/zdjecie_aplikacji.gif)
## Wstęp

>Aplikacja ta, to narzędzie do przeszukiwania 
>ofert nieruchomości w Polsce.

Ten projekt łączy w sobie zarówno backend, jak i frontend, 
tworząc aplikację do przeszukiwania danych dotyczących nieruchomości. Backend jest napisany w języku Python, wykorzystuje takie technologie jak `fastapi`, `spaCY`,`geopy`,`sklearn`  i wiele innnych. 
Natomiast Frontend jest zbudowany przy użyciu React z wykorzystanie `axios`.

## Funkcje

-   **Web Scraping:** Aplikacja pobiera najnowsze oferty dotyczące domów, mieszkań i kawalerek z otodom.pl, zapisując datę ostatniego pobrania dla każdej kategorii, generuje odpowiedni pliki json i csv oraz używa Cache'owania do optymalizacji zapytań.
    
-   **Wyszukiwanie:** Użytkownicy mogą przeszukiwać oferty, wprowadzając zapytanie. Aplikacja porównuje zapytanie z dostępnymi ofertami, uwzględniając tytuł, opis i lokalizację.

## Wyszukiwanie Ofert

-   Przejdź do sekcji wyszukiwania, wprowadź zapytanie, a następnie naciśnij przycisk "Szukaj".
-   Aplikacja zwróci oferty pasujące do zadanego zapytania.

**Ciesz się korzystaniem z 
Aplikacji do Przeszukiwania Ofert Nieruchomości! 🏡✨**

## Struktura Projektu

    D:\Projekt_ZP 
    │ 
    ├── Backend 
    │ ├── main.py 
    │ ├── requirements.txt 
    │ └── web_scraping.py 
    │ 
    ├── Frontend 
    │ ├── real_estate_app 
    │ ├── node_modules 
    │ ├── public 
    │ ├── src 
    │ ├── .gitignore 
    │ ├── package.json 
    │ ├── package-lock.json 
    │ └── README.md 
    │ 
    └── .gitignore

### Backend  
##### main.py Ten plik zawiera główny punkt wejścia dla backendu. 
#####  requirements.txt Lista zależności Pythona potrzebnych do uruchomienia backendu.  
#####  web_scraping.py Skrypt napisany w Pythonie do asynchronicznego web scrapingu, wykorzystujący `aiohttp`, `asyncio` i inne biblioteki. 
###  Frontend  
#####  real_estate_app Ten katalog zawiera kod aplikacji napisanej w React. 
#####  node_modules Folder zależności Node.js. Generuje się po zainstalowaniu wymaganych pakietów za pomocą `npm install`. 
#####  public Zasoby statyczne i plik HTML będący punktem wejścia dla aplikacji React. 
#####  src Kod źródłowy aplikacji React. 
#####  .gitignore Plik konfiguracyjny dla Git, określający, które pliki i katalogi powinny być ignorowane. 
#####  package.json Plik konfiguracyjny Node.js z metadanymi i zależnościami. 
#####  package-lock.json Zapisuje dokładną wersję każdej zainstalowanej paczki w celu lepszej spójności w różnych środowiskach. 
#####  README.md Ten plik zawiera  dokumentację na temat konfiguracji i uruchamiania aplikacji frontendowej. 
#### .gitignore Globalny plik konfiguracyjny dla Git, określający pliki i katalogi, które Git powinien ignorować.


## Jak Zacząć

1.  **Konfiguracja Backendu:**
    
    -   Przejdź do katalogu `Backend`.
    -   Zainstaluj zależności: `pip install -r requirements.txt`.
    -   Uruchom backend: `uvicorn main:app --reload --port 8005`.
2.  **Konfiguracja Frontendu:**
    
    -   Przejdź do katalogu `Frontend`.
    - Przeczytaj instrukcje pliku `README.md` dotyczącą instalacji

3.  **Dostęp do Aplikacji:**

> W terminalu aplikacji :

a) w folderze Backend `uvicorn main:app --reload --port 8005`
b) w folderze Frontend `npm strart`

> Otwórz przeglądarkę internetową i przejdź pod podany adres URL 
> lub  port aplikacji
