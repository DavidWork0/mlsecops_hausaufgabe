# mlsecops_hausaufgabe
Done project for MLSECOPS. Ats David

**BEFORE RUNNING!**
-create credentials.py and put it into src folder
-syntax can be observed in documentation (picture) and also here:

    class neptune_ai:
        project = "YOURPROJECTNAME"   
        api_token = "YOURAPITOKEN" 

-Add your project name instead of YOURPROJECTNAME and add your api token from neptuneai.
![image](https://github.com/user-attachments/assets/85172f9d-1e34-421b-a076-2ab54ffc434f)


**Running:**
-Go to folder
-Open shell
-Run/start docker
-insert command to shell/bash: docker-compose up --build -d
-Wait till the containers are running (depending on system wait 2-5min) - This project is far from optimization.
-insert command docker-compose logs
-Grab airflow password from logs from airflow-app-1 container
![docker compose logs parancs majd airflow jelszo_app1 containerbol](https://github.com/user-attachments/assets/7dcfe565-1aad-4f60-b254-335f38bc2604)

After everything is up and running (mainly the containers):

On localhost you can interact with:
MLflow - http://localhost:5000/ 
Airflow - http://localhost:8080/
Streamlit - http://localhost:8501/ 
Swagger - http://localhost:8000/docs

You can predict which flower you have is you add parameters:
Sepal length (cm) - float - accepted values: 0-10.0
Sepal width (cm) - float - accepted values: 0-10.0
Petal length (cm) - float - accepted values: 0-10.0
Petal width (cm) - float - accepted values: 0-10.0

Remark: This repo is far from optimazitation and the folders also containing unnecessary files for debugging. Please follow the above mentioned routine during startup. 
Tested on windows 11. 

Screenshots about the working process in order:
Docker containers after command docker-compose up --build -d
![docker build with compose build](https://github.com/user-attachments/assets/15b8082c-7d89-44a6-a509-9f447bb25de7)
![docker build with compose build2_done](https://github.com/user-attachments/assets/b4e725ba-8214-4d2a-abb4-57e9be095824)

After waiting several minutes the localhosts are up:
-MLflow:
![mlflow_reachable](https://github.com/user-attachments/assets/925b361c-b196-4c71-ac8e-3af5cb1c3552)

-API:
![image](https://github.com/user-attachments/assets/409dd981-3293-4860-894b-350c0bbf64ea)

-NeptuneAI working: (Basic metrics only)
![neptuneai_working](https://github.com/user-attachments/assets/3f47d7cb-690f-4cbc-a6d5-be1e841c2436)

-Streamlit (inference):
![streamlit_reachable](https://github.com/user-attachments/assets/8fc67825-4885-4350-a695-174b19b4bbd3)

Grab proper password for airflow from airflow-app-1 container. Username: admin
![docker compose logs parancs majd airflow jelszo_app1 containerbol](https://github.com/user-attachments/assets/411c7948-3cb9-4301-85ab-5449f7991ddc)

Airflow reachable after successful authentication:
![airflow_reachable](https://github.com/user-attachments/assets/3fbb75cc-ff7e-41ae-9366-0d4838add340)

You need to trigger a DAG event:
![image](https://github.com/user-attachments/assets/513ea78b-90ac-432c-9712-9bc03082556a)

After event DAG-s are running:
![airflow_reachable_dag_working](https://github.com/user-attachments/assets/5435f9e1-a80d-4d37-bc22-2e6344094607)
![airflow_reachable_dag_working](https://github.com/user-attachments/assets/c47a221d-dc53-4e83-86d3-08c04080bed3)
![airflow_reachable_dag_completed](https://github.com/user-attachments/assets/193d04f0-dfa3-49ed-9810-49fb790233a9)
