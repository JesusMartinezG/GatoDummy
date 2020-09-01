import random
import time

class Gato:

    def __init__(self, siz): # Crea el tablero con el tamaño indicado
        self.tiempoInicio = time.time()
        self.tam = siz
        self.tablero = [[0 for x in range(siz)] for y in range(siz)]  # Crea un tablero de tam x tam lleno de ceros
        self.turno = 0

    def cambiarTurno(self): # Cambia entre los jugadores ( solo dos para este caso )
        if self.turno == 1:
            self.turno = 2
        else:
            self.turno = 1

    def tirar(self, jg, coord): # Plasma el simbolo del jugador indicado en las coordeneadas ingresadas
        if self.tablero[coord[0]][coord[1]] == 0: # Que la casilla esté vacía
            self.tablero[coord[0]][coord[1]] = jg # Pone el simbolo
            return self.win(jg)  # Revisa la condición ganar
        else:
            return -1  # Retorna -1 cuando la casilla ya está ocupada

    def imprimir(self):
        for x in range(self.tam):
            for y in range(self.tam):
                print("%i \t" % self.tablero[x][y], end="", flush=True)
            print("\n")

    def win(self, jg): # Evalúa si el jugador indicado ha ganado
        winner = False

        for x in range(self.tam):
            aux = True
            for y in range(self.tam):
                aux = aux and (self.tablero[x][y] == jg)  # Es linea vertical
            winner = winner or aux

        if winner:
            self.tiempoFin = time.time()
            return jg

        for y in range(self.tam):
            aux = True
            for x in range(self.tam):
                aux = aux and (self.tablero[x][y] == jg)  # Es linea horizontal
            winner = winner or aux

        if winner:
            self.tiempoFin = time.time()
            return jg

        aux = True
        for x in range(self.tam):
            aux = aux and (self.tablero[x][x] == jg)  # Es Diagonal \

        if aux:
            self.tiempoFin = time.time()
            return jg

        aux = True
        for x in range(self.tam):
            aux = aux and (self.tablero[x][self.tam - 1 - x] == jg)  # es diagonal /

        if aux:
            self.tiempoFin = time.time()
            return jg

        return 0

    def validar(self, arr): # Revisa que las coordenadas introducidas sean validas para el tamaño del tablero
        return arr[0] < 0 or arr[1] < 0 or arr[0] >= self.tam or arr[1] >= self.tam

def cambiarjugador(jg):
    if jg == 1:
        return 2
    else:
        return 1


def decode(cadena): # Para obtener las coordenadas introducidas
    aux = cadena.split(',')
    if len(aux) is 2:
        aux = [int(x) for x in aux]  # convierte la cadena en un arreglo de enteros
    else:
        aux = []
    return aux

def main():
    print("Juego de Gato\n Seleccione la dificultad:\n1) 3x3\n2) 5x5")

    tam = int(input()) # Ingresar la dificultad

    if tam == 2:
        tam = 5
    else:
        tam = 3

    # Crear una instancia del juego de gato
    juego = Gato(tam)
    jugador = 1 #random.randint(1, 2)
    noWin = True

    while noWin: # Ciclo de intercambio de tiros
        novalido = True
        while novalido:
            print("Turno del jugador %i" % jugador)
            x = input()
            tiro = decode(x)
            if len(tiro) == 2:
                novalido = juego.validar(tiro)
            else:
                novalido = True

        noWin = not (juego.tirar(jugador, tiro) == jugador)
        jugador = cambiarjugador(jugador)
        juego.imprimir()
    print('Duración del juego: {:.2f}'.format(juego.tiempoFin - juego.tiempoInicio) + ' segundos' )

if __name__ == '__main__':
    main()
