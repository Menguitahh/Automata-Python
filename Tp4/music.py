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


#!PARTE 1
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


#!PARTE 2
def validating_data(fila):
    Uri = r"^spotify:track:[\w\d]+$"
    Url_spotify = r"^https?://(?:open\.)?spotify\.com/\/[\w\d]+$"
    Url_youtube = r"https?://(?:www\.?youtube\.com|youtu\.be)/[\w\d]+$"

    if not re.match(Uri, fila['Url_spotify']):
        return print(f"URL de Spotify inválida: {fila['Url_spotify']}")
    if not re.match(Url_spotify, fila['Url_spotify']):
        return print(f"URL de Spotify inválida: {fila['url_spotify']}")
    if not re.match(Url_youtube, fila['Url_youtube']):
        return print(f"URL de YouTube inválida: {fila['url_youtube']}")
    
    if int(fila['likes']) > int(fila['views']):

        return print("Los Likes no pueden ser mayores que las visitas.")
    return True    
    
def insert_from_csv(name_file):
        with open(name_file, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                fila['Duration_ms'] = convert_duration(fila['Duration_ms'])
                if fila['Likes'].strip() == '' or fila['Views'].strip() == '':
                    print("Fila con datos faltantes, se omite:", fila)
                    continue
                fila['Uri'] = (fila['Uri']).strip()
                fila['Track'] = (fila['Track'])
                fila['Url_spotify'] = fila['Url_spotify'].strip()
                fila['Url_youtube'] = fila['Url_youtube'].strip()
                fila['Artist'] = fila['Artist'].strip()
                fila['Album'] = fila['Album'].strip()
                
            
            if validating_data(fila):
                print("Registro válido:", fila)
            else:
                print("Registro inválido:", fila)
                

def manual_insert():
    Artist = input("Ingrese el nombre del artista: ")
    Track = input("Ingrese el título de la canción: ")
    Album = input("Ingrese el nombre del álbum: ")
    Uri = input("URI Sportify: ")
    Duration_ms = input("Ingrese la duración (en milisegundos): ")
    Views = input("Ingrese la cantidad de vistas: ")
    Likes = input("Ingrese la cantidad de likes: ")
    Url_spotify = input("Ingrese la URL de Spotify: ")
    Url_youtube = input("Ingrese la URL de YouTube: ")
        
        
    fila = {
        'Artist': Artist,
        'Track': Track,
        'Album': Album,
        'Iri': Uri,
        'Duration_ms': Duration_ms,
        'Views': Views,
        'Likes': Likes,
        'Url_spotify': Url_spotify,
        'Url_youtube': Url_youtube
    }
        
    valido, error = validating_data(fila)
    if valido:
        print("Registro válido:", fila)
    else:
            print("Registro inválido:", error)


#!PARTE 3
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


#!PARTE 4
def show_albums():
    artist_input = input("Ingrese el nombre del artista: ").strip()
    albums = {}

    with open("spotify_and_youtube.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            artist = row.get("Artist", "")
            album = row.get("Album", "")
            duration_ms = row.get("Duration_ms", "0")

            if artist_input.lower() == artist.lower():
                if album not in albums:
                    albums[album] = {
                        "songs": 0,
                        "total_duration": 0
                    }
                albums[album]["songs"] += 1

                try:
                    albums[album]["total_duration"] += int(float(duration_ms))
                except ValueError:
                    pass

    if not albums:
        print("No se encontraron álbumes para ese artista.")
        return
    
    print(f"\n{artist_input} tiene {len(albums)} álbum(es):\n")
    
    for i, (album_name, data) in enumerate(albums.items(), 1): #!El enumerate permite agregar un número de orden empezando desde 1.
        duration = convert_duration(data["total_duration"])
        print(f"{i}. Álbum: {album_name}")
        print(f"   - Canciones: {data['songs']}")
        print(f"   - Duración total: {duration}")


def menu():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Buscar por Título o Artista")
        print("2. Mostrar Top 10 canciones de un Artista")
        print("3. Insertar nuevo registro (desde archivo)")
        print("4. Insertar nuevo registro (manualmente)")
        print("5. Mostrar Álbumes de un Artista")
        print("6. Salir")
        print("----------------------")

        option = input("seleccione una opcion: ")

        if option == "1":
            search_title_or_artist()
        elif option == "2":
            top_10_artist()
        elif option == "3":
            name_file = input("Ingrese el nombre del archivo CSV: ")
            if not name_file.endswith('.csv'):
                name_file += '.csv'
        elif option == "4":
            print("insertando registro manual...")
            manual_insert()
        elif option == "5":
            show_albums()
        elif option == "6":
            print("Cerrando la app...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()