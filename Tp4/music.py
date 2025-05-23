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


def search_title_or_artist():

    while True:
        print("\n--- MENÚ DE BÚSQUEDA ---")
        print("1. Buscar por Título")
        print("2. Buscar por Artista")
        print("3. Salir")
        
        try:
            option = int(input("Qué desea hacer? (1-3): "))

        except ValueError:
            print("Número inválido. Ingrese otro: ")
            continue
    
        if option == 1:
            print("Búsqueda por Título")
            query = input("Ingrese un Título: ").strip().lower()
            field = "Track"

        elif option == 2:
            print("Búsqueda por Artista")
            query = input("Ingrese un Artista: ").strip().lower()
            field = "Artist"
        
        elif option == 3:
            print("Saliendo...")
            break
        
        else:
            print("Opción inválida.")
            continue

        with open("spotify_and_youtube.csv", 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames or field not in reader.fieldnames:
                print(f"El campo '{field}' no existe en el archivo.")
                continue

            coincidences = []

            for row in reader:
                if row[field].lower().startswith(query):
                    coincidences.append(row)

            if coincidences:
                # Ordenar por rating descendente
                coincidences.sort(key=lambda x: int(x.get("views", 0)), reverse=True)
                #coincidences = coincidences[:10]  #! limitar a top 10 PREGUNTAR

                print(f"\n Se encontraron {len(coincidences)} resultados:")
                for c in coincidences:
                    print(f"- {c['Artist']} - {c['Track']} | {convert_duration(c['Duration_ms'])}")
            else:
                print("No se encontraron coincidencias.")


def menu():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Buscar por Título o Artista")
        print("2. Mostrar todas las canciones ordenadas por reproducciones (descendente)")
        print("3. Mostrar Top 10 canciones de un Artista")
        print("4. Insertar nuevo registro (manual o desde archivo)")
        print("5. Mostrar Álbumes de un Artista")
        print("6. Salir")
        print("----------------------")

        option = input("seleccione una opcion: ")

        if option == "1":
            search_title_or_artist()
        elif option == "2":
            print("Cerrando la app...")
        elif option == "3":
            print("Cerrando la app...")
        elif option == "4":
            print("Cerrando la app...")
        elif option == "5":
            print("Cerrando la app...")
        elif option == "6":
            print("Cerrando la app...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()