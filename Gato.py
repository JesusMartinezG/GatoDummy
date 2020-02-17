import random


class Gato:
    tablero = None
    turno = 0

    def __init__(self, siz):
        self.tam = siz
        self.tablero = [[0 for x in range(siz)] for y in range(siz)]  # Crea un tablero de tam x tam lleno de ceros

    def tirar(self, jg, coord):
        if self.tablero[coord[0]][coord[1]] == 0:
            self.tablero[coord[0]][coord[1]] = jg
            return self.win(jg)  # Retorna el numero del jugador si es que gana con su tiro, si no retorna 0
        else:
            return -1  # Retorna -1 cuando el tiro no es válido

    def imprimir(self):
        for x in range(self.tam):
            for y in range(self.tam):
                print("%i \t" % self.tablero[x][y], end="", flush=True)
            print("\n")

    def win(self, jg):
        winner = False

        for x in range(self.tam):
            aux = True
            for y in range(self.tam):
                aux = aux and (self.tablero[x][y] == jg)  # Es linea vertical
            winner = winner or aux

        if winner:
            return jg

        for y in range(self.tam):
            aux = True
            for x in range(self.tam):
                aux = aux and (self.tablero[x][y] == jg)  # Es linea horizontal
            winner = winner or aux

        if winner:
            return jg

        aux = True
        for x in range(self.tam):
            aux = aux and (self.tablero[x][x] == jg)  # Es Diagonal \

        if aux:
            return jg

        aux = True
        for x in range(self.tam):
            aux = aux and (self.tablero[x][self.tam - 1 - x] == jg)  # es diagonal /

        if aux:
            return jg

        return 0

    def validar(self, arr):
        return arr[0] < 0 or arr[1] < 0 or arr[0] >= self.tam or arr[1] >= self.tam


def cambiarjugador(jg):
    if jg == 1:
        return 2
    else:
        return 1


def decode(cadena):
    aux = cadena.split(',')
    if len(aux) is 2:
        aux = [int(x) for x in aux]  # convierte la cadena en un arreglo de enteros
    else:
        aux = []
    return aux


print("Juego de Gato\n Seleccione la dificultad:\n1) 3x3\n2) 5x5")

tam = int(input())

if tam == 2:
    tam = 5
else:
    tam = 3

juego = Gato(tam)
jugador = random.randint(1, 2)
noWin = True

while noWin:
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
