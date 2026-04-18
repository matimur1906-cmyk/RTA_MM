# Analiza danych w czasie rzeczywistym

Repozytorium zawiera wykonanie zadań z kursu RTA.

## Zakres:
- Python (środowisko + Jupyter)
- Git (repozytorium)
- Docker (środowisko)
- Kafka (test działania)

## Uruchomienie środowiska
1. Uruchomić Docker Desktop
2. Przejść do katalogu `jupyterlab-project`
3. Wykonać:
   `docker compose up -d`
4. Otworzyć JupyterLab pod adresem:
   `http://localhost:8999`

## Zawartość repozytorium
- `producer.py` – producent danych transakcyjnych
- `consumer_filter.py` – filtr transakcji powyżej 1000 PLN
- `consumer_count.py` – agregacja transakcji per sklep
- `scoring_consumer.py` – scoring transakcji i wysyłanie alertów do topicu `alerts`
- `Lab1.ipynb` – notebook z zajęć
- `zadania.md` – opis wykonanych zadań
