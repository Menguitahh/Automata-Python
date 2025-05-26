import re
import csv

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
        for row in lector:
            artist = row["Artist"].strip().lower()
            if artist == name:
                songs.append(row)

    if not songs:
        print("No se encontraron artistas. Verificá si lo escribiste bien.")
        return

    def views_float(row):
        try:
            return float(row["Views"]) # asegura que se puede ordenar correctamente por vistas, incluso si los datos tienen errores
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

        option = input("Opción elegida: ")

        if option == "1":
            print("Cerrando la app...")
        elif option == "2":
            top_10_artist()
        elif option == "3":
            print("Cerrando la app...")
        elif option == "4":
            print("Cerrando la app...")
        elif option == "5":
            print("\nGracias por usar el sistema! ;)\n")
            break
        else:
            print("Opción invalida. Intente de nuevo.")



if __name__ == "__main__":
    menu()