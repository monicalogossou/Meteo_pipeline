#dag\fetch_weather_dag
import sys
sys.path.append("/opt/airflow/api_fetcher")  

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from fetch_weather import fetch_all_cities

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
}

with DAG(
    dag_id="fetch_weather_dag",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2025, 9, 19),
    catchup=False,
    tags=["weather"],
) as dag:
     # 1. Extraction depuis API
    fetch_weather_task = PythonOperator(
        task_id="fetch_weather_task",
        python_callable=fetch_all_cities,
    )
    
        # 2. Transformation + Chargement via Spark
    transform_and_load_task = BashOperator(
        task_id="transform_and_load_task",
        bash_command="""
            docker exec -it spark-job bash \
            spark-submit \
                --conf spark.driver.extraJavaOptions='-Divy.home=/tmp/.ivy' \
                --conf spark.executor.extraJavaOptions='-Divy.home=/tmp/.ivy' \
                --jars /app/jars/postgresql.jar \
                /app/transform_load_weather.py
        """
 
   )
    fetch_weather_task >> transform_and_load_task