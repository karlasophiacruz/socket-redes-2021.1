#!/usr/bin/env python3
import time
import socket
import threading
import tictactoe
from tictactoe import TicTacToe as ttt

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
c = None

# Dados do Player 1
player1 = {
    "name": "",
    "symbol": "X",
}

# Dados do Player 2
player2 = {
    "name": "",
    "symbol": "O",
}

me = 0 # Define se o jogador é player 1 (me = 0) ou player 2 (me = 1)
current_turn = 0 # Define o turno atual
is_over = False # Define se o jogo acabou

# Cria um tabuleiro de jogo vazio
board = ttt()

# Função para checar se o jogo acabou
def check_endgame():
    global board, me
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

# Função para realizar a jogada do oponente e a jogada do jogador
def do_playing(x, y):
    global c, me, board, current_turn, is_over

    if me == current_turn:
        # Checa se não é a primeira jogada
        if x != -100 and y != -100:
            # Realiza a jogada do oponente
            ttt.fazMovimento(board, x, y, ((me + 1) % 2))
            is_over = check_endgame()

            ttt.printBoard(board)

        if not is_over:
            print("\nSophLia: It's your turn!")

            # Realiza a jogada do jogador
            while True:
                x = ttt.getInputValido("SophLia: Enter row (1-3): ")
                y = ttt.getInputValido("SophLia: Enter column (1-3): ")

                if ttt.verificaMovimento(board, x, y):
                    ttt.fazMovimento(board, x, y, me)

                    tictactoe.clear() # LIMPA A TELA

                    ttt.printBoard(board)

                    jogadaaa = "$coord:" + str(x) + str(y)

                    # Envia a jogada para o servidor enviar para o oponente
                    c.send(jogadaaa.encode('utf-8'))
                    
                    # Muda o turno do jogo
                    current_turn = (current_turn + 1) % 2
                    break
                else:
                    print("SophLia: Invalid move.")

            is_over = check_endgame()

        return is_over
    else:
        print("SophLia: We're waiting for your opponent's move.")
        return 100

# Função que roda o jogo do cliente na thread
def running_game_t(c, name):
    global current_turn, player1, player2, me, board, is_over
    data_server = " "

    while not is_over:
        # Recebe a mensagem do servidor
        data_server = c.recv(4096)

        if not data_server:
            break

        data_server = data_server.decode('utf-8')

        # Mensagem de que o jogo já começou
        if data_server.startswith("full"):
            print("SophLia: Oh, " + name +
                  "! We're in the middle of a turn, try again later! :(")
            break

        # Mensagem de bem-vindo
        elif data_server.startswith("hello"):
            # Primeiro jogador a entrar no servidor
            if data_server == "hello1":
                player1["name"] = name
                print("SophLia: Welcome " +
                      player1["name"] + "! We're waiting for your opponent.")
            
            # Segundo jogador a entrar no servidor
            elif data_server == "hello2":
                player2["name"] = name
                print("Sophlia: Welcome " +
                      player2["name"] + "! Glad you're here! Tic Tac Toe will start soon.")

            # Jogador do modo IA
            elif data_server == "hello3":
                player1["name"] = name
                print("Sophlia: Welcome " +
                      player1["name"] + "! Glad you're here!")
        
        # Mensagem para pegar os dados do jogador e do oponente
        elif data_server.startswith("iamplayer"):
            # Define o jogador como Player 1
            if data_server.startswith("iamplayer1$"):
                print("SophLia: Hey! Your game will start now! \n")

                player2["name"] = data_server[11: len(data_server)]
                print("SophLia: Your opponent is " +
                      player2["name"] + ". Good Luck!")

                time.sleep(1)

                # Player 1 sempre inicia a jogada
                do_playing(-100, -100)

            # Define o jogador como Player 2
            elif data_server.startswith("iamplayer2$"):
                me = 1  # Representa o player 2
                player1["name"] = data_server[11: len(data_server)]

                print("SophLia: Your opponent is " +
                      player1["name"] + ". Good Luck!")
                print("SophLia: It's your opponent's turn.")
        
        # Mensagem que representa que o jogo começou
        elif data_server.startswith("begin"):
            while not is_over:
                if me == 0:
                    print("SophLia: Waiting for " + player2["name"] + "'s move...")
                else:
                    print("SophLia: Waiting for " + player1["name"] + "'s move...")

                # Receber a mensagem do servidor
                while True:
                    data_server = c.recv(1024)
                    if len(data_server) > 0:
                        break
                
                tictactoe.clear() # LIMPA A TELA

                data_server = data_server.decode('utf-8')

                # Checa se a mensagem recebida é a jogada do oponente
                if data_server.startswith("$coord:"):
                    current_turn = me
                    
                    x = int(data_server[7])
                    y = int(data_server[8])

                    result = do_playing(x, y)
                    if result == True:
                        is_over = True
                        break
                    
                    # Troca o turno do jogo
                    current_turn = ((me + 1) % 2)
                
                # Checa se a mensagem recebida é um erro de desconexão do oponente
                elif data_server.startswith("err"):
                    is_over = True
                    if me == 1:
                        print("SophLia: Oh! " + player1["name"] + " gave up!")
                        print("SophLia: Congrats! You won by W/O.")

                    else:
                        print("SophLia: Oh! " + player2["name"] + " gave up!")
                        print("SophLia: Congrats! You won by W/O.")
                    
        # Checa se a mensagem recebida é um erro de desconexão do oponente
        elif data_server.startswith("err"):
            if me == 1:
                print("SophLia: Oh! " + player1["name"] + " gave up!")
                print("SophLia: Congrats! You won by W/O.")
                break
            else:
                print("SophLia: Oh! " + player2["name"] + " gave up!")
                print("SophLia: Congrats! You won by W/O.")
                break

        time.sleep(2)
    c.close()

# Função principal de conexão com o servidor
def connect_server():
    global c, HOST, PORT

    # Ler o nome
    name = input("SophLia: Hey, player! Enter your name: ")

    while len(name) == 0:
        name = input("SophLia: Please, you need to enter your name: ")

    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((HOST, PORT))

        # Recebe a mensagem do servidor
        while True:
            time.sleep(1)
            ia_mode = c.recv(4096)
            if len(ia_mode) > 1:
                break

        ia_mode = ia_mode.decode('utf-8')

        # Checa se a mensagem é para perguntar o modo de jogo escolhido
        if ia_mode == "ia_mode":
            print("SophLia: What game mode do you wanna play?")
            answer = str(ttt.getInputValido("SophLia: Press '1' for 'Player vs Player' and '2' for 'Player vs IA': ") + 1)
            
            # Envia a resposta do jogador para o servidor
            c.send(answer.encode('utf-8'))
        
        # Envia o nome do jogador para o servidor
        c.send(name.encode('utf-8'))

        # Inicia a thread que rodará a função do jogo no cliente
        threading.Thread(target=running_game_t, args=(c, name)).start()
        
        tictactoe.clear() # LIMPA A TELA

    except Exception as e:
        print("ERROR")

connect_server()
