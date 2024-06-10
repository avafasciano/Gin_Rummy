"""
This module contains the main controller for a Gin-Rummy game.
Note: We will start by creating an instance of Game in terminal and simply playing between 2 humans through there.
"""

import random
import round
import player
import sys


class Game:
    """
    A class used to represent a game.
    Attributes
    ----------
        playerAScore : int
        playerBScore : int
        roundCount : int
    Methods
    -------
        play(playerA, playerB)
            randomly chooses a player to go first. facilitates rounds until a player reaches 100 points.
            Returns winner.
    """

    def __init__(self):
        self.winner = None
        self.roundCount = 0
        self.totalMoves = 0

    def opposite_player(self, current, playerA, playerB):
        '''
        Helper to get the opposite player
        '''
        if current == playerA:
            return playerB
        else:
            return playerA

    def play(self, playerA: player.Player, playerB: player.Player):
        '''
        nextMover = ;; randomly chose between player A and B
        while (playerAScore < 100 && playerBScore < 100) {
            roundCount++
        round = new Round(nextMover, firstMover.opposite())
            nextMover = round.play(nextMover, oppositePlayer(nextMover));	;; Round.play() returns winner
        }
        logGame()
        '''

        # randomly pick first mover
        players = [playerA, playerB]
        random.shuffle(players)
        next_mover = players[0]

        while playerA.get_points() < 100 and playerB.get_points() < 100:
            # opponent =
            self.roundCount += 1
            new_round = round.Round()
            # next mover is winner of round
            next_mover = new_round.play(
                next_mover, self.opposite_player(next_mover, playerA, playerB))
            self.totalMoves += new_round.get_total_moves()

        if playerA.get_points() > playerB.get_points():
            # player A reaches 100 points and wins game
            self.winner = playerA
        else:
            self.winner = playerB


with open('results.txt', 'w') as f:
    for i in range(20):
        game1 = Game()
        player1 = player.AvaComputerPlayer()
        player2 = player.AvaComputerPlayer()
        # set players names
        player1.set_name("Ava\'s Computer Player 1")
        player2.set_name("Ava\'s Computer Player 2")

        game1.play(player1, player2)
        # eventually log this in a text file
        average_moves = int(game1.totalMoves / game1.roundCount)
        game_num = str(i)
        if i < 10:
            game_num += ' '
        f.write("GAME: " + game_num + "\t WINNER: " + game1.winner.get_name() +
                "\t ROUNDS: " + str(game1.roundCount) + "\t AVG MOVES PER ROUND: " + str(average_moves) + '\n')
