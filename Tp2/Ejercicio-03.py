
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

# Definición del AFN para (a|b)*(a|b|ε)
estados = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
alfabeto = {'a', 'b'}
transiciones = {
    '0': {'ε': {'1'}},
    '1': {'ε': {'2', '4', '7'}},
    '2': {'a': {'3'}},
    '3': {'ε': {'6'}},
    '4': {'b': {'5'}},
    '5': {'ε': {'6'}},
    '6': {'ε': {'1'}},
    '7': {'a': {'8'}},
    '8': {'ε': {'9'}},
    '7': {'b': {'8'}},  # también se puede pasar a 'b'
    '7': {'ε': {'9'}},  # también epsilon
}
estado_inicial = '0'
estados_aceptacion = {'9'}

afn = AFN(estados, alfabeto, transiciones, estado_inicial, estados_aceptacion)


#! Ejercicio 3 punto 3


class AFD:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transiciones = dict()
        self.estado_inicial = None
        self.estados_aceptacion = set()

def convertir_afn_a_afd(afn):
    afd = AFD()
    afd.alfabeto = afn.alfabeto

    inicial = frozenset(afn.epsilon_clausura({afn.estado_inicial}))
    afd.estado_inicial = inicial
    estados_sin_procesar = [inicial]
    afd.estados.add(inicial)

    while estados_sin_procesar:
        actual = estados_sin_procesar.pop()
        for simbolo in afd.alfabeto:
            mov = afn.mover(actual, simbolo)
            clausura = afn.epsilon_clausura(mov)
            if not clausura:
                continue
            clausura_frozen = frozenset(clausura)
            if clausura_frozen not in afd.estados:
                afd.estados.add(clausura_frozen)
                estados_sin_procesar.append(clausura_frozen)
            if actual not in afd.transiciones:
                afd.transiciones[actual] = dict()
            afd.transiciones[actual][simbolo] = clausura_frozen

    for estado in afd.estados:
        if any(e in afn.estados_aceptacion for e in estado):
            afd.estados_aceptacion.add(estado)

    return afd

afd = convertir_afn_a_afd(afn)


#! Ejercicio 3 punto 4


class AFD_Simulador:
    def __init__(self, afd):
        self.estados = afd.estados
        self.alfabeto = afd.alfabeto
        self.transiciones = afd.transiciones
        self.estado_inicial = afd.estado_inicial
        self.estados_aceptacion = afd.estados_aceptacion

    def acepta(self, cadena):
        estado_actual = self.estado_inicial
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False
            if simbolo not in self.transiciones.get(estado_actual, {}):
                return False
            estado_actual = self.transiciones[estado_actual][simbolo]
        return estado_actual in self.estados_aceptacion

simulador_afd = AFD_Simulador(afd)

# Probar
cadenas = ['a', 'b', '', 'ab', 'ba', 'aba', 'bb', 'aab', 'aabbababab', 'ad', 'abdbb']
for cadena in cadenas:
    if simulador_afd.acepta(cadena):
        print(f'La cadena "{cadena}" es aceptada.')
    else:
        print(f'La cadena "{cadena}" NO es aceptada.')
