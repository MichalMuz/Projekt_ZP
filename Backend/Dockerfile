# Używamy obrazu Python 3.12
FROM python:3.12

# Ustawiamy katalog roboczy na /Projekt_ZP/Backend
WORKDIR /Projekt_ZP/Backend

# Kopiujemy pliki requirements.txt do katalogu roboczego
COPY ./requirements.txt .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę plików do katalogu roboczego
COPY . .

# Pobieramy model SpaCy
RUN python -m spacy download pl_core_news_sm

# Expose port 8005
EXPOSE 8005

# Uruchamiamy backend
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8005"]
