# Używamy oficjalnego obrazu Node 18
FROM node:18

# Ustawiamy katalog roboczy na /Projekt_ZP/Frontend
WORKDIR /Projekt_ZP/Frontend

# Kopiujemy pliki z katalogu projektu do katalogu roboczego
COPY . .

# Usuwamy katalog real_estate_app
RUN rm -rf real_estate_app

# Tworzymy nowy projekt React
RUN npx create-react-app my-react-app

# Przechodzimy do katalogu my-react-app
WORKDIR /Projekt_ZP/Frontend/my-react-app

# Usuwamy domyślne pliki
RUN rm -rf src public .gitignore package.json package-lock.json README.md

# Kopiujemy pliki z projektu do katalogu roboczego
COPY ./real_estate_app .

# Instalujemy niezbędne zależności
RUN npm install axios

# Expose port 3000
EXPOSE 3000

# Uruchamiamy aplikację
CMD ["npm", "start"]
