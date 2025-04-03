import re
from collections import Counter

def validar_email(email):
    patron_email = r"^[a-zA-Z][a-zA-Z0-9_.-]*@(?:gmail|yahoo|outlook|hotmail|company)\.(co|uy|cl|ar|es|com|)$"
    return re.match(patron_email, email)

def validar_url(url):
    patron_url = r"^(https?:\/\/)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(\/.*)?(\?.*)?$"
    return re.match(patron_url, url)

def validar_ipv4(ip):
    patron_ip = r"\b(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}\b"
    return re.match(patron_ip, ip)

def analizar_emails(nombre_archivo):
    with open(nombre_archivo + ".txt", 'r') as archivo:
        lineas = archivo.readlines()
    for linea in lineas:
        linea = linea.strip()
        if validar_email(linea):
            print(f"email correcto: {linea}")
        else:
            print(f"email incorrecto: {linea}")

def analizar_urls(nombre_archivo):
    with open(nombre_archivo + ".txt", 'r') as archivo:
        lineas = archivo.readlines()
    for linea in lineas:
        linea = linea.strip()
        if validar_url(linea):
            print(f"url correcta: {linea}")
        else:
            print(f"url incorrecta: {linea}")

def analizar_ips(nombre_archivo):
    with open(nombre_archivo + ".txt", 'r',) as archivo:
        lineas = archivo.readlines()
    for linea in lineas:
        linea = linea.strip()
        if validar_ipv4(linea):
            print(f"ip correcta: {linea}")
        else:
            print(f"ip incorrecta: {linea}")

def contar_palabras(nombre_archivo):
    with open(nombre_archivo + ".txt", 'r',) as archivo:
        palabras = re.findall(r"\b\w+\b", archivo.read().lower())
    
    if not palabras:
        print("no contiene palabras.")
        return
    
    contar_palabras = Counter(palabras)
    palabra_mas_repetida, max_repeticiones = contar_palabras.most_common(1)[0]
    print(f"\nla mas repetida: '{palabra_mas_repetida}' ({max_repeticiones} veces)")

def menu():
    while True:
        print("\n===== MENÚ =====")
        print("1. analizar emails")
        print("2. analizar url")
        print("3. analizar ips")
        print("4. contar palabras en texto")
        print("5. salir")
        opcion = input("seleccione una opcion  ")
        
        if opcion == "1":
            nombre_archivo = input("ingrese el nombre del archivo de emails  ")
            analizar_emails(nombre_archivo)
        elif opcion == "2":
            nombre_archivo = input("ingrese el nombre del archivo de urls  ")
            analizar_urls(nombre_archivo)
        elif opcion == "3":
            nombre_archivo = input("ingrese el nombre del archivo de ips  ")
            analizar_ips(nombre_archivo)
        elif opcion == "4":
            nombre_archivo = input("ingrese el nombre del archivo de texto  ")
            contar_palabras(nombre_archivo)
        elif opcion == "5":
            print("cerrando la app")
            break
        else:
            print("elija una opcion correcta.")

if __name__ == "__main__":
    menu()
