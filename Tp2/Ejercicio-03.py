
#! Ejercicio 3 punto 2

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
estados = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}
alfabeto = {'a', 'b'}
transiciones = {
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
estado_inicial = '0'
estados_aceptacion = {'10'}

afn = AFN(estados, alfabeto, transiciones, estado_inicial, estados_aceptacion)


#! Ejercicio 3 punto 4


