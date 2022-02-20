# -*- coding: utf-8 -*-
"""

IA - Jogo da Velha.ipynb

# Jogo para dois jogadores - Jogo da Velha

"""

branco = " "
token = ["X", "O"]

class TicTacToe:
  def __init__(self):
    self.board = [[branco] * 3 for n in range(3)]


  def printBoard(self):
    for i in range(3):
      print("|".join(self.board[i]))

      if(i < 2):
        print("------")


  def getInputValido(mensagem):
    try:
      n = int(input(mensagem))

      if(n >= 1 and n <= 3):
        return n - 1
      
      else:
        print("Numero precisa estar entre 1 e 3")

        return getInputValido(mensagem)
    
    except:
      print("Numero nao valido")

      return getInputValido(mensagem)


  def verificaMovimento(self, i, j):
    if(self.board[i][j] == branco):
      return True
    
    else:
      return False


  def fazMovimento(self, i, j, jogador):
    self.board[i][j] = token[jogador]


  def verificaGanhador(self):
    for i in range(3):
      if(self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2] and self.board[i][0] != branco):
        return self.board[i][0]
    
    for i in range(3):
      if(self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i] and self.board[0][i] != branco):
        return self.board[0][i]
      
    if(self.board[0][0] != branco and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]):
      return self.board[0][0]

    if(self.board[0][2] != branco and self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]):
      return self.board[0][2]
    
    for i in range(3):
      for j in range(3):
        if(self.board[i][j] == branco):
          return False

    return "EMPATE"

  def __str__(self):
    str = ''
    for i in range(3):
      str += ("|".join(self.board[i]))

      if(i < 2):
        str += ("\n------")
    
    return str


  """ 
  jogador = 0
  self.board = criarBoard()
  ganhador = verificaGanhador(self.board)

  while(not ganhador):
    printBoard(self.board)
    print("=========================")

    if(jogador == 0):
      i, j = movimentoIA(self.board, jogador)
      #i = getInputValido("Digite a linha: ")
      #j = getInputValido("Digite a coluna: ")
    
    else:
      i, j = movimentoIA(self.board, jogador)
      #i = getInputValido("Digite a linha: ")
      #j = getInputValido("Digite a coluna: ")
      
    
    if(verificaMovimento(self.board, i, j)):
      fazMovimento(self.board, i, j, jogador)
      jogador = (jogador + 1) % 2

    else:
      print("A posicao informada ja esta ocupada")
    
    ganhador = verificaGanhador(self.board)

  print("=========================")
  printBoard(self.board)
  print("Ganhador = ", ganhador)
  print("=========================")
  """