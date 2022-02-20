import socket
import threading
from tictactoe import TicTacToe
import time

HOST = '127.0.0.1'
PORT = 65432
#s = None


#Cria um tabuleiro de jogo vazio
board = TicTacToe()
players = []
players_name = []
turno = 'X'
acabou = 0

#start_server()

# Função para executar o jogo e enviar as rodadas para o outro jogador
def game_t(conn, addr):
    global turno, acabou, players, players_name
    player = 0
    message = ""

    while True:
    # recebe o nome do jogador
        time.sleep(1)
        player_name = conn.recv(1024)
        #print(player_name)
        if len(player_name) > 1:
            break
    
    #player_name = player_name.rstrip()
    players_name.append(player_name.decode('utf-8'))
    print(players_name[-1])

    # define os turnos de cada jogador
    # if turno == 'O':
    #     player = 'O'
    #     turno = 'X'
    # else:
    #     player = 'X'
    #     turno = 'O'

    # envia mensagem de 'bem-vindo'
    if len(players) < 2:
        msg = "welcome1"
        conn.send(msg.encode('utf-8'))
        #print(players[0], conn)
    else:
        msg = "welcome2"
        conn.send(msg.encode('utf-8'))
        #print(players[1], conn)
        time.sleep(1)

        # envia os dados dos jogadores
        msg = "iamplayer1$" + players_name[1]
        players[0].send(msg.encode('utf-8'))

        msg = "iamplayer2$" + players_name[0]
        players[1].send(msg.encode('utf-8'))
        
    # while True:
        
    #     # recebe a jogada do jogador
    #     data = conn.recv(4096)
    #     if not data:
    #         break
        
    #     # envia a jogada do outro jogador para o adversário
    #     if data.startswith("$xy$"):
    #         if conn == players[0]:
    #             players[1].send(data)
    #         else:
    #             players[0].send(data) 
    
    # remove o jogador após o fim da partida ou perda de conexão
    #if conn == players[0]:
    #    del players[0]
    #else:
    #    del players[1]

    #conn.close()         
                 
                      
def start_server():
    global HOST, PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        # Aceita novos jogadores se o número de jogadores ativos for menor que 2 
        while True:
            conn, addr = s.accept()
            if len(players) < 2:
                print('Jogador se conectou!', len(players))
                players.append(conn)
                threading._start_new_thread(game_t, (conn, addr))
                #player.start()
                    
            
                
                # data = conn.recv(1024)
                # if not data:
                #     break
                # conn.sendall(data)
            else:
                # conn.sendall('Já temos muitos jogadores, querido!'.encode('utf-8'))
                print('Jogador vai embora!', len(players))
                
                #conn.close() 
                
                
                #board.printBoard()
                
                
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