from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
import os

def process_weather_data(input_dir="/data/raw", output_dir="/data/processed"):
    spark = SparkSession.builder.appName("Weather JSON to Parquet") \
        .config("spark.jars", "/app/jars/postgresql.jar") \
        .getOrCreate()

    try:
        cities = os.listdir(input_dir)
        for city in cities:
            city_path = os.path.join(input_dir, city)
            if not os.path.isdir(city_path):
                continue

            df_raw = spark.read.option("multiline", "true").json(f"{city_path}/*.json")
            if df_raw.count()== 0:
                print(f"Aucun fichier JSON pour la ville {city}, skip.")
                continue

            df = df_raw.select(
                to_date(col("location.localtime")).alias("date"),
                col("location.name").alias("ville"),
                col("location.country").alias("pays"),
                col("location.lat").alias("latitude"),
                col("location.lon").alias("longitude"),
                col("current.temp_c").alias("temperature"),
                col("current.humidity").alias("humidity"),
                col("current.condition.text").alias("condition"),
                col("current.wind_kph").alias("wind_kph"),
                col("current.pressure_mb").alias("pressure_mb"),
                col("current.uv").alias("uv_index")
            )

            output_path = os.path.join(output_dir, city)
            df.write.mode("overwrite").parquet(output_path)
            print(f"✅ Parquet écrit pour {city} dans {output_path}")

            df.write \
                .format("jdbc") \
                .option("url", "jdbc:postgresql://postgres:5432/airflow") \
                .option("dbtable", "weather_data") \
                .option("user", "airflow") \
                .option("password", "airflow") \
                .option("driver", "org.postgresql.Driver") \
                .mode("append") \
                .save()
            print(f"✅ Données chargées dans PostgreSQL pour {city}")

    finally:
        spark.stop()

if __name__ == "__main__":
    process_weather_data()
