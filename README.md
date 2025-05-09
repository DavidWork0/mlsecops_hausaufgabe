# MLSecOps Projekt 

[![Python 3.12.8](https://img.shields.io/badge/python-3.12.8-blue.svg)](https://www.python.org/downloads/release/python-3128/)
[![Docker](https://img.shields.io/badge/docker-supported-brightgreen.svg)](https://www.docker.com/)

Gépi tanulási projekt, amely tartalmazza az alábbi komponenseket:
- Iris adatkészlet elemzése és modell tanítás
- MLflow model tracking és registry
- FastAPI REST API a modell kiszolgálásához
- Streamlit dashboard a felhasználói interfészhez
- Neptune.AI monitoring a teljesítmény monitorozásához

## Futtatás Docker segítségével

A projekt egyszerűen futtatható Docker konténerben, amely minden szükséges komponenst tartalmaz.
A Python 3.12.8 alapú Docker konténer automatikusan beállítja és elindítja az összes szolgáltatást.

### Előfeltételek
- Docker
- Docker Compose

### Használat

#### Windows rendszeren

Használja a mellékelt batch scriptet a konténer indításához:

```
run-docker.bat
```

Vagy futtatás a háttérben (detached mode):

```
run-docker.bat --detach
```

#### Linux/Mac rendszeren

Használja a mellékelt shell scriptet a konténer indításához:

```bash
./run-docker.sh
```

Vagy futtatás a háttérben (detached mode):

```bash
./run-docker.sh --detach
```

#### Konténer leállítása

```bash
# Windows
run-docker.bat --stop

# Linux/Mac
./run-docker.sh --stop
```

#### Szolgáltatások elérése
- MLflow UI: http://localhost:5000
- FastAPI dokumentáció: http://localhost:8000/docs
- Streamlit dashboard: http://localhost:8501

#### Docker parancsok közvetlen használata
```bash
# Konténer indítása
docker-compose up --build

# Konténer indítása a háttérben
docker-compose up --build -d

# Konténer leállítása
docker-compose down

# Logok megtekintése detached mode esetén
docker-compose logs -f
```

## Helyi futtatás (Docker nélkül)

### Követelmények telepítése
```bash
pip install -r requirements.txt
```

### Alkalmazások indítása
```bash
python src/run_all.py
```

## Docker támogatás fejlesztések

A projekt Docker támogatása jelentősen fejlesztve lett a következő komponensekkel:

### 1. Fejlett Docker környezet
- **Python 3.12.8** alapú konténer
- Biztonsági fejlesztések (nem root felhasználó, jogosultság kezelés)
- Optimalizált Docker kép rétegek
- Automatikus egészségellenőrzés

### 2. Docker kezelő eszközök
- **docker-builder.bat / docker-builder.sh**: Haladó Docker build és kezelő segédeszközök
- **run-docker.bat / run-docker.sh**: Egyszerűsített konténer indítás több móddal
- **.dockerignore**: Optimalizált Docker kép építés

### 3. Dokumentáció
- **docker-best-practices.md**: Docker legjobb gyakorlatok dokumentációja
- **docker-troubleshooting.md**: Hibaelhárítási útmutató

### 4. Hálózati és környezeti beállítások
- Docker hálózat konfigurálása a szolgáltatások közötti kommunikációhoz
- Környezeti változók beállítása (`DOCKER_MODE=true`)
- Erőforrás korlátok és monitorozás

## Projekt struktúra

- `src/api.py`: FastAPI modell kiszolgáló API
- `src/iris_ml_pipeline.py`: ML pipeline Airflow DAG-gal
- `src/neptuneai_monitoring.py`: Teljesítmény monitorozás
- `src/streamlit_app.py`: Felhasználói webfelület
- `src/run_all.py`: Minden komponens indítása egy scriptből
- `mlruns/`: MLflow kísérletek és modellek
- `docker-builder.bat/sh`: Docker build és kezelő segédeszközök
- `run-docker.bat/sh`: Docker konténer indító eszközök
