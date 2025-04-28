
# Ejercicio 3 - Punto 2: Definición del AFN

class AFN:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion

    def mover(self, estados, simbolo):
        resultado = set()
        for estado in estados:
            if estado in self.transiciones and simbolo in self.transiciones[estado]:
                resultado.update(self.transiciones[estado][simbolo])
        return resultado

    def epsilon_clausura(self, estados):
        pila = list(estados)
        clausura = set(estados)
        while pila:
            estado = pila.pop()
            if estado in self.transiciones and 'ε' in self.transiciones[estado]:
                for e in self.transiciones[estado]['ε']:
                    if e not in clausura:
                        clausura.add(e)
                        pila.append(e)
        return clausura

# Definimos el AFN
estados_afn = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}
alfabeto_afn = {'a', 'b'}
transiciones_afn = {
    '0': {'ε': {'1'}},
    '1': {'ε': {'2', '3', '6'}},
    '2': {'a': {'4'}},
    '4': {'ε': {'6'}},
    '3': {'b': {'5'}},
    '5': {'ε': {'6'}},
    '6': {'ε': {'1', '7'}},
    '7': {'a': {'8'}, 'b': {'9'}, 'ε': {'10'}},
    '8': {'ε': {'10'}},
    '9': {'ε': {'10'}},
}
estado_inicial_afn = '0'
estados_aceptacion_afn = {'10'}

afn = AFN(estados_afn, alfabeto_afn, transiciones_afn, estado_inicial_afn, estados_aceptacion_afn)

# Probar aceptación en el AFN

def acepta_afn(afn, cadena):
    estados_actuales = afn.epsilon_clausura({afn.estado_inicial})
    for simbolo in cadena:
        estados_actuales = afn.epsilon_clausura(afn.mover(estados_actuales, simbolo))
    return bool(estados_actuales & afn.estados_aceptacion)

print("\n🔵 Pruebas de aceptación en el AFN:")

cadenas_prueba = ['a', 'b', '', 'ab', 'ba', 'aba', 'bb', 'aab', 'aabbababab', 'ad', 'abdbb', 'aaaa', 'bbbb']

for cadena in cadenas_prueba:
    if acepta_afn(afn, cadena):
        print(f'✅ La cadena "{cadena}" es aceptada.')
    else:
        print(f'❌ La cadena "{cadena}" NO es aceptada.')

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

# Probar aceptación en el AFD

print("\n🟢 Pruebas de aceptación en el AFD:")

for cadena in cadenas_prueba:
    if afd.acepta(cadena):
        print(f'✅ La cadena "{cadena}" es aceptada.')
    else:
        print(f'❌ La cadena "{cadena}" NO es aceptada.')
