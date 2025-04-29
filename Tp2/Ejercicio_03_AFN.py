# Ejercicio 3 - Punto 2: Definición del AFN
    
class AFN:
    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion

    def epsilon_cerradura(self, estados):
        pila = list(estados)
        clausura = set(estados)
        while pila:
            actual = pila.pop()
            if actual in self.transiciones and 'ε' in self.transiciones[actual]:
                for destino in self.transiciones[actual]['ε']:
                    if destino not in clausura:
                        clausura.add(destino)
                        pila.append(destino)
        return clausura

    def transitar(self, estados, simbolo):
        nuevos = set()
        for estado in estados:
            if estado in self.transiciones and simbolo in self.transiciones[estado]:
                nuevos.update(self.transiciones[estado][simbolo])
        return nuevos

    def acepta(self, cadena):
        estados_actuales = self.epsilon_cerradura({self.estado_inicial})
        
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False
            estados_actuales = self.transitar(estados_actuales, simbolo)
            estados_actuales = self.epsilon_cerradura(estados_actuales)

        return bool(estados_actuales & self.estados_aceptacion)

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
estados_aceptacion_afn = {'8', '9', '10'}

afn = AFN(estados_afn, alfabeto_afn, transiciones_afn, estado_inicial_afn, estados_aceptacion_afn)


print("\n🔵 Pruebas de aceptación en el AFN:")

cadenas_prueba = ['a', 'b', '', 'ab', 'ba', 'aba', 'bb', 'aab', 'aabbababab', 'ad', 'abdbb', 'aaaa', 'bbbb']

for cadena in cadenas_prueba:
    if afn.acepta(cadena):
        print(f'✅ La cadena "{cadena}" es aceptada.')
    else:
        print(f'❌ La cadena "{cadena}" NO es aceptada.')