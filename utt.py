"""
Juego del super gato (Ultimate TicTacToe)

El estado se va a representar como una tupla de 9 elementos, un entero, otro entero.
Los elementos dentro de la tupla son otras 9 tuplas de 9 enteros, que indican los 81 espacios 
del super gato. Tal:

(0,0) (0, 1) (0, 2)||(1,0) (1, 1) (1, 2)||(2,0) (2, 1) (2, 2)
(0,3) (0, 4) (0, 5)||(1,3) (1, 4) (1, 5)||(2,3) (2, 4) (2, 5)
(0,6) (0, 7) (0, 8)||(1,6) (1, 7) (1, 8)||(2,6) (2, 7) (2, 8)
===================||===================||===================
(3,0) (3, 1) (3, 2)||(4,0) (4, 1) (4, 2)||(5,0) (5, 1) (5, 2)
(3,3) (3, 4) (3, 5)||(4,3) (4, 4) (4, 5)||(5,3) (5, 4) (5, 5)
(3,6) (3, 7) (3, 8)||(4,6) (4, 7) (4, 8)||(5,6) (5, 7) (5, 8)
===================||===================||===================
(6,0) (6, 1) (6, 2)||(7,0) (7, 1) (7, 2)||(8,0) (8, 1) (8, 2)
(6,3) (6, 4) (6, 5)||(7,3) (7, 4) (7, 5)||(8,3) (8, 4) (8, 5)
(6,6) (6, 7) (6, 8)||(7,6) (7, 7) (7, 8)||(8,6) (8, 7) (8, 8)

y cada entero puede ser 0, 1 o -1, donde 0 es vacío, 1 es una X del
jugador 1 y -1 es una O del jugador 2. El ultimo entero (0-8) del estado distingue el tablero en que se tiene 
que jugar dependiendo de la posicion elegida por el oponente o -1 si se puede jugar en cualquier tablero.

Las acciones son poner una X si eres el jugador 1 o una O si eres el jugador 2, en una posicion abierta de las 9 
posiciones que tiene un tablero normal del gato, en el tablero del gato que sea determinado por el numero en el 
estado (0-8) o cualquiera si el valor es -1

Un estado terminal es aquel en el que un jugador ha ganado 3 tableros del gato de forma
horizontal, vertical o diagonal, o ya no hay espacios para colocar
X u O.

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un ASQUEROSO
empate.

"""

from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from juegos_simplificado import minimax
from minimax import jugador_negamax
from minimax import minimax_iterativo

class UltimateTTT(ModeloJuegoZT2):
    """
    El juego del super gato (Ultimate TicTacToe) 
    
    """
    def inicializa(self):
        """
        Inicializa el estado inicial del juego, el jugador
        que comienza y que se pueda jugar en cualquier tablero
        
        """
        return (tuple([tuple([0]*9) for _ in range(9)]), 1, -1)
    
    def jugadas_legales(self, s, j):
        """
        Devuelve una lista con las jugadas legales para el jugador j
        en el estado s
        
        """
        tableros, j, t = s

        jugadas = []
        def tablero_ganado(tablero):
            return self.victoria(tablero) != 0 or all(cell != 0 for cell in tablero)

        if t == -1 or tablero_ganado(tableros[t]):
            for b in range(9):
                if tablero_ganado(tableros[b]):
                    continue
                for i in range(9):
                    if tableros[b][i] == 0:
                        jugadas.append((b, i))
        else:
            for i in range(9):
                if tableros[t][i] == 0:
                    jugadas.append((t, i))
        
        return jugadas
           
    
    def transicion(self, s, a, j):
        """
        Devuelve el estado que resulta de realizar la jugada a en el estado s
        para el jugador j
        
        """
        tableros, _, _ = s
        b, i = a

        nuevo_tableros = [list(tablero) for tablero in tableros]
        nuevo_tablero = nuevo_tableros[b]

        nuevo_tablero[i] = j

        sig_activo = i

        if self.victoria(nuevo_tableros[sig_activo]) != 0 or all(cell !=0 for cell in nuevo_tableros[sig_activo]):
            sig_activo = -1

        sig_jug = -j

        nuevo_tableros = tuple(tuple(tablero) for tablero in nuevo_tableros)

        return(nuevo_tableros, sig_jug, sig_activo)
    
    def terminal(self, s):
        """
        Devuelve True si es terminal el estado actual,
        
        """
        tableros, j, t = s

        completo_tablero = [self.victoria(tablero) for tablero in tableros]

        if self.victoria(completo_tablero) != 0:
            return True
        
        for tablero in tableros:
            if self.victoria(tablero) == 0 and any(cell == 0 for cell in tablero):
                return False

        return True
    
    def ganancia(self, s):
        """
        Devuelve la ganancia para el jugador 1 en el estado terminal s
        
        """
        if not self.terminal(s):
            raise ValueError("No usar a menos que el juego este terminado")
    
        tableros, j, t = s

        completo_tablero = [self.victoria(tablero) for tablero in tableros]

        resultado = self.victoria(completo_tablero)

        return resultado

    def victoria(self, tablero):
        """
        Funcion auxiliar para checar el tablero, regresa el jugador que lo gano o 0 si aun no hay
        
        """
        if not isinstance(tablero, (list, tuple)) or len(tablero) != 9:
            raise ValueError(f"Tablero 3x3, no {tablero}")

        for i in range(3):
            if tablero[3*i] != 0 and tablero[3*i] == tablero[3*i+1] == tablero[3*i+2]:
                return tablero[3*i]
            
        for i in range(3):
            if tablero[i] != 0 and tablero[i] == tablero[i+3] == tablero[i+6]:
                return tablero[i]
        
        if tablero[0] != 0 and tablero[0] == tablero[4] == tablero[8]:
            return tablero[0]
        if tablero[2] != 0 and tablero[2] == tablero[4] == tablero[6]:
            return tablero[2]
        
        return 0
    
    def congela(self, estado):
        # Problemas con estado con lista
        return congela_estado(estado)

