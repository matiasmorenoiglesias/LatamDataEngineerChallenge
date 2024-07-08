import profile
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format, count
from pyspark.sql.window import Window
from pyspark.sql import functions as F
from memory_profiler import profile
import time

@profile
def q1_time(file_path: str):
      # Iniciar la sesión de Spark
    spark = SparkSession.builder \
        .appName("TwitterDataProcessing") \
        .config("spark.executor.memory", "2g") \
        .config("spark.python.profile.memory", True) \
        .getOrCreate()

    # Leer el archivo JSON
    df = spark.read.json(file_path)

    # Extraer la fecha y el usuario
    df = df.withColumn("fecha", date_format(col("date"), 'yyyy-MM-dd')) \
           .withColumn("usuario", col("user.username"))

    # Contar los tweets por día y usuario
    tweet_counts = df.groupBy("fecha", "usuario").count()

    # Obtener los días con más tweets
    top_days = tweet_counts.groupBy("fecha").sum("count").orderBy("sum(count)", ascending=False).limit(10)

    # Ventana para obtener el usuario con más tweets por día
    window_spec = Window.partitionBy("fecha").orderBy(col("count").desc())

    # Agregar el ranking de usuarios por número de tweets
    ranked_users = tweet_counts.withColumn("rank", F.rank().over(window_spec))

    # Filtrar para obtener solo los usuarios con más tweets por día
    top_users = ranked_users.filter(col("rank") == 1).select("fecha", "usuario")

    # Unir los días con más tweets con los usuarios con más tweets en esos días
    result_df = top_days.join(top_users, "fecha").select("fecha", "usuario")

    # Convertir a formato de salida esperado
    result = [(row.fecha, row.usuario) for row in result_df.collect()]

    # Detener la sesión de Spark
    spark.stop()

    return result

if __name__ == "__main__":
    start_time = time.time()
    print(q1_time("data/data.json"))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo de ejecución: {elapsed_time} segundos")