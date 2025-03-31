import re as re


# EJERCICIO N° 1 
# Escribir una función en Python llamada validate_string que espere un único argumento de tipo string. La función deberá validar si el string cumple las siguientes condiciones: 
 
# Contiene al menos un carácter alfanumérico. 
# Contiene al menos una letra. 
# Contiene al menos una letra mayúscula. 
# Contiene al menos una letra minúscula. 
# Contiene al menos un dígito. 
# Contiene 8 o más caracteres. 
 
# El output esperado de la función es un  boolean (True o False) por cada condición que se evalúa, en el orden especificado en este ejercicio. 
 
# Por ejemplo: 
# Dado el string xYz8, el output esperado es: 
 
# ``` 
# True 
# True 
# True 
# True 
# False 
# ```  
# Dado el string xy@z!, el output esperado es: 
 
# ``` 
# True 
# True 
# False 
# True 
# False 
# False 
# ``` 
# Se pueden utilizar funciones auxiliares si se deseara, pero recordar que el resultado se evaluará llamando a la función validate_string

def validate_string(s):

    has_alphanumeric = any(char.isalnum() for char in s)       # Contiene al menos un caracter alfanumerico
    has_letter = any(char.isalpha() for char in s)    # Contiene al menos una letra
    has_uppercase = any(char.isupper() for char in s)  # Contiene almenos una mayuscula
    has_lowercase = any(char.islower() for char in s)  # Contiene almenos una minuscula
    has_digit = any(char.isdigit() for char in s)    # Contiene almenos un digito
    has_min_chars = len(s) >= 8  # Contiene 8 o mas caracteres
    return has_alphanumeric, has_letter, has_uppercase, has_lowercase, has_digit, has_min_chars


if __name__ == "__main__":
    test_strings = ["xYz8", "xy@z!", "Abc12345", "12345678", "ABCDEFG", "abcdefg"]
    
    for test in test_strings:
        print(f"'{test}' → {validate_string(test)}")