def pprint_uttt(s):
    """
    Imprime el estado del juego del super gato

    """
    tableros, j, t = s

    simbologia = {1: 'X', -1: 'O', 0: ' '}

    def formato_tablero(b):
        return [simbologia[b[i]] for i in range(9)]
    
    formato = [formato_tablero(tablero) for tablero in tableros]

    print("\n=== ULTIMATE TIC TAC TOE (Super Gato) ===")
    for renglon in range(3):
        for linea in range(3):
            renglon_str = ""
            for col in range(3):
                indice_tablero = renglon * 3 + col
                tablero = formato[indice_tablero]
                renglon_str += f" {tablero[linea*3]} | {tablero[linea*3+1]} | {tablero[linea*3+2]} "
                if col < 2:
                    renglon_str += "||"
            print(renglon_str)
        if renglon < 2:
            print("===================================")
    print(f"\nJugador que mueve: {'X' if j == 1 else 'O'}")
    print(f"Tablero activo: {t if t != -1 else 'Cualquiera'}\n")

def checar_victoria(tablero):
    """
    Funcion auxiliar para checar el tablero, regresa el jugador que lo gano o 0 si aun no hay
    
    """
    if not isinstance(tablero, (list, tuple)) or len(tablero) != 9:
        raise ValueError(f"Tablero 3x3, no {tablero}")

    for i in range(3):
        if tablero[3*i] != 0 and tablero[3*i] == tablero[3*i+1] == tablero[3*i+2]:
            return tablero[3*i]
            
    for i in range(3):
        if tablero[i] != 0 and tablero[i] == tablero[i+3] == tablero[i+6]:
            return tablero[i]
        
    if tablero[0] != 0 and tablero[0] == tablero[4] == tablero[8]:
        return tablero[0]
    if tablero[2] != 0 and tablero[2] == tablero[4] == tablero[6]:
        return tablero[2]
        
    return 0

def ordena_centro(jugadas, jugador):
    """
    Ordena las jugadas de acuerdo a la distancia al centro del tablero general y del tablero en el que se esta
    """
    return sorted(jugadas, key=lambda x: abs(x[0] - 4) + abs(x[1] - 4))

def simple_evalua_uttt(s):
    """
    Evalua el estado s para el jugador de forma simple
    """
    tableros, j, t = s
    opt = -j
    puntaje = 0

    def eval_tab(tablero):
        val = 0
        lineas = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for linea in lineas:
            # Da valor a tener dos posiciones en un mini tablero
            valores = [tablero[i] for i in linea]
            if valores.count(j) == 2 and valores.count(0) == 1:
                val += 1
            elif valores.count(opt) == 2 and valores.count(0) == 1:
                val -= 1
        return val

    # Resultado del tablero grande checando los tableros mini
    meta_tab = [checar_victoria(b) for b in tableros]

    for tablero in tableros:
        result = checar_victoria(tablero)
        if result == j:
            puntaje += 5
        elif result == opt:
            puntaje -= 5
        else:
            puntaje += eval_tab(tablero)

        # Center control - Valor a tener el centro en un minitablero
        if tablero[4] == j:
            puntaje += 0.5
        elif tablero[4] == opt:
            puntaje -= 0.5

    meta_resultado = checar_victoria(meta_tab)
    if meta_resultado == j:
        puntaje += 1000
    elif meta_resultado == opt:
        puntaje -= 1000

    # Center meta indice - Valor a tener el centro del meta tablero
    if meta_tab[4] == j:
        puntaje += 1
    elif meta_tab[4] == opt:
        puntaje -= 1
    return puntaje

