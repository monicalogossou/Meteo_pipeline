# Debug et Mise en place du DAG Airflow `fetch_weather_dag`

## Contexte

- Projet Airflow avec DAG pour récupérer la météo via API (`fetch_weather_dag.py`)
- Structure de projet :



/meteo_pipeline
├─ airflow/dags/fetch_weather_dag.py
├─ api_fetcher/fetch_weather.py
└─ docker-compose.yml


---

## Problèmes rencontrés

### 1. DAG non visible dans Airflow UI ni avec `airflow dags list`

- La commande `airflow dags list` renvoyait `No data found`
- Le DAG semblait absent, bien que présent dans le dossier `/airflow/dags`

### 2. Erreurs dans les logs du scheduler / absence d’erreur claire

- Le scheduler ne listait pas le DAG
- Aucune erreur explicite visible dans les logs pour le DAG

### 3. Docker-compose ne montait pas correctement tous les dossiers nécessaires

- Le dossier `api_fetcher` n’était pas monté dans les containers `scheduler` et `worker`
- Parfois, les volumes personnalisés dans `scheduler` et `worker` écrasaient ceux hérités

### 4. Import Python invalide dans le DAG

- Import `from api_fetcher.fetch_weather import fetch_all_cities` échouait dans le container car `api_fetcher` n’était pas dans le `PYTHONPATH`
- Python ignorait silencieusement le fichier DAG complet faute de module accessible

---

## Causes principales

- Montages Docker (volumes) incomplets ou écrasés, ce qui empêchait Airflow de trouver le dossier `api_fetcher` et ses scripts
- Le dossier `api_fetcher` n’était pas ajouté au chemin Python (`sys.path`) dans le DAG
- Par défaut, Airflow ne charge que les fichiers dans `/opt/airflow/dags` et ne connaît pas les modules externes

---

## Solutions appliquées

### 1. Correction du montage des volumes dans `docker-compose.yml`

- Ajout de la ligne `- ./api_fetcher:/opt/airflow/api_fetcher` dans tous les services Airflow (`scheduler`, `worker`, `webserver`) **en s’assurant que les volumes hérités ne soient pas écrasés**

```yaml
volumes:
  - ./airflow/dags:/opt/airflow/dags
  - ./airflow/logs:/opt/airflow/logs
  - ./airflow/plugins:/opt/airflow/plugins
  - ./api_fetcher:/opt/airflow/api_fetcher
  - ./data:/data  # ajout optionnel selon besoin