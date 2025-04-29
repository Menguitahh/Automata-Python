# Ejercicio 3 - Punto 4: Definición del AFD

class AFD:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion

    def acepta(self, cadena):
        estado_actual = self.estado_inicial
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False
            if simbolo not in self.transiciones.get(estado_actual, {}):
                return False
            estado_actual = self.transiciones[estado_actual][simbolo]
        return estado_actual in self.estados_aceptacion

# Definimos el AFD
estados_afd = {'A', 'B', 'C'}
alfabeto_afd = {'a', 'b'}
estado_inicial_afd = 'A'
transiciones_afd = {
    'A': {'a': 'B', 'b': 'C'},
    'B': {'a': 'B', 'b': 'C'},
    'C': {'a': 'B', 'b': 'C'}
}
estados_aceptacion_afd = {'A', 'B', 'C'}

afd = AFD(estados_afd, alfabeto_afd, transiciones_afd, estado_inicial_afd, estados_aceptacion_afd)
cadenas_prueba = ['a', 'b', '', 'ab', 'ba', 'aba', 'bb', 'aab', 'aabbababab', 'ad', 'abdbb', 'aaaa', 'bbbb']

# Probar aceptación en el AFD

print("\n🟢 Pruebas de aceptación en el AFD:")

for cadena in cadenas_prueba:
    if afd.acepta(cadena):
        print(f'✅ La cadena "{cadena}" es aceptada.')
    else:
        print(f'❌ La cadena "{cadena}" NO es aceptada.')