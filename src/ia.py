from tictactoe import TicTacToe as ttt

branco = " "
token = ["X", "O"]


def getPosicoes(board):
  posicoes = []
  for i in range(3):
    for j in range(3):
      if board[i][j] == branco:
        posicoes.append([i, j])
  
  return posicoes


def movimentoIA(board, jogador):
  possibilidades = getPosicoes(board)
  melhor_valor = None
  melhor_movimento = None

  for possibilidade in possibilidades:
    board[possibilidade[0]][possibilidade[1]] = token[jogador]
    valor = minimax(board, jogador)
    board[possibilidade[0]][possibilidade[1]] = branco

    if(melhor_valor is None):
      melhor_valor = valor
      melhor_movimento = possibilidade
    
    elif(jogador == 0):
      if(valor > melhor_valor):
        melhor_valor = valor
        melhor_movimento = possibilidade
    
    elif(jogador == 1):
      if(valor < melhor_valor):
        melhor_valor = valor
        melhor_movimento = possibilidade

  return melhor_movimento[0], melhor_movimento[1]


score = {
    "DRAW": 0,
    "X": 1,
    "O": -1
}


def minimax(board, jogador, profundidade = 1):
  boardd = ttt()
  boardd.board = board
  ganhador = ttt.verificaGanhador(boardd)

  if ganhador:
    return score[ganhador] / profundidade
  
  jogador = (jogador + 1) % 2

  possibilidades = getPosicoes(board)
  melhor_valor = None

  for possibilidade in possibilidades:
    board[possibilidade[0]][possibilidade[1]] = token[jogador]
    valor = minimax(board, jogador, profundidade + 1)
    board[possibilidade[0]][possibilidade[1]] = branco

    if(melhor_valor is None):
      melhor_valor = valor
    
    elif(jogador == 0):
      if(valor > melhor_valor):
        melhor_valor = valor
    
    elif(jogador == 1):
      if(valor < melhor_valor):
        melhor_valor = valor

  return melhor_valor