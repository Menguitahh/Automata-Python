import re
import csv
from datetime import timedelta

# Funcion para convertir milisegundos a horas, minutos y segundos
def convert_duration(ms):
    try:
        ms = int(float(ms))  # Asegura que sea entero, incluso si viene como string float
        if ms <= 0:
            return "00:00:00"
        seconds = ms // 1000
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    except (ValueError, TypeError):
        return "00:00:00"  # Por defecto si hay error
    
def top_10_artist():
    name = input("Ingresa el artista: ")
    songs = []

    with open("spotify_and_youtube.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if re.search(name, fila["Artist"], re.IGNORECASE): #re.IGNORECASE es para indicar q la busqueda no distinga entre mayusculas y minusculas
                songs.append(fila)

    if not songs:
        print("No se encontraron canciones")
        return

    def views_float(fila):
        try:
            return float(fila["Views"]) #asegura que se puede ordenar correctamente por vistas, incluso si los datos tienen errores
        except (ValueError, TypeError):
            return 0

    top_10 = sorted(songs, key=views_float, reverse=True)[:10]

    print(f"\n Top 10 canciones más reproducidas de {name.title()}:\n")
    for i, song in enumerate(top_10, 1):
        duration = convert_duration(song["Duration_ms"])
        views = float(song["Views"]) / 1_000_000 if song["Views"] else 0
        print(f"{i}. {song['Artist']} - {song['Track']} | Duración: {duration} | Reproducciones: {round(views, 2)} millones")



def menu():
    while True:
        print("\n" + "="*40)
        print("SISTEMA DE MÚSICA")
        print("="*40)
        print("Seleccioná una opción:\n")
        print("1️  Buscar por Título o Artista")
        print("2  Top 10 canciones de un Artista")
        print("3  Insertar nuevo registro (manual o archivo)")
        print("4  Mostrar álbumes de un Artista")
        print("5  Salir\n")
        print("-"*40)

        opcion = input("Opción elegida: ")

        if opcion == "1":
            print("Cerrando la app...")
        elif opcion == "2":
            top_10_artist()
        elif opcion == "3":
            print("Cerrando la app...")
        elif opcion == "4":
            print("Cerrando la app...")
        elif opcion == "5":
            print("\nGracias por usar el sistema! ;)\n")
            break
        else:
            print("Opción invalida. Intente de nuevo.")



if __name__ == "__main__":
    menu()