def jugador_manual_uttt(juego, s, j):
    pprint_uttt(s)
    jugadas = juego.jugadas_legales(s, j)
    print("Jugadas legales:", jugadas)

    def movimiento_valido():
        try:
            movimiento = input("Que vas a jugar? (ej. (4,4)): ")
            b, c = map(int, movimiento.strip().split(","))

            if (b, c) in jugadas:
                return (b, c)
            else:
                print(f"Movimiento ({b}, {c}) no es legal. Intenta de nuevo o seras arrestado.")
                return movimiento_valido()
        except ValueError:
            print("Formato igual de invalido que Stephen Hawking. Formato Correcto: tablero, posicion (ejemplo: 4,2)")
            return movimiento_valido()

    return movimiento_valido()

def jugare(juego):
    """
    Jugador con elecciones manual, a profundidad y por tiempo

    """
    modelo = juego()

    print("=" * 40 + "\n" + "ULTIMATE TIC TAC TOE".center(40) + "\n" + "=" * 40)

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
            jugs.append(jugador_manual_uttt)
        elif sel == 2:
            d = None
            while type(d) != int or d < 1:
                d = int(input("Profundidad: "))
            jugs.append(lambda juegos, s, j: jugador_negamax(
                juegos, juegos.congela(s), j, ordena=ordena_centro, evalua=simple_evalua_uttt, d=d)
            )
        else:
            t = None
            while type(t) != int or t < 1:
                t = int(input("Tiempo: "))
            jugs.append(lambda juegos, s, j: minimax_iterativo(
                juegos, juegos.congela(s), j, ordena=ordena_centro, evalua=simple_evalua_uttt, tiempo=t)
            )

    g, s_final = juega_dos_jugadores(modelo, jugs[0], jugs[1])
    pprint_uttt(s_final)
    print("GAME OVER!")

    resultado = g
    if resultado == 1:
        print("GANO LA X!")
    elif resultado == -1:
        print("GANO LA O!")
    else:
        print("EMPATE! REVANCHA O QUE?")

def jugar(juego):
    """
    Jugador completamente manual

    """
    modelo = juego()
    estado = modelo.inicializa()

    while not modelo.terminal(estado):
        pprint_uttt(estado)
        tableros, j, t = estado
        jugadas = modelo.jugadas_legales(estado, j)

        print("Jugadas legales:", jugadas)

        while True:
            try:
                movimiento = input("Que vas a jugar? (tablero (0-9), posicion(0-9)): ")
                b, c = map(int, movimiento.strip().split(","))
                if (b, c) in jugadas:
                    break
                else:
                    print("Jugada Ilegal. Intenta de nuevo o seras arrestado...")
            except:
                print("Formato igual de invalido que Stephen Hawking. Formato Correcto: tablero, posicion (ejemplo: 4,2)")
        
        estado = modelo.transicion(estado, (b, c), j)
    
    pprint_uttt(estado)
    print("GAME OVER!")

    resultado = modelo.ganancia(estado)
    if resultado == 1:
        print("GANO LA X!")
    elif resultado == -1:
        print("GANO LA O!")
    else:
        print("EMPATE! REVANCHA O QUE?")

def jugador_minimax_uttt(juego, s, j):
    """
    Jugador minimax para el juego del super gato

    """
    return minimax(juego, s, j)

def juega_dos_jugadores(juego, jugador1, jugador2):
    """
    Juega un juego de dos jugadores, editado del original para poder utilizar un estado diferente
    
    juego: instancia de ModeloJuegoZT
    jugador1: función que recibe el estado y devuelve la jugada
    jugador2: función que recibe el estado y devuelve la jugada
    
    """
    s = juego.inicializa()
    # Falta probar despues de cambiar las transiciones
    s = juego.congela(s)
    while not juego.terminal(s):
        _, j, _ = s
        a = jugador1(juego, s, j) if j == 1 else jugador2(juego, s, j)
        s = juego.transicion(s, a, j)
        s = juego.congela(s)
        j = -j
    return juego.ganancia(s), s

def congela_estado(estado):
    tableros, j, t = estado
    # Convirtiendo a hashable por problemas con negamax
    # Falta probar si funciona sin esto otra vez
    tableros_congelados = tuple(
        tuple(tuple(row) if isinstance(row, list) else row for row in tablero)
        if isinstance(tablero, list) else tablero
        for tablero in tableros
    )

    t_congelado = tuple(t) if isinstance(t, list) else t
    return (tableros_congelados, j, t_congelado)

if __name__ == '__main__':
    jugare(UltimateTTT)
