import socket
import threading
from tictactoe import TicTacToe
import time

HOST = '127.0.0.1'
PORT = 65432

#Cria um tabuleiro de jogo vazio
board = TicTacToe()
players = []
turno = 'X'
acabou = 0

def connection_t(conn, addr):
    global turno, acabou
    player = 0

    if turno == 'O':
        player = 'O'
        turno = 'X'
    else:
        player = 'X'
        turno = 'O'

    while True:
        if len(players) == 2:
            conn.sendall('1'.encode('utf-8'))
            msg = player + '$' + turno + '$\n' + str(board) + '$' + str(acabou)
            conn.sendall(msg.encode('utf-8'))    
            break
        else:
            time.sleep(1)
            conn.sendall('0'.encode('utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        if len(players) < 2:
            with conn:
                player = threading.Thread(target=connection_t, args=(conn, addr))
                player.start()
                players.append(player)
                print('Jogador se conectou!', len(players))
        
            
            # data = conn.recv(1024)
            # if not data:
            #     break
            # conn.sendall(data)
        else:
            conn.sendall('Já temos muitos jogadores, querido!'.encode('utf-8'))
            conn.close() 
            
            
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
