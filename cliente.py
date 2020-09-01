import socket
import sys


def recibir(sock, buffsize):
    return sock.recv(buffsize).decode("utf-8")


def enviar(sock, cadena):
    cadena = str(cadena).encode()
    sock.sendall(cadena)


def comprobar(resultado):
    # --------------------------------------------------------------------------------------------------------------------------------------------
    # estado
    #   -2 = El Juego acaba de iniciar
    #   -1 = La cadena enviada no era valida(*)
    #    0 = El juego termina en empate(*)
    #    1 = Se registró el tiro correctamente pero nadie ha ganado - El resto de la cadena indica los cambios que se realizan al tablero local
    #    2 = Gana el cliente(*)
    #    3 = Gana el servidor(*)
    #
    #        (*) - El resto de la cadena se vuelve irrelevante
    #
    # ____________________________________________________________________________________________________________________________________________
    # jugador
    #   1 = El tiro era del cliente
    #   2 = Es tiro era del servidor
    #
    # ____________________________________________________________________________________________________________________________________________
    # coordenadas
    #   tupla que indica la casilla donde colocar el simbolo del tiro
    #
    # --------------------------------------------------------------------------------------------------------------------------------------------

    partir = resultado.split(',')  # Separa los argumentos recibidos
    if len(partir) == 1 or partir[0] != '1':  # Si solo se envío el digito de estado
        estado = int(partir[0])  # Obtén el valor del digito de control
        return estado

    else:  # Si se envió información adicional
        estado, jugador, c1, c2 = partir  # Obten los demás datos
        jugador = int(jugador)
        coordenadas = int(c1), int(c2)
        ret = int(estado), jugador, coordenadas

        return int(estado), jugador, coordenadas


def imprimirTablero(tablero, tam):
    for x in range(tam):
        for y in range(tam):
            print("{} \t".format(tablero[x][y]), end="", flush=True)
        print("\n")


def cambiarTablero(tablero, coordenadas, simbolo):
    tablero[coordenadas[0]][coordenadas[1]] = simbolo


def main():
    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)

    ip, puerto = sys.argv[1:3]

    dirServidor = (ip, int(puerto))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SocketCliente:
        print('Conectando al servidor...')
        SocketCliente.connect(dirServidor)
        print('Conectado')

        # Inicia el juego
        # Elegir dificultad
        print('Elija la dificultad del juego: \n 1) 3x3\n 2) 5x5')
        dificultad = int(input())
        tam = dificultad * 2 + 1
        tableroLocal = [[0 for x in range(tam)] for y in range(tam)]  # Crea un tablero de tam x tam lleno de ceros
        enviar(SocketCliente, tam)  # Envía la dificultad al servidor

        continuar = True
        turno = 1

        while continuar:  # Enviar y recibir tiros
            resultado = recibir(SocketCliente, 512)
            print('R: {}'.format(resultado))
            resultado = comprobar(resultado)

            if type(resultado) == int:  # Se recibe una trama de control
                if resultado == -1:  # No valido
                    print(
                        'La cadena ingresara no es válida.\nIngrese las coordenadas de la casilla que quiera elegir: ')
                    tiro = input()
                    enviar(SocketCliente, tiro)
                elif resultado == -2:  # Inicio
                    print('Ingrese las coordenadas de la casilla que quiera elegir: ')
                    tiro = input()
                    enviar(SocketCliente, tiro)
                elif resultado == 0:  # Empate
                    print('El juego ha terminado: EMPATE')
                    continuar = False
                elif resultado == 2:  # Gana cliente
                    print('El juego ha terminado: HAS GANADO')
                    continuar = False
                elif resultado == 3:  # Gana servidor
                    print('El juego ha terminado: CPU GANA')
                    continuar = False

            else:  # Se recibe una trama de tiro
                cambiarTablero(tableroLocal, resultado[2], str(resultado[1]))  # Realizar el cambio en el tablero local
                imprimirTablero(tableroLocal, tam)  # Imprimir tablero
                turno = resultado[1]  # Cambiar al siguente jugador
                if turno == 1:  # Turno del cliente
                    print('Ingrese las coordenadas de la casilla que quiera elegir: ')
                    tiro = input()
                    enviar(SocketCliente, tiro)

                else:  # Turno del cpu
                    print('Tiro del cpu: {},{}'.format(resultado[2][0], resultado[2][1]))
                    cambiarTablero(tableroLocal, resultado[2], str(resultado[1]))
                    imprimirTablero(tableroLocal, tam)  # Imprimir tablero

        duracion = recibir(SocketCliente, 256)  # Recibir duración del juego
        print('El juego ha durado ' + duracion + 'segundos')
        # FIN


if __name__ == '__main__':
    main()
