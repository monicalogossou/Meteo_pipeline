# README - Partie Airflow

## Présentation

Ce dossier contient la configuration et les fichiers nécessaires pour exécuter Apache Airflow dans le cadre du projet météo.

Airflow est orchestré via Docker Compose avec les services suivants :

- **webserver** : interface web d’Airflow  
- **scheduler** : planificateur qui lance les tâches  
- **worker** : exécutant les tâches (avec CeleryExecutor)  
- **postgres** : base de données  
- **redis** : broker Celery  
- **flower** : monitoring des workers  
- **minio** : stockage objet (optionnel)  

---

## Structure

```plaintext
airflow/
 ├── dags/          # Fichiers DAG Airflow (.py)
 ├── logs/          # Logs Airflow générés
 ├── plugins/       # Plugins Airflow personnalisés (opérateurs, hooks...)
 └── docs/          # document de debug
 └── README.md      # Ce fichier
 ```

## Commandes utiles

###Lancement de la stack Airflow

Dans la racine du projet (meteo_pipeline/), lancer :

docker-compose up --build

###Lister les DAGs :

docker-compose exec scheduler airflow dags list


###Exécuter un DAG manuellement :

docker-compose exec scheduler airflow dags trigger fetch_weather_dag


###Voir les logs d’un DAG/task :

docker-compose logs scheduler
docker-compose logs worker
