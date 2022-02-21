# -*- coding: utf-8 -*-
"""

IA - Jogo da Velha.ipynb

# Jogo para dois jogadores - Jogo da Velha

"""
import os

def clear():
  os.system('cls' if os.name == 'nt' else 'clear') or None

branco = " "
token = ["X", "O"]

class TicTacToe:
  def __init__(self):
    self.board = [[branco] * 3 for n in range(3)]


  def printBoard(self):
    print("\n########################")
    print("------ Your board ------\n")
    for i in range(3):
      print(" | ".join(self.board[i]))

      if(i < 2):
        print("---------")

    print("\n########################\n")


  def getInputValido(mensagem):
    while True:
      try:
        n = int(input(mensagem))

        if(n >= 1 and n <= 3):
          break
        
        else:
          print("SophLia: Enter a number between 1 and 3.")
      
      except:
        print("SophLia: This is not a valid number.")
        pass
    
    return n - 1


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

    return "DRAW"