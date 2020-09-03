import socket
import sys


def recibirTablero(sock, tamTablero):
    s = sock.recv(512).decode("utf-8")  # control simbolo tablero
    print('R: ',s)
    print('Tablero actual')
    print('____________________')
    imprimirTablero(s[2:], tamTablero)  # imprime el tablero recibido
    print('\n____________________')
    return s[0:2]                       # retorna la porcion de control de la cadena

def enviarTiro(sock, simbolo, par_coordenado):
    cadena = simbolo + ',' + par_coordenado
    cadena = cadena.encode()
    sock.sendall(cadena)


def imprimirTablero(s, tam):
    for i in range(0, len(s)):
        if (i%tam) == 0:
            print("\n")
        print("{} \t".format(s[i]), end="", flush=True)

def main():
    # Argumentos de ejecución
    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)
    ip, puerto = sys.argv[1:3]
    dirServidor = (ip, int(puerto))

    turno = 1

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SocketCliente: # Creación del socket
        print('Conectando al servidor...')
        SocketCliente.connect(dirServidor) # Conexión del socket
        print('Conectado')

        # Inicia el juego
        print('Elija la dificultad del juego: \n 1) 3x3\n 2) 5x5')
        dificultad = int(input())                   # Ingresar la dificultad
        tam = dificultad * 2 + 1                    # Convertir a un numero impar
        SocketCliente.sendall(str(tam).encode())    # Envía la dificultad al servidor
        misimbolo = 'x'

        continuar = True                    # Variable para detener el juego

        while continuar:                    # Enviar y recibir tiros

            codigo = recibirTablero(SocketCliente, tam)  # Espera e imprime el tablero. codigo indica el estado del juego

            if codigo[0] == '0':                                 # Seguir jugando
                if codigo[1] == misimbolo:
                    print('Su turno. Ingrese las coordenadas de su tiro: ')
                    tiro = input()
                    enviarTiro(SocketCliente, misimbolo, tiro)          # enviar tiro
                else:
                    print('Turno del CPU')
            elif codigo[0] == 1: # El juego termina
                print('{} gana')
                continuar = False
            else: # Error
                if codigo[1] == misimbolo:
                    print('Error en la cadena enviada, intente de nuevo')
                else:
                    pass

        duracion = recibir(SocketCliente, 256)  # Recibir duración del juego
        print('El juego ha durado ' + duracion + 'segundos')
        # FIN


if __name__ == '__main__':
    main()