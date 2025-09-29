from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def run_spark_job():
    try:
        result = subprocess.run([
            "spark-submit",
            "--conf", "spark.driver.extraJavaOptions=-Divy.home=/tmp/.ivy",
            "--conf", "spark.executor.extraJavaOptions=-Divy.home=/tmp/.ivy",
            "--jars", "/app/jars/postgresql.jar",
            "/app/transform_load_weather.py"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            return {"message": "Spark job ran successfully", "output": result.stdout}, 200
        else:
            return {"error": "Spark job failed", "details": result.stderr}, 500

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)