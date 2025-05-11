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
            if texto in fila["title"].lower():
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

    print("\nPlataformas disponibles:")
    for key, value in plataformas.items():
        print(f"{key}. {value.title()}")
    plataforma_key = input("Seleccione una plataforma (1-4): ")
    plataforma = plataformas.get(plataforma_key, "")

    print("\nCategorías disponibles:")
    for key, value in categorias.items():
        print(f"{key}. {value}")
    categoria = categorias.get(input("Seleccione una categoría (1-4): "), "")

    if not plataforma or not categoria:
        print("Error: Selección inválida.")
        return

    with open("movies.csv", 'r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        filtradas = []
        for fila in lector:
            valor_plataforma = fila.get(plataforma)
            if valor_plataforma and valor_plataforma.strip() == "1" and fila["age"].strip() == categoria:
                filtradas.append(fila)


        ordenadas = sorted(filtradas, key=rating_as_float, reverse=True)[:10]

        print(f"\nTop 10 en {plataforma.title()} ({categoria}):")
        for i, p in enumerate(ordenadas, 1):
            print(f"{i}. {p['title']} - Rating: {p['rating']}")

def validar_pelicula(pelicula):
    errores = []
    try:
        año = int(pelicula["year"])
        if not (1900 <= año <= 2026):
            errores.append("año invalido.")
    except:
        errores.append("año no es un numero valido.")

    if rating_as_float(pelicula["rating"]) == 0.0:
        errores.append("puntuacion invalida. usa formato como '85/100'.")

    if not pelicula["age"].endswith("+"):
        errores.append("categoría debe ser '7+', '13+', etc.")
    return errores

def agregar_pelicula():
    titulo = input("titulo: ")
    año = input("año: ")
    categoria = input("categoria (ej. 7+, 13+, 16+ , 18+): ")
    puntuacion = input("puntuacion (formato '90/100'): ")

    plataformas = {
        "netflix": "0",
        "hulu": "0",
        "prime video": "0",
        "disney+": "0"
    }

    plataforma_input = input("plataforma (Netflix/Hulu/Prime Video/Disney+): ").strip().lower()
    if plataforma_input in plataformas:
        plataformas[plataforma_input] = "1"
    else:
        print("plataforma no valida.")
        return

    nueva = {
        "title": titulo,
        "year": año,
        "age": categoria,
        "rating": puntuacion,
        "netflix": plataformas["netflix"],
        "hulu": plataformas["hulu"],
        "prime video": plataformas["prime video"],
        "disney+": plataformas["disney+"]
    }

    errores = validar_pelicula(nueva)
    if errores:
        print("errores:")
        for e in errores:
            print(f"- {e}")
        return

    with open("movies.csv", 'a', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["title", "year", "age", "rating", "netflix", "hulu", "prime video", "disney+"])
        escritor.writerow(nueva)
    print("la pelicula se agrego correctamente")


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
