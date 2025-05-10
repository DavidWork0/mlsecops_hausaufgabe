"""
Ez a script folyamatosan elindítja a szükséges lépéseket:
- Modell tanítás és regisztráció (api.py)
- MLflow UI indítása
- REST API indítása
- neptuneai monitoring futtatása
- Streamlit dashboard indítása
- Airflow webserver és scheduler indítása

A REST API, MLflow UI, Streamlit és Airflow külön folyamatban futnak, így a script minden szükséges komponenst elindít.
"""

import subprocess
import time
import webbrowser
import os
import sys
import signal
import argparse


def run_process(command, name):
    print(f"Indítás: {name}...")
    try:
        # Redirecting stderr to stdout to capture all output
        proc = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        return proc
    except Exception as e:
        print(f"Hiba a(z) {name} indítása során: {e}")
        return None

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
        # Nyomon követjük, hogy streamlit-et már megnyitottuk-e
        streamlit_opened = False
        if streamlit_proc:
            streamlit_opened = True
        
        # A főfolyamat folyamatosan fut
        while True:
            time.sleep(1)
            # Ellenőrizzük, hogy a folyamatok még mindig futnak-e
            for name, proc in list(processes.items()):
                if proc and proc.poll() is not None:
                    print(f"Figyelmeztetés: {name} leállt.")
                    
                    # Attempt to read any output from the failed process
                    if proc.stdout:
                        output = proc.stdout.read()
                        if output:
                            print(f"{name} kimenet: {output}")
                    
                    # Restart the process if it's one that should keep running
                    if name == "REST API":
                        print(f"Újraindítás: {name}...")
                        host = "0.0.0.0" if os.environ.get("DOCKER_MODE") == "true" else "127.0.0.1"
                        new_proc = run_process(["uvicorn", "src.api:app", "--host", host, "--port", "8000"], "REST API")
                        if new_proc:
                            processes[name] = new_proc
                            print(f"{name} újraindítva")
                    
                    if name == "Streamlit Dashboard":
                        print(f"Újraindítás: {name}...")
                        new_proc = run_process(["streamlit", "run", "src/streamlit_app.py", "--server.headless=true", "--server.port=8501", "--server.address=0.0.0.0"], "Streamlit Dashboard")
                        if new_proc:
                            processes[name] = new_proc
                            print(f"{name} újraindítva")
                            # Csak akkor nyitjuk meg a böngészőt újra, ha ez az első indítás
                            if not streamlit_opened:
                                time.sleep(5)  # Várunk, hogy a Streamlit elinduljon
                                webbrowser.open("http://localhost:8501")
                                print("Streamlit Dashboard elérhetősége: http://localhost:8501")
                                streamlit_opened = True
                    
                    if name == "Airflow Webserver":
                        print(f"Újraindítás: {name}...")
                        new_proc = run_process(["airflow", "webserver", "-p", "8080"], "Airflow Webserver")
                        if new_proc:
                            processes[name] = new_proc
                            print(f"{name} újraindítva")
                            
                    if name == "Airflow Scheduler":
                        print(f"Újraindítás: {name}...")
                        new_proc = run_process(["airflow", "scheduler"], "Airflow Scheduler")
                        if new_proc:
                            processes[name] = new_proc
                            print(f"{name} újraindítva")
    except KeyboardInterrupt:
        shutdown_gracefully(None, None)

def main(processes):
    import subprocess
    import time
    import webbrowser
    import os
    import sys
    import signal
    print("Starting run_all.py")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print("Listing installed packages:")
    os.system("pip list")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run all components of the ML system")
    parser.add_argument("--run-once", action="store_true", help="Run the script once without monitoring processes")
    args = parser.parse_args()
    
    # Set the host based on whether we're in Docker or not
    host = "0.0.0.0" if os.environ.get("DOCKER_MODE") == "true" else "127.0.0.1"
    print(f"Using host: {host} (Docker mode: {os.environ.get('DOCKER_MODE')})")
    
    # MLflow UI indítása háttérben
    mlflow_proc = run_process(["mlflow", "ui", "--host", host], "MLflow UI")
    time.sleep(3)  # Várunk, hogy elinduljon
    if mlflow_proc:
        if host == "127.0.0.1":
            webbrowser.open("http://localhost:5000")
        print("MLflow UI elérhetősége: http://localhost:5000")
    else:
        print("Hiba: MLflow UI nem indult el")

    # Modell tanítás és regisztráció
    print("Modell tanítása és regisztrálása...")
    try:
        # Setting GIT_PYTHON_REFRESH to silence git warnings
        env = os.environ.copy()
        env["GIT_PYTHON_REFRESH"] = "quiet"
        subprocess.run(["python", "src/api.py"], check=True, env=env)
        print("Modell tanítása és regisztrálása sikeres")
    except subprocess.CalledProcessError as e:
        print(f"Hiba a modell tanítása során: {e}")

    # REST API indítása háttérben
    restapi_proc = run_process(["uvicorn", "src.api:app", "--host", host, "--port", "8000"], "REST API")
    time.sleep(2)
    if restapi_proc:
        if host == "127.0.0.1":
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

    # Streamlit Dashboard indítása
    streamlit_proc = run_process(["streamlit", "run", "src/streamlit_app.py", "--server.headless=true", "--server.port=8501", "--server.address=0.0.0.0"], "Streamlit Dashboard")
    time.sleep(5)  # Több időt adunk a Streamlit indulásához
    if streamlit_proc:
        if host == "127.0.0.1":
            webbrowser.open("http://localhost:8501")
        print("Streamlit Dashboard elérhetősége: http://localhost:8501")
    else:
        print("Hiba: Streamlit Dashboard nem indult el")

    # Airflow esetén a webserver és scheduler már fut a dockerben
    # Itt csak a böngészőt nyitjuk meg
    if host == "127.0.0.1":
        webbrowser.open("http://localhost:8080")
    print("Airflow UI elérhetősége: http://localhost:8080")

    # Folyamatok tárolása a megfelelő leállításhoz
    processes = {
        "MLflow UI": mlflow_proc,
        "REST API": restapi_proc,
        "Streamlit Dashboard": streamlit_proc
    }

    # If run-once flag is set, return processes and exit without monitoring
    if args.run_once:
        print("\nEgyszeri futtatás kész. A futó folyamatokat a Docker kezeli.")
        return processes

    print("\nMinden komponens elindítva. Leállításhoz zárd be ezt a scriptet vagy nyomj Ctrl+C.")
    print("Run_all.py completed successfully")

    return processes


if __name__ == "__main__":
    # Folyamatok tárolása a megfelelő leállításhoz
    processes = {}

    # Fő funkció meghívása
    processes = main(processes)
