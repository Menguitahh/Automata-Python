import re
import csv
from datetime import timedelta

# Funcion para convertir milisegundos a horas, minutos y segundos
def convert_duration(ms):
    try:
        seconds = int(ms) // 1000
        return str(timedelta(seconds=seconds))
    except:
        return "00:00:00"
    
def top_10_artista():
    nombre = input("Ingresa el artista: ")
    canciones = []

    with open("spotify_and_youtube.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if re.search(nombre, fila["Artist"], re.IGNORECASE): #re.IGNORECASE es para indicar q la busqueda no distinga entre mayusculas y minusculas
                canciones.append(fila)

    if not canciones:
        print("No se encontraron canciones")
        return

    def vistas_en_float(fila):
        try:
            return float(fila["Views"]) #asegura que se puede ordenar correctamente por vistas, incluso si los datos tienen errores
        except (ValueError, TypeError):
            return 0

    top_10 = sorted(canciones, key=vistas_en_float, reverse=True)[:10]

    print(f"\n Top 10 canciones más reproducidas de {nombre.title()}:\n")
    for i, p in enumerate(top_10, 1):
        duracion = convert_duration(p["Duration_ms"])
        vistas = float(p["Views"]) / 1_000_000 if p["Views"] else 0
        print(f"{i}. {p['Artist']} - {p['Track']} | Duración: {duracion} | Reproducciones: {round(vistas, 2)} millones")


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
            print("Cerrando la app...")
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