import player
import deck
import pile
import card
import move

# constants
GIN_POINTS = 20
KNOCK_POINTS = 10


class Round():
    """
    A class used to represent one round of a game.
    Attributes
    ----------
        new_card_pile : Deck
        discard_pile : DiscardPile
        round_winner : Player
        moves : list of moves since start of the game

    Methods
    -------
        play(player_A, player_B)
            Player A moves first. Keep switching players until someone folds. Validate fold.
            Scores the hands and returns round winner.
    """

    def __init__(self):

        self.new_card_pile = deck.Deck()
        self.discard_pile = pile.DiscardPile()
        self.round_winner = None
        self.moves = [move.Move]

    def get_total_moves(self):
        '''
        for displaying average
        '''
        return len(self.moves)

    def score_round(self, last_mover: player.Player, opponent: player.Player):
        '''
        The player who makes Gin, scores 20 points plus the value of the opponent’s unmatched cards.
        If the player who Knocks wins the game, they score the difference in the value of
        their unmatched cards with those of their opponent,
        while if the opponent wins, they score 10 points plus the difference in the value of
        the unmatched cards between both players. If there is no difference, the 10 point bonus remains

        this function assigns points to each player according to moves last
        it also assigns a round winner to the round
        '''

        last_move = self.moves.pop()
        op_best_melds = opponent.hand.find_best_melds(
            opponent.hand.find_melds(), [], 0)[0]
        # error
        op_unmatched_card_value = opponent.hand.calc_unmatched_card_values(
            op_best_melds)
        last_mover_best_melds = last_mover.hand.find_best_melds(
            last_mover.hand.find_melds(), [], 0)[0]
        if last_move.get_type() == 'gin':
            # validate gin
            if last_mover.hand.validate_gin(last_mover_best_melds):
                last_mover.set_points(GIN_POINTS + op_unmatched_card_value)
                self.round_winner = last_mover
            else:
                # print(last_mover.get_name() +
                # ' does not have a valid gin hand. Opponent wins')
                self.round_winner = opponent
        elif last_move.get_type() == 'knock':
            last_mover_unmatched_value = last_mover.hand.calc_unmatched_card_values(
                last_mover_best_melds)
            last_mover_highest_card = last_mover.hand.get_highest_card_value(
                last_mover_best_melds)
            # The player wins if the value of their unmatched cards is less than the value of the opponent’s unmatched cards
            if last_mover_unmatched_value - last_mover_highest_card < op_unmatched_card_value:
                self.round_winner = last_mover
                last_mover.set_points(
                    op_unmatched_card_value - last_mover_unmatched_value - last_mover_highest_card)
            # opponent wins if the value of their unmatched cards is equal to or less than that of the one that Knocked
            else:
                self.round_winner = opponent
                opponent.set_points(
                    KNOCK_POINTS + last_mover_unmatched_value - op_unmatched_card_value - opponent.hand.get_highest_card_value(op_best_melds))

    # player: player.Player):

    def replace(self, next_mover: player.Player, removed_card: card.Card, move: move.Move):
        '''
        helper to add picked card to player's hand
        set move discard
        remove discard from player's hand
        add discard to discard pile
        '''
        next_mover.hand.add_card(removed_card)
        next_mover.set_discard_or_gin(next_mover.hand, move, self.moves)
        if move.fold is False:
            next_mover.hand.remove_card(move.discard)
            self.discard_pile.add_card(move.discard)

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
        Function to play a round between any 2 players
        sets each players points after round ends
        returns round winner
        '''
        # add dealt cards to each players hands
        playerA.hand.deal(self.new_card_pile)
        playerB.hand.deal(self.new_card_pile)
        # add a card from new card pile to discard
        self.discard_pile.add_card(self.new_card_pile.remove_top())
        next_mover = playerA
        move = next_mover.pickup_discard_or_pass(
            self.discard_pile.get_top_card(), next_mover.hand)

        self.moves.append(move)
        if move.type == "pickupDiscard":
            removed_top_of_discard = self.discard_pile.remove_top()
            self.replace(next_mover, removed_top_of_discard, move)
            next_mover = self.opposite_player(next_mover, playerA, playerB)
        else:
            print('-------------')
            print('SWITCH PLAYER')
            print('-------------')
            # player 1 passes, second mover either picks up new card or passes
            next_mover = self.opposite_player(next_mover, playerA, playerB)
            move = next_mover.pickup_discard_or_pass(
                self.discard_pile.get_top_card(), next_mover.hand)
            # eventually validate move and throw error
            self.moves.append(move)
            if move.type == "pickupDiscard":
                removed_top_of_discard = self.discard_pile.remove_top()
                self.replace(next_mover, removed_top_of_discard, move)
                next_mover = self.opposite_player(next_mover, playerA, playerB)

        # Keep switching turns until you run out of new cards, or someone folds (knocks or gins)
        while not move.fold and len(self.new_card_pile.deck) != 0:
            print('-------------')
            print('SWITCH PLAYER')
            print('-------------')
            move = next_mover.pickup_discard_or_new(
                self.discard_pile.get_top_card(), next_mover.hand, self.moves[-1])
            if move.type == "pickupNewCard":
                removed_top_of_new_card_pile = self.new_card_pile.remove_top()
                self.replace(next_mover, removed_top_of_new_card_pile, move)
                self.moves.append(move)

            elif move.type == "pickupDiscard":
                # player picked discard and we must put their card at the top of the discard pile
                removed_top_of_discard = self.discard_pile.remove_top()
                self.replace(next_mover, removed_top_of_discard, move)
                self.moves.append(move)
            else:
                print('error')
            next_mover = self.opposite_player(next_mover, playerA, playerB)

        # round is over, score hands and update player's points, assign round winner
        op = self.opposite_player(
            next_mover, playerA, playerB)
        self.score_round(op, next_mover)
        loser = self.opposite_player(
            self.round_winner, playerA, playerB)
        print('Winner: ' + self.round_winner.get_name() +
              ', score: ' + str(self.round_winner.get_points()))
        print('Loser: ' + loser.get_name() +
              ', score: ' + str(loser.get_points()))
        playerA.clear_hand()
        playerB.clear_hand()
        return(self.round_winner)


# PRINTLINE TESTNG
player1 = player.HumanPlayer()
player2 = player.HumanPlayer()

player1.set_name('Player 1')
player2.set_name('Player 2')

round1 = Round()
round1.play(player1, player2)
