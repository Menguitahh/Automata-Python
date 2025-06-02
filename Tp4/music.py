import re
import csv
import os

    
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


#!PARTE 1 Funcion buscar por titulo o artista
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


#!PARTE 2 Validacion datos y carga desde archivo CSV

def validating_data(fila):
    Uri = r"^spotify:track:[a-zA-Z0-9]+$"
    
    
    Url_spotify = r"^https?://(?:open\.)?spotify\.com/(track|album|artist|playlist)/[a-zA-Z0-9]+$"
    
    
    
    Url_youtube = r"^https?://(?:www\.)?(youtube\.com|youtu\.be)/[a-zA-Z0-9_\-]+"

    if not re.match(Uri, fila.get('Uri', '')):
        return False, f"URI de Spotify inválida: {fila.get('Uri', '')}"
    if not re.match(Url_spotify, fila.get('Url_spotify', '')):
        return False, f"URL de Spotify inválida: {fila.get('Url_spotify', '')}"
    if not re.match(Url_youtube, fila.get('Url_youtube', '')):
        return False, f"URL de YouTube inválida: {fila.get('Url_youtube', '')}"
    
    try: # Convierte likes y views a enteros para comparar
        likes = int(float(fila.get('Likes', 0)))
        views = int(float(fila.get('Views', 0)))
        if likes > views:
            return False, "Los Likes no pueden ser mayores que las visitas."
    except Exception as e:
        return False, f"Error al convertir Likes o Views a entero: {e}"

    return True, None


def insert_from_csv(name_file):
    path_destino = "spotify_and_youtube.csv"

    print(f"Leyendo encabezados del archivo destino: {path_destino}")
    with open(path_destino, 'r', encoding='utf-8') as destino:
        encabezados = next(csv.reader(destino))
        print("Encabezados detectados:", encabezados)

    print(f"Abriendo archivo de origen: {name_file}")
    with open(name_file, 'r', encoding='utf-8') as archivo_origen:
        lector = csv.DictReader(archivo_origen)
        filas_validas = []

        for i, fila in enumerate(lector, 1):
            print(f"\nProcesando fila #{i}")
            fila['Duration_ms'] = convert_duration(fila['Duration_ms'])

            if fila['Likes'].strip() == '' or fila['Views'].strip() == '':
                print("⚠️ Fila con datos faltantes, se omite:", fila)
                continue

                # elimina espacios en blanco
            fila['Uri'] = fila['Uri'].strip()
            fila['Track'] = fila['Track'].strip()
            fila['Url_spotify'] = fila['Url_spotify'].strip()
            fila['Url_youtube'] = fila['Url_youtube'].strip()
            fila['Artist'] = fila['Artist'].strip()
            fila['Album'] = fila['Album'].strip()

            valido, error = validating_data(fila)
            if valido:
                print("Registro válido:", fila)
                filas_validas.append(fila)
            else:
                print("Registro inválido:", error)

    if filas_validas:
        print(f"\nAgregando {len(filas_validas)} filas válidas al archivo destino.")
        with open(path_destino, 'a', newline='', encoding='utf-8') as destino:
            writer = csv.DictWriter(destino, fieldnames=encabezados)
            for fila in filas_validas:
                writer.writerow(fila)
        print("Agregado con éxito.")
    else:
        print("No hay filas válidas para agregar.")


def manual_insert():
    def Request_field(mensaje, validacion=None, error_msg="Valor inválido. Intente nuevamente."):
        while True:
            value = input(mensaje)
            if validacion is None or validacion(value):
                return value
            else:
                print(error_msg)

    def validating_uri(uri):
        return re.match(r"^spotify:track:[a-zA-Z0-9]+$", uri)

    def validating_url_spotify(url):
        return re.match(r"^https?://(?:open\.)?spotify\.com/(track|album|artist|playlist)/[a-zA-Z0-9]+$", url)

    def validating_url_youtube(url):
        return re.match(r"^https?://(?:www\.)?(youtube\.com|youtu\.be)/[a-zA-Z0-9_\-]+", url)

    def validating_entero(entrada):
        return entrada.isdigit()

    Artist = input("Ingrese el nombre del artista: ")
    Track = input("Ingrese el título de la canción: ")
    Album = input("Ingrese el nombre del álbum: ")
    
    Uri = Request_field("URI Spotify: ", validating_uri, "URI de Spotify inválida. Debe tener el formato spotify:track:ID")
    Duration_ms = Request_field("Ingrese la duración (en milisegundos): ", validating_entero, "Debe ser un número entero")
    while True:
        Views = Request_field("Ingrese la cantidad de vistas: ", validating_entero, "Debe ser un número entero")
        Likes = Request_field("Ingrese la cantidad de likes: ", validating_entero, "Debe ser un número entero")
        if int(Views)  > int(Likes) > 0:
            break
        else:
            print("Los likes no pueden ser mayores que las vistas.")
    Url_spotify = Request_field("Ingrese la URL de Spotify: ", validating_url_spotify, "URL de Spotify inválida.")
    Url_youtube = Request_field("Ingrese la URL de YouTube: ", validating_url_youtube, "URL de YouTube inválida.")
    
    fila = {
        'Artist': Artist,
        'Url_spotify': Url_spotify,
        'Track': Track,
        'Album': Album,
        'Uri': Uri,
        'Duration_ms': Duration_ms,
        'Views': Views,
        'Likes': Likes,
        'Url_youtube': Url_youtube
    }

    valid, error = validating_data(fila)
    if valid:
        print("Registro válido:", fila)
        try:
            # Leer los encabezados desde el archivo CSV original
            path_csv = "spotify_and_youtube.csv"
            with open(path_csv, 'r', encoding='utf-8') as f:
                encabezados = next(csv.reader(f))

            # Escribir la fila nueva respetando los encabezados del archivo
            with open(path_csv, 'a', newline='', encoding='utf-8') as archivo:
                writer = csv.DictWriter(archivo, fieldnames=encabezados)
                writer.writerow(fila)

            print("Registro agregado al archivo CSV en el orden correcto.")
        except Exception as e:
            print("Error al escribir en el archivo CSV:", e)
    else:
        print("Registro inválido:", error)


#!PARTE 3 top 10 canciones de artista
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

    print(f"\nTop 10 canciones más reproducidas de {name.title()}:\n")
    for i, song in enumerate(top_10, 1):
        duration = convert_duration(song["Duration_ms"])
        views = float(song["Views"]) / 1_000_000 if song["Views"] else 0
        print(f"{i}. {song['Artist']} - {song['Track']} | Duración: {duration} | Reproducciones: {round(views, 2)} millones")


#!PARTE 4 mostrar los albumes de un artista
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
            name_file = os.path.join(name_file + ".csv")
            if not os.path.exists(name_file):
                print(f"El archivo {name_file} no existe.")
                continue
            else:
                insert_from_csv(name_file)

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