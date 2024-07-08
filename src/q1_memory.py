from collections import defaultdict
from datetime import datetime
import time
from typing import List, Tuple
import json
from memory_profiler import profile


@profile
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Función para procesar cada tweet y devolver la fecha y el nombre de usuario
    
    def process_tweet(tweet):
        fecha = datetime.fromisoformat(tweet["date"]).date()
        usuario = tweet["user"]["username"]
        return fecha, usuario

    # Función para leer los tweets del archivo y aplicar el procesamiento
    def read_tweets(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                yield process_tweet(json.loads(line))

    # Diccionario para almacenar la cantidad total de tweets por día y el usuario con más tweets
    tweets_por_dia = {}
    usuario_mas_tweets: defaultdict = defaultdict(lambda: {'total_tweets': 0, 'max_tweets': 0, 'usuario_mas_tweets': None})

    # Procesar cada tweet y actualizar los contadores
    for fecha, usuario in read_tweets(file_path):
        # Actualizar el total de tweets para este día
        if fecha not in tweets_por_dia:
            tweets_por_dia[fecha] = 0
        tweets_por_dia[fecha] += 1

        # Actualizar el contador de tweets por usuario y determinar el usuario con más tweets para este día
        current_data = usuario_mas_tweets[fecha]
        current_data['total_tweets'] += 1
        if current_data['usuario_mas_tweets'] is None:
            current_data['usuario_mas_tweets'] = usuario
            current_data['max_tweets'] = 1
        elif usuario == current_data['usuario_mas_tweets']:
            current_data['max_tweets'] += 1
        elif current_data['max_tweets'] == 1:
            current_data['usuario_mas_tweets'] = usuario

    # Obtener los top_n días con más tweets
    sorted_days = sorted(tweets_por_dia.items(), key=lambda item: item[1], reverse=True)[:10]

    # Retornar los resultados en el formato solicitado
    return [(fecha, usuario_mas_tweets[fecha]['usuario_mas_tweets']) for fecha, _ in sorted_days]


if __name__ == "__main__":
    start_time = time.time()
    print(q1_memory("data/data.json"))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo de ejecución: {elapsed_time} segundos")