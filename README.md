# RTA_MM

Repozytorium zawiera rozwiązania z laboratoriów RTA dotyczących przetwarzania strumieniowego, Apache Kafka oraz prostego systemu scoringu transakcji z wykorzystaniem modeli ML.

## Zawartość repozytorium

### Lab 1 — Kafka basics

Pierwsza część ćwiczeń dotyczy podstaw pracy z Apache Kafka.

Zakres:

* uruchamianie producenta wiadomości,
* konsumowanie wiadomości z topicu Kafka,
* filtrowanie strumienia transakcji,
* zliczanie wiadomości,
* podstawowy scoring w czasie rzeczywistym.

Przykładowe pliki:

* `producer.py`
* `consumer_count.py`
* `consumer_filter.py`
* `scoring_consumer.py`
* `Lab1.ipynb`
* `zadania.md`

---

### Lab 2 — Fraud Detection API + Kafka Consumer

Druga część ćwiczeń rozwija pipeline o model uczenia maszynowego oraz API.

Zakres:

* przygotowanie danych syntetycznych,
* trenowanie modelu Random Forest,
* zapis modelu do pliku `.pkl`,
* utworzenie API we FastAPI,
* endpoint `POST /score`,
* integracja API z konsumentem Kafka,
* wysyłanie alertów dla podejrzanych transakcji.

Główne elementy:

* `fraud_api.py` — API scoringowe,
* `ml_consumer.py` — konsument Kafka korzystający z API,
* `producer.py` — producent transakcji,
* `fraud_model.pkl` — zapisany model Random Forest.

---

### Lab 3 — Random Forest vs Isolation Forest

Trzecia część ćwiczeń porównuje podejście nadzorowane i nienadzorowane do wykrywania fraudów.

Zakres:

* ograniczenia Random Forest w przypadku nowych typów fraudów,
* trenowanie modelu Isolation Forest tylko na normalnych transakcjach,
* porównanie RF i IF,
* endpoint `GET /model-info`,
* równoległe uruchomienie dwóch API i dwóch consumerów,
* porównanie alertów generowanych przez modele.

Główne elementy:

* `fraud_api_if.py` — API z modelem Isolation Forest,
* `fraud_api_rf.py` — API z modelem Random Forest,
* `ml_consumer_if.py` — consumer korzystający z Isolation Forest,
* `ml_consumer_rf.py` — consumer korzystający z Random Forest,
* `fraud_model_if.pkl` — zapisany model Isolation Forest,
* `fraud_model.pkl` — zapisany model Random Forest.

---

## Architektura rozwiązania

Pipeline działa według schematu:

```text
producer.py
   ↓
Kafka topic: transactions
   ↓
ml_consumer.py
   ↓
FastAPI /score
   ↓
Kafka topic: alerts / logi alertów
```

W Lab 3 pipeline został rozszerzony o równoległe porównanie dwóch modeli:

```text
Kafka transactions
   ↓
ml_consumer_if.py → fraud_api_if.py → Isolation Forest
   ↓
ml_consumer_rf.py → fraud_api_rf.py → Random Forest
```

Dzięki różnym `group_id` oba konsumery mogą otrzymywać te same wiadomości z topicu `transactions`, co pozwala porównać alerty generowane przez oba modele.

---

## Endpointy API

### `POST /score`

Endpoint przyjmuje dane transakcji i zwraca ocenę modelu.

Przykładowy request:

```json
{
  "amount": 150,
  "is_electronics": 0,
  "tx_per_minute": 3
}
```

Przykładowa odpowiedź:

```json
{
  "is_fraud": false,
  "fraud_probability": 0.288,
  "model": "isolation_forest"
}
```

### `GET /health`

Sprawdza, czy API działa.

Przykładowa odpowiedź:

```json
{
  "status": "ok"
}
```

### `GET /model-info`

Zwraca informacje o aktualnym modelu.

Przykład dla Isolation Forest:

```json
{
  "type": "isolation_forest",
  "n_estimators": 100,
  "contamination": 0.05
}
```

Przykład dla Random Forest:

```json
{
  "type": "random_forest",
  "n_estimators": 100
}
```

---

## Uruchomienie

### 1. Uruchom środowisko Docker

```bash
docker compose up
```

lub w tle:

```bash
docker compose up -d
```

### 2. Uruchom API Isolation Forest

```bash
cd lab3
uvicorn fraud_api_if:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Uruchom API Random Forest

W drugim terminalu:

```bash
cd lab3
uvicorn fraud_api_rf:app --host 0.0.0.0 --port 8002 --reload
```

### 4. Uruchom konsumery

Consumer dla Isolation Forest:

```bash
cd lab3
python ml_consumer_if.py
```

Consumer dla Random Forest:

```bash
cd lab3
python ml_consumer_rf.py
```

### 5. Uruchom producenta transakcji

```bash
cd lab3
python producer.py
```

---

## Wnioski

Random Forest jest modelem nadzorowanym i dobrze wykrywa transakcje podobne do fraudów widzianych podczas treningu. Jego ograniczeniem jest zależność od etykiet historycznych.

Isolation Forest jest modelem nienadzorowanym. Uczy się wzorca normalnych transakcji i wykrywa obserwacje odbiegające od normy. Dzięki temu może być przydatny w sytuacji, gdy pojawiają się nowe, wcześniej nieznane typy fraudów.

Parametr `contamination` wpływa na liczbę alertów:

* niższa wartość, np. `0.01`, oznacza mniej alertów i bardziej konserwatywny model,
* wyższa wartość, np. `0.10`, oznacza więcej alertów, ale również większe ryzyko false positives.
