"""
Juego de conecta 4

El estado se va a representar como una lista de 42 elementos, tal que


0  1  2  3  4  5  6
7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31 32 33 34
35 36 37 38 39 40 41

y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del
jugador 1 y -1 es una ficha del jugador 2.

Las acciones son poner una ficha en una columna, que se representa como un
número de 0 a 6.

Un estado terminal es aquel en el que un jugador ha conectado 4 fichas
horizontales, verticales o diagonales, o ya no hay espacios para colocar
fichas.

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un
empate.

"""

from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from minimax import jugador_negamax
from minimax import minimax_iterativo

class Conecta4(ModeloJuegoZT2):
    def inicializa(self):
        return (tuple([0 for _ in range(6 * 7)]), 1)
        
    def jugadas_legales(self, s, j):
        return (columna for columna in range(7) if s[columna] == 0)
    
    def transicion(self, s, a, j):
        s = list(s[:])
        for i in range(5, -1, -1):
            if s[a + 7 * i] == 0:
                s[a + 7 * i] = j
                break
        return tuple(s)
    
    def ganancia(self, s):
        #Verticales
        for i in range(7):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
                    == s[i + 7 * (j + 2)] == s[i + 7 * (j + 3)] 
                    != 0):
                    return s[i + 7 * j]
        #Horizontales
        for i in range(6):
            for j in range(4):
                if (s[7 * i + j] == s[7 * i + j + 1] 
                    == s[7 * i + j + 2] == s[7 * i + j + 3] 
                    != 0):
                    return s[7 * i + j]
        #Diagonales
        for i in range(4):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * j + 8] 
                    == s[i + 7 * j + 16] == s[i + 7 * j + 24] 
                    != 0):
                    return s[i + 7 * j]
                if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
                    == s[i + 7 * j + 15] == s[i + 7 * j + 21] 
                    != 0):
                    return s[i + 7 * j + 3]
        return 0
    
    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0
    
def pprint_conecta4(s):
    a = [' X ' if x == 1 else ' O ' if x == -1 else '   ' 
         for x in s]
    print('\n 0 | 1 | 2 | 3 | 4 | 5 | 6')
    for i in range(6):
        print('|'.join(a[7 * i:7 * (i + 1)]))
        print('---+---+---+---+---+---+---')
    print('|'.join(a[42:49]))
    
def jugador_manual_conecta4(juego, s, j):
    pprint_conecta4(s)
    print("Jugador", " XO"[j])
    jugadas = list(juego.jugadas_legales(s, j))
    print("Jugadas legales:", jugadas)
    jugada = None
    while jugada not in jugadas:
        jugada = int(input("Jugada: "))
    return jugada

def ordena_centro(jugadas, jugador):
    """
    Ordena las jugadas de acuerdo a la distancia al centro
    """
    return sorted(jugadas, key=lambda x: abs(x - 4))

def ordena_extension(s, jugadas, jugador):
    """
    Ordena los movimientos basado en su potencial usando evalua_3con (Error)
    """
    juego = Conecta4()
    puntajes = []

    for movimiento in jugadas:
        estado_nuevo = juego.transicion(s, movimiento, jugador)

        if juego.ganancia(estado_nuevo) == jugador:
            puntaje = float('inf')
        else:
            eval_estado = [1 if x == jugador else -1 if x != 0 else 0 for x in estado_nuevo]
            puntaje = evalua_3con(eval_estado)

            central = [3, 2, 4, 1, 5, 0, 6]
            central_puntaje = 0.05 * (6 - central.index(movimiento))
            puntaje += central_puntaje
        
        if jugador == 2:
            puntaje = -puntaje
        
        puntajes.append((movimiento, puntaje))

    puntajes_desc = [movimiento for movimiento, puntaje in sorted(puntajes, key=lambda x: x[1], reverse=True)]
    return puntajes_desc

def ordenar_jugadas_avanzado(jugadas, jugador):
    """
    Ordena jugadas con una estrategia un poco mas avanzada
    """
    # Preferencias de columna básicas
    preferencia_columnas = {3: 10, 2: 8, 4: 8, 1: 6, 5: 6, 0: 4, 6: 4}
    
    if jugador == 1:
        preferencia_columnas = {3: 12, 2: 9, 4: 9, 1: 6, 5: 6, 0: 3, 6: 3}
    else:
        preferencia_columnas = {3: 10, 2: 9, 4: 9, 1: 7, 5: 7, 0: 5, 6: 5}
    
    # Ordenar jugadas por preferencia de columna (mayor a menor)
    jugadas_ordenadas = sorted(jugadas, key=lambda col: preferencia_columnas[col], reverse=True)
    
    return jugadas_ordenadas

