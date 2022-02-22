<p align="center">
  <img src= logo.png />
</p>

<h3 align="center">UNIVERSIDADE FEDERAL DE ALAGOAS - UFAL <br /> INSTITUTO DE COMPUTAÇÃO - IC <br /> Engenharia de Computação</h3 >

---

<h2 align= "center"> Tic Tac Toe </h3>

Repositório relacionado ao projeto do Socket da matéria de Redes de Computadores, ministrada pelo prof. Leandro Salles na UFAL em 2021.1.

### Alunas:

- Karla Sophia Santana da Cruz
- Lilian Giselly Pereira Santos

---

## Descrição

- Com os conceitos de Socket, comunicação Cliente e Servidor e Thread aprendidos durante a matéria de Redes de Computadores, foi escolhido como aplicação de projeto o famoso Jogo da Velha.
- O Jogo da Velha SophLia possui dois _gamemode_:
  - **Modo PvP** ou Multiplayer, quando dois jogadores estão jogando
  - **Modo IA** ou SophLia, quando o jogador irá jogar contra a IA SophLia

---

## Execução

Para a execução será necessária a instalação de python na máquina local.

Em seguida, é hora de executar o código!

Inicialmente, execute o servidor em um terminal rodando os seguintes comandos, respectivamente:

```bash
$ cd src
$ py server.py
```

> É de extrema importância que o servidor seja executado previamente ao cliente.

Em seguida, para executar o cliente, abra um novo terminal e rode os comandos:

```bash
$ cd src
$ py client.py
```

> Caso deseje testar com um novo cliente - fator necessário para o modo de jogo "_Player vs Player_" abra um terceiro terminal e rode os comandos citados novamente.

> Para encerrar um servidor ou cliente, basta digitar os comandos `Ctrl + C` em seu terminal ou simplesmente fechá-lo.

O código foi estruturado de maneira interativa do servidor com o lado do cliente, imprimindo mensagens intuitivas que permitem a condução do jogo, como para saber o nome do jogador, seu modo de jogo escolhido, mensagens informando o resultado, etc.

---

## Desenvolvimento

- O projeto foi desenvolvido utilizando a linguagem de programação Python.
- Para o uso de socket e thread, foram importadas as bibliotecas <code>socket</code> e <code>threading</code>
- Para a execução do **Modo IA**, foi usado o algoritmo Minimax, presente em <code>ia.py</code>
- A classe **Tic Tac Toe** em <code>tictactoe.py</code> possui toda a lógica de jogo usada na aplicação

Agora, divita-se!
