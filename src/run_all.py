"""
Ez a script folyamatosan elindítja a szükséges lépéseket:
- Modell tanítás és regisztráció (api.py)
- MLflow UI indítása
- REST API indítása
- neptuneai monitoring futtatása
- Streamlit dashboard indítása

A REST API, MLflow UI és Streamlit külön folyamatban futnak, így a script minden szükséges komponenst elindít.
"""

import subprocess
import time
import webbrowser
import os
import sys
import signal

def run_process(command, name):
    print(f"Indítás: {name}...")
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc
    except Exception as e:
        print(f"Hiba a(z) {name} indítása során: {e}")
        return None

# MLflow UI indítása háttérben
mlflow_proc = run_process(["mlflow", "ui"], "MLflow UI")
time.sleep(3)  # Várunk, hogy elinduljon
if mlflow_proc:
    webbrowser.open("http://localhost:5000")
    print("MLflow UI elérhetősége: http://localhost:5000")
else:
    print("Hiba: MLflow UI nem indult el")

# Modell tanítás és regisztráció
print("Modell tanítása és regisztrálása...")
try:
    subprocess.run(["python", "src/api.py"], check=True)
    print("Modell tanítása és regisztrálása sikeres")
except subprocess.CalledProcessError as e:
    print(f"Hiba a modell tanítása során: {e}")

# REST API indítása háttérben
restapi_proc = run_process(["uvicorn", "src.api:app", "--host", "127.0.0.1", "--port", "8000"], "REST API")
time.sleep(2)
if restapi_proc:
    webbrowser.open("http://localhost:8000/docs")
    print("REST API elérhetősége: http://localhost:8000/docs")
else:
    print("Hiba: REST API nem indult el")

# Neptun AI monitoring futtatása
try:
    subprocess.run(["python", "src/neptuneai_monitoring.py"], check=True)
    print("Neptune AI monitoring futtatása sikeres")
except subprocess.CalledProcessError as e:
    print(f"Hiba a Neptune AI monitoring futtatása során: {e}")

# Streamlit dashboard indítása háttérben
streamlit_proc = run_process(["streamlit", "run", "src/streamlit_app.py"], "Streamlit Dashboard")
time.sleep(5)  # Több időt adunk a Streamlit indulásához
if streamlit_proc:
    counter = 0
    webbrowser.open("http://localhost:8501")
    print("Streamlit Dashboard elérhetősége: http://localhost:8501")
else:
    print("Hiba: Streamlit Dashboard nem indult el")

# Folyamatok tárolása a megfelelő leállításhoz
processes = {
    "MLflow UI": mlflow_proc,
    "REST API": restapi_proc,
    "Streamlit Dashboard": streamlit_proc
}

print("\nMinden komponens elindítva. Leállításhoz zárd be ezt a scriptet vagy nyomj Ctrl+C.")

# Megfelelő leállítás biztosítása
def shutdown_gracefully(sig, frame):
    print("\nLeállítás...")
    for name, proc in processes.items():
        if proc:
            try:
                print(f"{name} leállítása...")
                if sys.platform == "win32":
                    # Windows-specifikus leállítás
                    proc.terminate()
                else:
                    # Unix-specifikus leállítás
                    proc.send_signal(signal.SIGTERM)
                proc.wait(timeout=5)
            except Exception as e:
                print(f"Hiba a(z) {name} leállítása során: {e}")
                try:
                    proc.kill()
                except:
                    pass
    print("Minden folyamat leállítva.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_gracefully)
signal.signal(signal.SIGTERM, shutdown_gracefully)

try:
    # A főfolyamat folyamatosan fut
    while True:
        time.sleep(1)
        
        # Ellenőrizzük, hogy a folyamatok még mindig futnak-e
        for name, proc in processes.items():
            if proc and proc.poll() is not None:
                print(f"Figyelmeztetés: {name} leállt.")
                
except KeyboardInterrupt:
    shutdown_gracefully(None, None)