def evalua_3con(s):
    """
    Evalua el estado s para el jugador 1
    """
    conect3 = sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == 1)
    ) - sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == -1)
    ) + sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == 1)
    ) - sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == -1)
    )
    promedio = conect3 / (7 * 4 + 6 * 5 + 5 * 4 + 5 * 4)
    if abs(promedio) >= 1:
        print("ERROR, evaluación fuera de rango --> ", promedio)
    return promedio

def evalua_nuevo(s):
    """
    Evalua el estado s para el jugador 1, considerando secuencias de 3 y 2
    """
    puntaje = 0
    
    # Secuencias de 3, vertical, horizontal y diagonal
    for i in range(4): 
        for j in range(7): 
            indice = i * 7 + j
            if s[indice] == s[indice + 7] == s[indice + 14] == 1:
                puntaje += 5
            elif s[indice] == s[indice + 7] == s[indice + 14] == -1:
                puntaje -= 5

    for i in range(6):
        for j in range(4):
            indice = i * 7 + j
            if s[indice] == s[indice + 1] == s[indice + 2] == 1:
                puntaje += 5
            elif s[indice] == s[indice + 1] == s[indice + 2] == -1:
                puntaje -= 5
    
    for i in range(3, 6):
        for j in range(4):
            indice = i * 7 + j
            if s[indice] == s[indice - 6] == s[indice - 12] == 1:
                puntaje += 5
            elif s[indice] == s[indice - 6] == s[indice - 12] == -1:
                puntaje -= 5

    for i in range(4):
        for j in range(5):
            indice = i * 7 + j
            if s[indice] == s[indice + 8] == s[indice + 16] == 1:
                puntaje += 5
            elif s[indice] == s[indice + 8] == s[indice + 16] == -1:
                puntaje -= 5
                
    # Secuencias de 2, vertical, horizontal y diagonal
    for i in range(5):  
        for j in range(7):
            indice = i * 7 + j
            if s[indice] == s[indice + 7] == 1:
                puntaje += 1
            elif s[indice] == s[indice + 7] == -1:
                puntaje -= 1

    for i in range(6):  
        for j in range(5):
            indice = i * 7 + j
            if s[indice] == s[indice + 1] == 1:
                puntaje += 1
            elif s[indice] == s[indice + 1] == -1:
                puntaje -= 1
    
    for i in range(4,6):
        for j in range(5):
            indice = i * 7 + j
            if s[indice] == s[indice - 6] == 1:
                puntaje += 1
            elif s[indice] == s[indice - 6] == -1:
                puntaje -= 1

    for i in range(4):
        for j in range(5):
            indice = i * 7 + j
            if s[indice] == s[indice + 8] == 1:
                puntaje += 1
            elif s[indice] == s[indice + 8] == -1:
                puntaje -= 1

    return puntaje
    
if __name__ == '__main__':

    modelo = Conecta4()
    print("="*40 + "\n" + "EL JUEGO DE CONECTA 4".center(40) + "\n" + "="*40)
    
    jugs = []
    for j in [1, -1]:
        print(f"Selección de jugadores para las {' XO'[j]}:")
        sel = 0
        print("   1. Jugador manual")
        print("   2. Jugador negamax limitado en profundidad")
        print("   3. Jugador negamax limitado en tiempo")
        while sel not in [1, 2, 3]:
            sel = int(input(f"Jugador para las {' XO'[j]}: "))
    
        if sel == 1:
            jugs.append(jugador_manual_conecta4)
        elif sel == 2:
            d = None
            while type(d) != int or d < 1:
                d = int(input("Profundidad: "))
            jugs.append(lambda juego, s, j: jugador_negamax(
                juego, s, j, ordena=ordenar_jugadas_avanzado, evalua=evalua_nuevo, d=d)
            )
        else:
            t = None
            while type(t) != int or t < 1:
                t = int(input("Tiempo: "))
            jugs.append(lambda juego, s, j: minimax_iterativo(
                juego, s, j, ordena=ordenar_jugadas_avanzado, evalua=evalua_nuevo, tiempo=t)
            )
        
    g, s_final = juega_dos_jugadores(modelo, jugs[0], jugs[1])
    print("\nSE ACABO EL JUEGO\n")
    pprint_conecta4(s_final)
    if g != 0:
        print("Gana el jugador " + " XO"[g])
    else:
        print("Empate")
    
    
