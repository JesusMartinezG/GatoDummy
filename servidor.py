import time
import socket
import sys
import random


class Gato:

    def __init__(self, siz):                                            # Crea el tablero con el tamaño indicado
        self.tiempoInicio = time.time()                                 # Registra el tiempo de creación del juego
        self.tiempoFin = None
        self.tam = siz
        self.tablero = [[' ' for x in range(siz)] for y in range(siz)]  # Crea un tablero de tam x tam lleno de espacios
        self.turno = 0                                                  # Jugador 1 siempre tira primero
        self.numTiros = 0                                               # Cuenta los tiros realizados, sirve para detectar un empate
        self.tiros_maximos = siz*siz                                    # Numero de casillas = numero de tiros posibles
        self.simbolos = ['x', 'o']                                      # Simbolos de los jugadores en orden según su turno
        self.numJugadores = 2

    def cambiarTurno(self):  # Cambia entre los turnos
        if self.turno < self.numJugadores:
            self.turno+=1
        else:
            self.turno = 0

    def tirar(self, jg, coord):                             # Plasma el simbolo del jugador indicado en las coordeneadas ingresadas
        self.tablero[coord[0]][coord[1]] = jg               # Pone el simbolo en el tablero
        self.numTiros += 1                                  # Cuenta el tiro realizado
        pog = self.win(jg)                                  # Revisa la condición ganar
        if pog:                                             # Se forma una linea -> Gana el juego
            return '1'+jg                                   # Retorna el simbolo del jugador ganador y el digito de control que lo indica
        else:
            if self.numTiros == self.tiros_maximos:         # Si ya no hay más casillas que llenar
                return '1/'                                 # Empate
            else:
                self.cambiarTurno()                         # Solo si el juego continua se cambia el turno y no hubo errores
                return '0'+self.simbolos[self.turno]        # Sigue jugando

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
            return True

        for y in range(self.tam):
            aux = True
            for x in range(self.tam):
                aux = aux and (self.tablero[x][y] == jg)  # Es linea horizontal
            winner = winner or aux

        if winner:
            self.tiempoFin = time.time()
            return True

        aux = True
        for x in range(self.tam):
            aux = aux and (self.tablero[x][x] == jg)  # Es Diagonal \

        if aux:
            self.tiempoFin = time.time()
            return True

        aux = True
        for x in range(self.tam):
            aux = aux and (self.tablero[x][self.tam - 1 - x] == jg)  # es diagonal /

        if aux:
            self.tiempoFin = time.time()
            return True

        return False # No forma ninguna linea

    def validar(self, arr):
        try:
            return (not (arr[0] < 0 or arr[1] < 0 or
                   arr[0] >= self.tam or arr[1] >= self.tam)) and\
                   (self.tablero[arr[0]][arr[1]] == ' ')   # coordenadas validas y casilla vacía
        except Exception as e:
            print(e)
            return False

    def cpu(self):
        coord = (random.randint(0, self.tam - 1), random.randint(0, self.tam - 1))      # Genera un par de coordenadas aleatorio
        while not self.validar(coord):                                                  # Revisa que las casilla esté vacía
            coord = (random.randint(0, self.tam - 1), random.randint(0, self.tam - 1))  # Si no está vacía vuelve a generar
        print('CPU tira: ', coord)
        return self.tirar('o', coord)                                                  # Realiza el tiro y retorna la cadena de control

    def enviarTablero(self, sock, control):
        s = ''.join([''.join(i) for i in self.tablero])    # Convierte la matriz en una cadena de caracteres consegutivos
        s = str(control) + s                    # Agrega la porcion de control a la cadena
        print('Cadena enviada: ', s)
        s = s.encode()                          # Codifica la cadena
        sock.sendall(s)                         # Envío por el socket

def recibirTiro(sock, juego):
    print('Esperando tiro')
    s = sock.recv(512).decode("utf-8")     # Recibe el tiro del cliente
    s = s.split(',')
    print(s)
    try:
        coords = ( int(s[1]), int(s[2]) )       # Convierte la cadena en una tupla
        if juego.validar(coords):               # La cadena recibida es valida
            return juego.tirar(s[0], coords)    # Coordenadas registradas y comprueba la condición de ganar
        else:                                   # La cadena recibida no es valida
            return '2'+ s[0]                    # Mensaje de error
    except Exception as e:
        print(e)
        return '2'+ s[0]                        # Error en la cadena

    # Valores de retorno:
    #   0 : Sigue jugando, no hay errores y nadie ha ganado
    #   1 : Termina el juego, empata o gana alguien
    #   2 : Error, rxiste un error en la cadena recibida


def enviar(sock, cadena):
    cadena = str(cadena).encode()
    sock.sendall(cadena)


def main():
    ip = None
    puerto = None

    if len(sys.argv) != 3:  # Si no hay argumentos asigna la direccion local
        ip, puerto = ('127.0.0.1', '12345')
    else:
        ip, puerto = sys.argv[1:3]  # Recupera los argumentos de ejecución

    dirServidor = (ip, int(puerto))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SocketServidor:   # Crea el socket
        SocketServidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Opciones adicionales del socket
        SocketServidor.bind(dirServidor)                                        # Ligar socket a la dirección
        SocketServidor.listen(1)                                                # Espera conexion

        print("El servidor TCP está disponible y en espera de solicitudes")

        client_conn, client_addr = SocketServidor.accept()                      # Aceptar al cliente
        print("Conectado a", client_addr)

        with client_conn:
            tam = int(((client_conn.recv(512)).decode('utf-8')))                                # Recibe dificultad
            juego = Gato(tam)                                                   # Crea juego
            print('Juego creado tablero {}x{}'.format(tam,tam))

            continuar = True                                                    # Variable para detener el juego

            juego.enviarTablero(client_conn, '0'+juego.simbolos[juego.turno])

            while continuar:                                                    # Recibe y envía tiros

                if juego.simbolos[juego.turno] == 'x':                          # Turno del cliente
                    print('Turno del cliente')
                    r = recibirTiro(client_conn, juego)                         # Analiza la cadena del cliente
                    if r[0] == '0':
                        juego.enviarTablero(client_conn, r)
                        print('Tiro registrado, el juego continúa')
                    elif r[0] =='1':
                        print('{} gana'.format(r[1]))
                        juego.enviarTablero(client_conn, r)                     # Envía tablero al cliente
                        continuar = False
                    else:
                        juego.enviarTablero(client_conn, r)                     # Error en la cadena recibida
                        print('Error en los datos recibidos')

                else:  # Turno del cpu
                    print('Turno del CPU')
                    if r[0] == '0':
                        juego.cpu()
                        print('Tiro de CPU registrado')
                        juego.enviarTablero(client_conn, r)
                        print('Tiro registrado, el juego continúa')
                    elif r[0] == '1':
                        print('{} gana'.format(r[1]))
                        juego.enviarTablero(client_conn, r)  # Envía tablero al cliente
                        continuar = False

            enviar(client_conn, '{:.2f}'.format(juego.tiempoFin - juego.tiempoInicio))  # Envía duración del juego


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
