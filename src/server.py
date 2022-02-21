import socket
import threading
from tictactoe import TicTacToe as ttt
import ia
import time

HOST = '127.0.0.1'
PORT = 65432
s = None

players = []
players_name = []
turno = 'X'
is_over = False
players_ia = 0

# Função para executar o jogo e enviar as rodadas para o outro jogador

def check_end_ia_game(board, player_name):
    global is_over
    is_over = ttt.verificaGanhador(board)
    if is_over == "X":
        print("Me: I lost! Player " + player_name + " won!")
        print("\n###########################################\n")
    elif is_over == "O":
        print("Me: I won! Player " + player_name + " lost!")
        print("\n###########################################\n")
    elif is_over == "DRAW":
        print("Me: It's a DRAW!")
        print("\n################\n")
    else:
        return False
    return True

def game_pvp_t(conn, addr):
    global turno, players, players_name

    while True:
        # recebe o nome do jogador
        time.sleep(1)
        player_name = conn.recv(1024)
        if len(player_name) > 1:
            break

    players_name.append(player_name.decode('utf-8'))
    print('Me: Player ' + players_name[-1] +
          ' is online! Number of players PvP: ' + str(len(players)))

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
    global players_ia, is_over

    # Cria um tabuleiro de jogo vazio
    board = ttt()

    while True:
        # recebe o nome do jogador
        time.sleep(1)
        player_name = conn.recv(1024)
        if len(player_name) > 0:
            break

    player_name = player_name.decode('utf-8')
    print('Me: Player ' + player_name +
            ' is online! IA mode')

    msg = "hello3"
    conn.send(msg.encode('utf-8'))

    # envia os dados dos jogadores
    msg = "iamplayer1$me ;)"
    conn.send(msg.encode('utf-8'))
    init = 0
    while not is_over:
        # recebe a jogada do jogador
        while True:
            data = conn.recv(4096)
            if data:
                break
        
        data = data.decode('utf-8')
        # envia a jogada do outro jogador para o adversário
        if data.startswith("$coord:"):
            x = int(data[7])
            y = int(data[8])
            ttt.fazMovimento(board, x, y, 0)

            print("Me: Player " + player_name + " played:")
            ttt.printBoard(board)

            is_over = check_end_ia_game(board, player_name)

            if init == 0:
                msgg = "begin"
                conn.send(msgg.encode('utf-8'))
                init = 1
                time.sleep(3)
            
            if not is_over:
                while True:
                    x, y = ia.movimentoIA(board.board, 1)

                    if ttt.verificaMovimento(board, x, y):
                        print("Me: Opponent " + player_name + ". My turn:") 
                        ttt.fazMovimento(board, x, y, 1)
                        ttt.printBoard(board)
                        jogadaaa = "$coord:" + str(x) + str(y)

                        x = conn.send(jogadaaa.encode('utf-8'))
                        break
                    
                    else:
                        print("Me: Invalid move.")

                is_over = check_end_ia_game(board, player_name)
    
    players_ia -= 1


def start_server():
    global HOST, PORT, players, players_ia

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Me: I'm awake. Waiting foy players...")

        # Aceita novos jogadores se o número de jogadores ativos for menor que 2
        while True:
            conn, addr = s.accept()
            msg = "ia_mode"

            conn.send(msg.encode('utf-8'))
            time.sleep(1)
            game_mode = conn.recv(1024)

            if not game_mode:
                break
            
            game_mode = int(game_mode.decode('utf-8'))
            #print("game_mode", game_mode)

            if game_mode == 1:
                if len(players) < 2:
                    players.append(conn)
                    threading._start_new_thread(
                        game_pvp_t, (conn, addr))
                else:
                    msg = "full"
                    conn.sendall(msg.encode('utf-8'))

            else:
                players_ia += 1
                print("Me: Number of all players: " + str(len(players) + players_ia))
                threading._start_new_thread(game_ia_t, (conn, addr))

start_server()
