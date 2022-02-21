import socket
import threading
from tictactoe import TicTacToe
import time

HOST = '127.0.0.1'
PORT = 65432
#s = None


# Cria um tabuleiro de jogo vazio
board = TicTacToe()
players = []
players_name = []
turno = 'X'
acabou = 0

# start_server()

# Função para executar o jogo e enviar as rodadas para o outro jogador


def game_pvp_t(conn, addr):
    global turno, acabou, players, players_name

    while True:
        # recebe o nome do jogador
        time.sleep(1)
        player_name = conn.recv(1024)
        if len(player_name) > 1:
            break

    players_name.append(player_name.decode('utf-8'))
    print('Player ' + players_name[-1] +
          ' is online! Number of players: ' + str(len(players)))

    # envia mensagem de 'bem-vindo'
    if len(players) < 2:
        msg = "hello1"
        conn.send(msg.encode('utf-8'))
    else:
        msg = "hello2"
        conn.send(msg.encode('utf-8'))
        time.sleep(1)

        # envia os dados dos jogadores
        msg = "iamplayer1$" + players_name[1]
        players[0].send(msg.encode('utf-8'))

        msg = "iamplayer2$" + players_name[0]
        players[1].send(msg.encode('utf-8'))

        time.sleep(3)

        msgg = "begin"
        players[0].send(msgg.encode('utf-8'))
        players[1].send(msgg.encode('utf-8'))

    while True:
        # recebe a jogada do jogador
        data = conn.recv(4096)
        if not data:
            break

        data = data.decode('utf-8')
        # envia a jogada do outro jogador para o adversário
        if data.startswith("$coord:"):
            if conn == players[0]:
                players[1].send(data.encode('utf-8'))
            else:
                players[0].send(data.encode('utf-8'))

    # remove o jogador após o fim da partida ou perda de conexão
    if conn == players[0]:
        del players[0]
    else:
        del players[1]


def game_ia_t(conn, addr):
    while True:
        # recebe o nome do jogador
        time.sleep(1)
        player_name = conn.recv(1024)
        if len(player_name) > 1:
            break

        print('Player ' + players_name[-1] +
              ' is online! IA mode')

        msg = "hello3"
        conn.send(msg.encode('utf-8'))


def start_server():
    global HOST, PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        # Aceita novos jogadores se o número de jogadores ativos for menor que 2
        while True:
            conn, addr = s.accept()
            msg = "Hello! What game mode do you wanna play? Press '1' for 'Player vs Player' and '2' for 'Player vs IA'"
            conn.sendall(msg.encode('utf-8'))

            game_mode = conn.recv(1024)

            if game_mode == 1:
                if len(players) < 2:
                    players.append(conn)
                    threading._start_new_thread(
                        game_pvp_t, (conn, addr))
                else:
                    msg = "full"
                    conn.sendall(msg.encode('utf-8'))

            else:
                if len(players) < 1:
                    players.append(conn)
                    threading._start_new_thread(game_ia_t, (conn, addr))
                else:
                    msg = "full"
                    conn.sendall(msg.encode('utf-8'))

                # board.printBoard()

                # jogador = 0
                # self.board = criarBoard()
                # ganhador = verificaGanhador(self.board)

                # while(not ganhador):
                #     printBoard(self.board)
                #     print("=========================")

                #     if(jogador == 0):
                #     i, j = movimentoIA(self.board, jogador)
                #     #i = getInputValido("Digite a linha: ")
                #     #j = getInputValido("Digite a coluna: ")

                #     else:
                #     i, j = movimentoIA(self.board, jogador)
                #     #i = getInputValido("Digite a linha: ")
                #     #j = getInputValido("Digite a coluna: ")

                #     if(verificaMovimento(self.board, i, j)):
                #     fazMovimento(self.board, i, j, jogador)
                #     jogador = (jogador + 1) % 2

                #     else:
                #     print("A posicao informada ja esta ocupada")

                #     ganhador = verificaGanhador(self.board)

                # print("=========================")
                # printBoard(self.board)
                # print("Ganhador = ", ganhador)
                # print("=========================")


start_server()
