import time
import socket
import sys
import random


class Gato:

    def __init__(self, siz):  # Crea el tablero con el tamaño indicado
        self.tiempoInicio = time.time()
        self.tam = siz
        self.tablero = [[0 for x in range(siz)] for y in range(siz)]  # Crea un tablero de tam x tam lleno de ceros
        self.turno = 1  # Jugador 1 siempre tira primero

    def cambiarTurno(self):  # Cambia entre los jugadores ( solo dos para este caso )
        if self.turno == 1:
            self.turno = 2
        else:
            self.turno = 1

    def tirar(self, jg, coord):  # Plasma el simbolo del jugador indicado en las coordeneadas ingresadas
        self.tablero[coord[0]][coord[1]] = jg  # Pone el simbolo
        return self.win(jg)  # Revisa la condición ganar

    def imprimir(self):
        for x in range(self.tam):
            for y in range(self.tam):
                print("%i \t" % self.tablero[x][y], end="", flush=True)
            print("\n")

    def win(self, jg):  # Evalúa si el jugador indicado ha ganado
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

    def validar(self, arr):  # Revisa que las coordenadas introducidas sean validas para el tamaño del tablero
        aux = not (arr[0] < 0 or arr[1] < 0 or arr[0] >= self.tam or arr[
            1] >= self.tam)  # Que las coordenadas existan en el tablero
        if aux:
            return aux and (self.tablero[arr[0]][arr[1]] == 0)  # Que la casilla esté vacía
        else:
            return aux

    def cpu(self):
        coord = (random.randint(0, self.tam - 1), random.randint(0, self.tam - 1))
        while not self.validar(coord):
            coord = (random.randint(0, self.tam - 1), random.randint(0, self.tam - 1))
        return coord


def recibir(sock, buffsize):
    return sock.recv(buffsize).decode("utf-8")


def enviar(sock, cadena):
    cadena = str(cadena).encode()
    sock.sendall(cadena)


def coordenadas(recibido):
    part = recibido.split(',')
    part = [int(c) for c in part]
    return part


def main():
    ip = None
    puerto = None

    if len(sys.argv) != 3:  # Si no hay argumentos asigna la direccion local
        ip, puerto = ('127.0.0.1', '12345')
    else:
        ip, puerto = sys.argv[1:3]  # Recupera los argumentos de ejecución

    dirServidor = (ip, int(puerto))

    # Crea el socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SocketServidor:
        SocketServidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SocketServidor.bind(dirServidor)
        SocketServidor.listen(1)
        print("El servidor TCP está disponible y en espera de solicitudes")
        # Recibe conexion

        client_conn, client_addr = SocketServidor.accept()  # Aceptar al cliente
        print("Conectado a", client_addr)

        with client_conn:
            tam = int(recibir(client_conn, 512))  # Recibe dificultad
            juego = Gato(tam)  # Crea juego
            print('Juego creado tablero {}x{}'.format(tam,tam))
            enviar(client_conn, '-2')  # Indica el inicio del juego

            continuar = True

            while continuar:  # Recibe y envía tiros
                if juego.turno == 1:  # Turno del cliente
                    print('Turno del cliente')
                    r = recibir(client_conn, 512)  # Recibe la cadena con las coordenadas que envió el cliente
                    print('Recibido: ' + r)
                    coord = coordenadas(r)  # convierte la cadena a una tupla de enteros

                    if juego.validar(coord):  # La cadena es valida
                        print('Coordenadas validas')
                        juego.tirar(1, coord)  # Realiza el tiro en el tablero
                        print('Tiro registrado')
                        if juego.win(1):  # Revisa si el jugador gana
                            print('cliente gana')
                            continuar = False
                            enviar(client_conn, '2')
                            break
                        enviar(client_conn, '1,1,' + ','.join(str(x) for x in coord))
                        juego.cambiarTurno()  # Cambia el turno
                    else:
                        print('Coordenadas no validas')
                        enviar(client_conn, '-1')
                else:  # Turno del cpu
                    print('Turno del cpu')
                    coord = juego.cpu()  # Obtiene un tiro aleatorio válido
                    tiro = '1,2,' + ','.join(str(x) for x in coord)  # Crea la cadena de respuesta
                    juego.tirar(2, coord)  # Actualiza el tablero
                    if juego.win(2):  # Revisa si el cpu gana
                        print('cpu gana')
                        continuar = False
                        enviar(client_conn, '3')
                        break
                    enviar(client_conn, tiro)  # Envía la raspuesta
                    juego.cambiarTurno()  # Cambia el turno

            enviar(client_conn, '{:.2f}'.format(juego.tiempoFin - juego.tiempoInicio))  # Envía duración del juego


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
