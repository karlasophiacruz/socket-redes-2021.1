import socket
import threading
import tictactoe
from tictactoe import TicTacToe as ttt
import ia
import time

HOST = '127.0.0.1'
PORT = 65432
s = None

players = []
players_name = []
is_over = False
players_ia = 0


# Função para o servidor checar se o jogo no modo IA acabou
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


# Função para executar o jogo no modo PvP, enviando as jogadas de um jogador ao outro
def game_pvp_t(conn, addr):
    global players, players_name
    erro = 0
    # Recebe o nome do jogador
    while True:
        time.sleep(1)
        player_name = conn.recv(1024)
        if len(player_name) > 1:
            break

    player_name = player_name.decode('utf-8')
    players_name.append(player_name)
    print('Me: Player ' + players_name[-1] +
          ' is online!')

    # Envia mensagem de 'bem-vindo'
    if len(players) < 2:
        msg = "hello1"
        conn.send(msg.encode('utf-8'))
    else:
        msg = "hello2"
        conn.send(msg.encode('utf-8'))
        time.sleep(1)

        # Envia os dados dos jogadores
        msg = "iamplayer1$" + players_name[1]
        players[0].send(msg.encode('utf-8'))

        msg = "iamplayer2$" + players_name[0]
        players[1].send(msg.encode('utf-8'))

        time.sleep(2)

        # Envia mensagem para iniciar o jogo, pois o tabuleiro está completo
        msgg = "begin"
        players[0].send(msgg.encode('utf-8'))
        players[1].send(msgg.encode('utf-8'))

    while True:
        try:
            # Recebe a jogada do jogador
            data = conn.recv(4096)
            if not data:
                break

            data = data.decode('utf-8')

            # Envia a jogada do outro jogador para o adversário
            if data.startswith("$coord:"):
                if conn == players[0]:
                    players[1].send(data.encode('utf-8'))
                else:
                    players[0].send(data.encode('utf-8'))

        except:
            erro = 1
            break

    # Remove o jogador após o fim da partida ou perda de conexão
    if conn == players[0]:
        if erro:
            erro = "err"
            players[-1].send(erro.encode('utf-8'))
        print("Me: " + players_name[0] + " is offline.")
        del players[0], players_name[0]

    else:
        erro = "err"
        players[0].send(erro.encode('utf-8'))
        print("Me: " + players_name[-1] + " is offline.")
        del players[-1], players_name[-1]


# Função para executar o jogo no modo IA
def game_ia_t(conn, addr):
    global players_ia, is_over

    # Cria um tabuleiro de jogo vazio
    board = ttt()

    # Recebe o nome do jogador
    while True:
        time.sleep(1)
        player_name = conn.recv(1024)
        if len(player_name) > 0:
            break

    player_name = player_name.decode('utf-8')
    print('Me: Player ' + player_name +
          ' is online! IA mode')

    # Envia mensagem de 'bem-vindo'
    msg = "hello3"
    conn.send(msg.encode('utf-8'))

    # Envia os dados dos jogadores
    msg = "iamplayer1$me ;)"
    conn.send(msg.encode('utf-8'))

    init = 0
    while not is_over:
        # Recebe a jogada do jogador
        while True:
            data = conn.recv(4096)
            if data:
                break

        data = data.decode('utf-8')
        # Realiza a jogada do jogador no tabuleiro da IA
        if data.startswith("$coord:"):
            x = int(data[7])
            y = int(data[8])
            ttt.fazMovimento(board, x, y, 0)

            print("Me: Player " + player_name + " played:")
            ttt.printBoard(board)

            is_over = check_end_ia_game(board, player_name)

            # Quando o jogador fizer a primeira jogada da partida, ...
            if init == 0:
                msgg = "begin"
                # ... envia mensagem para o jogador entrar no loop
                conn.send(msgg.encode('utf-8'))
                init = 1
                time.sleep(2)

            # Se o jogo não acabou, a IA realiza sua jogada
            if not is_over:
                tictactoe.clear()
                while True:
                    x, y = ia.movimentoIA(board.board, 1)

                    if ttt.verificaMovimento(board, x, y):
                        print("Me: Opponent " + player_name + ". My turn:")
                        ttt.fazMovimento(board, x, y, 1)
                        ttt.printBoard(board)
                        jogadaaa = "$coord:" + str(x) + str(y)

                        # Envia a jogada da IA para o jogador
                        conn.send(jogadaaa.encode('utf-8'))
                        break

                    else:
                        print("Me: Invalid move.")

                is_over = check_end_ia_game(board, player_name)
        time.sleep(1)

    # Remove o jogador após o fim da partida ou perda de conexão
    print("Me: " + player_name + " is offline.")
    players_ia -= 1


def start_server():
    global HOST, PORT, players, players_ia

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Me: I'm awake. Waiting for players...")

        # Aceita novos jogadores:
        # --> no modo PvP, se o número de jogadores ativos for menor que 2
        # --> no modo IA, não há restrição de jogadores
        while True:
            conn, addr = s.accept()

            # Envia a mensagem ao jogador para escolher o modo de jogo
            msg = "ia_mode"
            conn.send(msg.encode('utf-8'))

            time.sleep(1)

            game_mode = conn.recv(1024)
            if not game_mode:
                break

            game_mode = int(game_mode.decode('utf-8'))

            # Modo PvP
            if game_mode == 1:
                if len(players) < 2:
                    players.append(conn)
                    print("Me: Number of players PvP: " + str(len(players)))

                    # Inicia a thread do jogo PvP
                    threading._start_new_thread(
                        game_pvp_t, (conn, addr))
                else:
                    msg = "full"
                    # Envia mensagem ao jogador de que já existe um jogo em andamento
                    conn.sendall(msg.encode('utf-8'))

            # Modo IA
            else:
                players_ia += 1
                print("Me: Number of all players: " +
                      str(len(players) + players_ia))

                # Inicia a thread do jogo Player vs IA
                threading._start_new_thread(game_ia_t, (conn, addr))


start_server()
