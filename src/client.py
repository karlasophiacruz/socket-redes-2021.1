#!/usr/bin/env python3
import time
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = []

    # Mantem uma conexão com o servidor
    while True:
        # Recebe as mensagens do servidor que informam o Jogador, Turno, Tabuleiro e se acabou
        while True:
            time.sleep(2)
            byte = s.recv(1)
            print(byte.decode('utf-8'))

            if byte.decode('utf-8') == "1":
                break
        
        while True:
            byte = s.recv(1024)
            if not byte:
                print("entrou")
                stre = ' '.join(map(str, data))
                strr = stre.split('$')
                player = strr[0]
                turno = strr[1]
                board = strr[2]
                acabou = strr[3]
                print(player)
                print(turno)
                print(board)
                print(acabou)
                break

            data.append(byte.decode('utf-8'))
        