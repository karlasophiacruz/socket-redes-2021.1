#!/usr/bin/env python3
import time
import socket
import threading


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
c = None

player1 = {
    "name": "",
    "symbol": "X",
    "score": 0
}
player2 = {
    "name": "",
    "symbol": "O",
    "score": 0
}

turno = 0

def running_game_t(c, m, name):
    global turno, player1, player2
    data_server = " "
    while True:
        data_server = c.recv(4096)

        if not data_server:
            break

        data_server = data_server.decode('utf-8')
        
        if data_server.startswith("welcome"):
            if data_server == "welcome1":
                player1["name"] = name
                print("Sophlia: Welcome " + player1["name"] + "! Waiting for your opponent")
            
            elif data_server == "welcome2":
                player2["name"] = name
                print("Sophlia: Welcome " + player2["name"] + "! Yeah! Tic Tac Toe will start soon")

        elif data_server.startswith("iamplayer"):
            if data_server.startswith("iamplayer1$"):
                print("SophLia: Hey! Your game will start now! \n")
                player2["name"] = data_server[11 : len(data_server)]
                print("SophLia: Your opponent is", player2["name"])
            
            elif data_server.startswith("iamplayer2$"):
                player1["name"] = data_server[11 : len(data_server)]
                print("SophLia: Your opponent is", player1["name"])
        
        
        time.sleep(3)            

def connect_server():
    global c, HOST, PORT, player1, player2

    name = input("Sophlia: Hey, player! Enter your name: ")
    
    while len(name) == 0:
        name = input("Enter your name, please! ")

    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((HOST, PORT))
        #data = []
        c.send(name.encode('utf-8'))
        
        threading.Thread(target=running_game_t, args=(c, "m", name)).start()
    
    except Exception as e:
        print("ERROR")

    
        # Mantem uma conexão com o servidor
        # while True:
            # Recebe as mensagens do servidor que informam o Jogador, Turno, Tabuleiro e se acabou
            #while True:
                # time.sleep(2)
                # byte = s.recv(1)
                #print(byte.decode('utf-8'))

                # if byte.decode('utf-8') == "1":
                #     break
            
            # while True:
            #     # byte = s.recv(1024)
            #     if not byte:
            #         print("entrou")
            #         stre = ' '.join(map(str, data))
            #         strr = stre.split('$')
            #         player = strr[0]
            #         turno = strr[1]
            #         board = strr[2]
            #         acabou = strr[3]
            #         print(player)
            #         print(turno)
            #         print(board)
            #         print(acabou)
            #         break

            #     data.append(byte.decode('utf-8'))
        
connect_server()