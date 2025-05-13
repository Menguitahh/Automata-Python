import csv

def rating_as_float(rating_str):
    try:
        return int(rating_str.split('/')[0]) / 100
    except:
        return 0.0

def buscar_titulo():
    texto = input("Ingrese el título a buscar: ").strip().lower()
    with open("movies.csv", 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        if not lector.fieldnames or 'title' not in lector.fieldnames:
            print("Error: El archivo CSV no tiene los encabezados correctos.")
            return

        coincidencias = []
        for fila in lector:
            if fila["title"].lower().startswith(texto):
                coincidencias.append(fila)

        if coincidencias:
            # Ordenar por rating descendente
            coincidencias.sort(key=rating_as_float, reverse=True)

            print("\nResultados:")
            for p in coincidencias:
                print(f"{p['title']} ({p['rating']}), Año: {p['year']}, Categoría: {p['age']}")
        else:
            print("No se encontraron coincidencias.")

def buscar_plataforma_categoria():
    plataformas = {
        "1": "netflix",
        "2": "hulu",
        "3": "prime video",
        "4": "disney+"
    }
    categorias = {
        "1": "7+",
        "2": "13+",
        "3": "16+",
        "4": "18+"
    }

    # Seleccionar plataforma válida
    plataforma_key = ""
    while plataforma_key not in plataformas:
        print("\nPlataformas disponibles:")
        for key, value in plataformas.items():
            print(f"{key}. {value.title()}")
        plataforma_key = input("Seleccione una plataforma (1-4): ").strip()
        if plataforma_key not in plataformas:
            print("❌ Entrada inválida. Ingrese un número del 1 al 4.")

    plataforma = plataformas[plataforma_key]

    # Seleccionar categoría válida
    categoria_key = ""
    while categoria_key not in categorias:
        print("\nCategorías disponibles:")
        for key, value in categorias.items():
            print(f"{key}. {value}")
        categoria_key = input("Seleccione una categoría (1-4): ").strip()
        if categoria_key not in categorias:
            print("❌ Entrada inválida. Ingrese un número del 1 al 4.")

    categoria = categorias[categoria_key]

    # Leer y filtrar CSV
    with open("movies.csv", 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        filtradas = []
        for fila in lector:
            valor_plataforma = fila.get(plataforma)
            if valor_plataforma and valor_plataforma.strip() == "1" and fila["age"].strip() == categoria:
                filtradas.append(fila)

        ordenadas = sorted(filtradas, key=rating_as_float, reverse=True)[:10]

        print(f"\n🎬 Top 10 en {plataforma.title()} ({categoria}):")
        for i, p in enumerate(ordenadas, 1):
            print(f"{i}. {p['title']} - Rating: {p['rating']}")

def agregar_pelicula():
    titulo = input("🎬 Título: ").strip()

    # Validar año
    while True:
        año = input("📅 Año (1900–2025): ").strip()
        if not año.isdigit():
            print("❌ El año debe ser un número.")
            continue
        año = int(año)
        if 1900 <= año <= 2025:
            break
        print("❌ Año fuera de rango. Debe estar entre 1900 y 2025.")

    # Validar categoría
    categorias_validas = {"7+", "13+", "16+", "18+"}
    while True:
        categoria = input("🔞 Categoría (7+, 13+, 16+, 18+): ").strip()
        if categoria in categorias_validas:
            break
        print("❌ Categoría inválida. Debe ser una de: 7+, 13+, 16+, 18+")

    # Validar puntuación
    while True:
        puntuacion = input("⭐ Puntuación (ej. '90/100' o solo '90'): ").strip()
        if '/' in puntuacion:
            partes = puntuacion.split('/')
            if len(partes) == 2 and partes[1] == '100' and partes[0].isdigit():
                break
            else:
                print("❌ Formato inválido. Debe ser como '90/100' o solo '90'.")
        elif puntuacion.isdigit():
            puntuacion += "/100"
            break
        else:
            print("❌ La puntuación debe ser un número entero o estar en formato '90/100'.")

    
    # Validar plataforma
    plataformas = {
        "netflix": "0",
        "hulu": "0",
        "prime video": "0",
        "disney+": "0"
    }

    while True:
        plataforma_input = input("📺 Plataforma (Netflix, Hulu, Prime Video, Disney+): ").strip().lower()
        if plataforma_input in plataformas:
            plataformas[plataforma_input] = "1"
            break
        else:
            print("❌ Plataforma no válida. Opciones válidas:")
            for p in plataformas:
                print(f"  - {p.title()}")

    # Armar registro nuevo
    nueva = {
        "title": titulo,
        "year": str(año),
        "age": categoria,
        "rating": puntuacion,
        "netflix": plataformas["netflix"],
        "hulu": plataformas["hulu"],
        "prime video": plataformas["prime video"],
        "disney+": plataformas["disney+"]
    }

    # Guardar en CSV
    with open("movies.csv", 'a', newline='', encoding='utf-8') as archivo:
        campos = ["title", "year", "age", "rating", "netflix", "hulu", "prime video", "disney+"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writerow(nueva)

    print("✅ La película se agregó correctamente.")


def menu():
    while True:
        print("\n===== MENÚ =====")
        print("1. Buscar por titulo(nombre)")
        print("2. Buscar por plataforma y categoria")
        print("3. Agregar nueva pelicula")
        print("4. Salir")
        opcion = input("seleccione una opcion: ")

        if opcion == "1":
            buscar_titulo()
        elif opcion == "2":
            buscar_plataforma_categoria()
        elif opcion == "3":
            agregar_pelicula()
        elif opcion == "4":
            print("Cerrando la app...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
