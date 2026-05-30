# Część 1 – Python
Zainstalowano Python 3.10+ oraz wymagane biblioteki.
Uruchomiono JupyterLab i zweryfikowano działanie bibliotek pandas, numpy i sklearn.

# Część 2 – Git
Utworzono repozytorium GitHub oraz wykonano pierwszy commit.

# Część 3 – Docker
Zainstalowano Docker Desktop.
Zweryfikowano działanie komend:
- docker --version
- docker compose version
- docker run hello-world

# Część 4 – Środowisko kursu
Uruchomiono środowisko za pomocą docker compose.

## Kafka
Polecenie z instrukcji nie działało bezpośrednio, ponieważ ścieżka była inna.
Poprawna komenda:

/usr/local/kafka_2.12-3.7.1/bin/kafka-topics.sh --list --bootstrap-server broker:9092

Kafka działa poprawnie (lista topiców pusta).
