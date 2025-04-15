"""
El juego del super gato

"""

from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from juegos_simplificado import minimax
from minimax import jugador_negamax

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
        nuevo_tablero = list(nuevo_tableros[b])

        nuevo_tablero[i] = j
        nuevo_tableros[b] = tuple(nuevo_tablero)

        sig_activo = b

        if self.victoria(nuevo_tableros[sig_activo]) != 0 or all(cell !=0 for cell in nuevo_tableros[sig_activo]):
            sig_activo = -1

        sig_jug = -j

        return(tuple(nuevo_tableros), sig_jug, sig_activo)
    
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

def jugar(juego):
    juegos = juego()
    estado = juegos.inicializa()

    while not juegos.terminal(estado):
        pprint_uttt(estado)
        tableros, j, t = estado
        jugadas = juegos.jugadas_legales(estado, j)

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
                print("Formato igual de invalido que Stephen Hawkin. Formato Correcto: tablero, posicion (ejemplo: 4,2)")
        
        estado = juegos.transicion(estado, (b, c), j)
    
    pprint_uttt(estado)
    print("GAME OVER!")

    resultado = juegos.ganancia(estado)
    if resultado == 1:
        print("GANO LA X!")
    elif resultado == -1:
        print("GANO LA O!")
    else:
        print("NO GANO NADIE!!! REVANCHA O QUE?")

if __name__ == '__main__':
    jugar(UltimateTTT)
