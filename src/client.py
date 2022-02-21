#!/usr/bin/env python3
import time
import socket
import threading
from tictactoe import TicTacToe as ttt


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
c = None

player1 = {
    "name": "",
    "symbol": "X",
    "score": 0,
}
player2 = {
    "name": "",
    "symbol": "O",
    "score": 0,
}

me = 0
current_turn = 0
is_over = False
# Cria um tabuleiro de jogo vazio
board = ttt()


def check_endgame():
    global c, board, me

    result = ttt.verificaGanhador(board)
    if result == "DRAW":
        print("SophLia: AH! It's a DRAW! That was a nice match!")
    elif (result == "X" and me == 0) or (result == "O" and me == 1):
        print("SophLia: Congrats! You won! :D ")
    elif (result == "X" and me == 1) or (result == "O" and me == 0):
        print("SophLia: Oh no! You lost! :(. Try again later.")
    else:
        return False
    return True


def do_playing(x, y):
    global c, me, board, current_turn, is_over
    if me == current_turn:
        if x != -100 and y != -100:
            ttt.fazMovimento(board, x, y, ((me + 1) % 2))
            is_over = check_endgame()
            ttt.printBoard(board)

        if not is_over:
            print("\nSophLia: It's your turn!")

            while True:
                x = ttt.getInputValido("SophLia: Enter row (1-3): ")
                y = ttt.getInputValido("SophLia: Enter column (1-3): ")

                if ttt.verificaMovimento(board, x, y):
                    ttt.fazMovimento(board, x, y, me)
                    ttt.printBoard(board)
                    jogadaaa = "$coord:" + str(x) + str(y)

                    c.send(jogadaaa.encode('utf-8'))
                    current_turn = (current_turn + 1) % 2
                    break
                else:
                    print("SophLia: Invalid move.")

            is_over = check_endgame()

        return is_over
    else:
        print("SophLia: We're waiting for your opponent's move.")
        return 100


def running_game_t(c, name):
    global current_turn, player1, player2, me, board, is_over
    data_server = " "
    while not is_over:
        data_server = c.recv(4096)

        if not data_server:
            break

        data_server = data_server.decode('utf-8')
        if data_server.startswith("full"):
            print("SophLia: Oh, " + name +
                  "! We're in the middle of a turn, try again later! :(")
            break

        if data_server.startswith("hello"):
            if data_server == "hello1":
                player1["name"] = name
                print("SophLia: Welcome " +
                      player1["name"] + "! We're waiting for your opponent.")

            elif data_server == "hello2":
                player2["name"] = name
                print("Sophlia: Welcome " +
                      player2["name"] + "! Glad you're here! Tic Tac Toe will start soon.")

            elif data_server == "hello3":
                player1["name"] = name
                print("Sophlia: Welcome " +
                      player1["name"] + "! Glad you're here!")

        elif data_server.startswith("iamplayer"):
            if data_server.startswith("iamplayer1$"):
                print("SophLia: Hey! Your game will start now! \n")
                player2["name"] = data_server[11: len(data_server)]
                print("SophLia: Your opponent is " +
                      player2["name"] + ". Good Luck!")
                time.sleep(1)
                do_playing(-100, -100)

            elif data_server.startswith("iamplayer2$"):
                me = 1  # Representa o player 2
                player1["name"] = data_server[11: len(data_server)]
                print("SophLia: Your opponent is " +
                      player1["name"] + ". Good Luck!")
                time.sleep(1)
                print("SophLia: It's your opponent's turn.")

        elif data_server.startswith("begin"):
            while not is_over:
                while True:
                    data_server = c.recv(1024)
                    if len(data_server) > 0:
                        break

                data_server = data_server.decode('utf-8')
                if data_server.startswith("$coord:"):
                    current_turn = me
                    
                    x = int(data_server[7])
                    y = int(data_server[8])

                    result = do_playing(x, y)
                    if result == True:
                        is_over = True
                        break
                    
                    current_turn = ((me + 1) % 2)

        time.sleep(2)
    c.close()


def connect_server():
    global c, HOST, PORT, player1, player2

    name = input("SophLia: Hey, player! Enter your name: ")

    while len(name) == 0:
        name = input("SophLia: Please, you need to enter your name: ")

    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((HOST, PORT))

        while True:
            time.sleep(1)
            ia_mode = c.recv(4096)
            if len(ia_mode) > 1:
                break

        ia_mode = ia_mode.decode('utf-8')
        if ia_mode == "ia_mode":
            print("Hello! What game mode do you wanna play?")
            answer = str(ttt.getInputValido("Press '1' for 'Player vs Player' and '2' for 'Player vs IA': ") + 1)
            c.send(answer.encode('utf-8'))

        #time.sleep(2)
        c.send(name.encode('utf-8'))

        threading.Thread(target=running_game_t, args=(c, name)).start()

    except Exception as e:
        print("ERROR")


connect_server()
