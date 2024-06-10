# can be human or computer
# computer can be hand-build strategy or ML
# should not have access to newCardPile or discardPile directly
# but is informed of the opponent’s move through moves.last()
import move
import card
import hand
import numpy as np

EARLY_DEADWOOD_THRESHOLD = 10
MID_DEADWOOD_THRESHOLD = 5
LATE_DEADWOOD_THRESHOLD = 3


class Player:
    """
    The player class represents a player, who is either a human or a computer.
    Attributes
    ----------
    points : int
    hand : Hand
    """

    def __init__(self):
        self.points = 0
        self.name = ""
        self.hand = hand.Hand()  # Hand

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_points(self, p: int):
        '''
        adds new points to ponits attribute
        '''
        self.points = self.points + p

    def get_points(self):
        '''
        returns player's points
        '''
        return self.points

    def clear_hand(self):
        self.hand = hand.Hand()


class ComputerPlayer(Player):
    '''
    TODO write computer player methods and init f
    attribtues
    ---------
    Hand

    methods
    -------
    pickup_discard_or_pass(self, discard_top: card.Card, hand: hand.Hand)
    pickup_discard_or_new(self, discard_top: card.Card, hand: hand.Hand)
    set_discard_or_fold(self, hand: hand.Hand, move: move.Move)

    '''


class HumanPlayer(Player):
    '''
    subclass of Player for a human player
    '''

    def string_to_card(self, string):
        suits = ["H", "D", "C", "S"]
        ranks = ["A", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "J", "Q", "K"]
        r = ranks.index(string[:-1])
        s = suits.index(string[-1])
        return card.Card(s, r)

    def pickup_discard_or_pass(self, discard_top: card.Card, hand: hand.Hand):
        '''
        a function that  prints the top dicard to the human, asks them if they want to pickup discard or pass, 
        and returns a Move object
        '''
        print('--------------------' + self.name + ' hand--------------------')
        print(hand.display())
        print('------------------------------------------------------')
        print("discard is: " + discard_top.display())
        print("Do you want to \'pickup\' discard or \'pass\'? ")
        choice = input()
        if choice == 'pickup':
            current_move = move.Move(self, "pickupDiscard", None)
            return current_move
        else:
            current_move = move.Move(self, "pass", None)
            return current_move
            # create a move object and make the move_type pass and discard card null and player self

    def is_discard_in_hand(self, this_hand: hand.Hand, card: card.Card):
        '''
        helper for validating discard
        '''
        s = card.get_suit()
        r = card.get_rank()
        if this_hand.hand[s][r] == 1:
            return True
        return False

    def set_discard_or_gin(self, hand: hand.Hand, move: move.Move, moves: list):
        '''
        sets the move.discard to the card picked by the player
        validate that card is in player's hand
        '''
        set_discard_or_gin = False
        hand.display()
        while set_discard_or_gin is False:
            print(
                'Enter the card from you hand which you\'d like to discard, \'gin\' or \'knock\'')
            choice = input()
            if choice == 'gin':
                move.set_type('gin')
                move.set_fold_true()
                set_discard_or_gin = True

            elif choice == 'knock':
                move.set_type('knock')
                move.set_fold_true()
                print(self.name + ' folded')
                set_discard_or_gin = True
            else:
                discard_card = self.string_to_card(choice)
                if self.is_discard_in_hand(hand, discard_card):
                    move.set_discard(discard_card)
                    set_discard_or_gin = True
                else:
                    print('This card is not in your hand')

    def pickup_discard_or_new(self, discard_top: card.Card, hand, last_move: move.Move):
        '''
        function that prompts the human player to either pickup discard or new card, returning a move object based on their choice
        '''
        print('--------------------' + self.name + ' hand--------------------')
        print(hand.display())
        print('-------------------------------------------------------')
        print('\'pickup\'', end=" ")
        print(discard_top.display(), end=" ")
        print('or \'new card\'')
        choice = input()

        if choice == 'pickup':
            #print('Enter the card from you hand which you\'d like to discard')
            #discard = input()
            current_move = move.Move(
                self, "pickupDiscard", None)
            return current_move

        elif choice == 'new card':
            current_move = move.Move(
                self, "pickupNewCard", None)
            return current_move

        else:
            print('re-enter choice')
            # TODO handle incorrect user input


class AvaComputerPlayer(Player):
    '''
    subclass of player for ava's computer strategy
    attribtues
    ---------
    Hand

    methods
    -------
    pickup_discard_or_pass(self, discard_top: card.Card, hand: hand.Hand)
    pickup_discard_or_new(self, discard_top: card.Card, hand: hand.Hand)
    set_discard_or_gin(self, hand: hand.Hand, move: move.Move)
    '''

    def calc_hand_scores(self):
        '''
        return 2d array
        HandScores (4 x 13 array of int…not limited to any value range, IDEA = each non-zero value in a 
        completed HandScores is the HandScore assuming you have DISCARDED that card, and picked up the discard, 
        in other words you’re looking to discard the card associated with the worst scoring hand)
        '''
        hand_scores = np.zeros_like(self.hand.get_hand_array())
        # for each card in hand, remove it and calc hand_score
        # cald hand score assuming you have discarded that card. that is the
        rank = len(hand_scores[0])
        suit = len(hand_scores)
        for s in range(suit):
            for r in range(rank):
                if self.hand.get_hand_array()[s][r] == 1:
                    c = card.Card(s, r)
                    discard = self.hand.remove_card(card=c)
                    score = self.hand.score_hand()
                    self.hand.add_card(discard)
                    hand_scores[s][r] = score
        return hand_scores

    def find_best_discard(self):
        '''
        returns the card that is the best to discard out of every card in hand 
        and returns score of hand after removing that card
        '''
        hand_scores = self.calc_hand_scores()
        max = -100
        for s in range(len(hand_scores)):
            for r in range(len(hand_scores[0])):
                if hand_scores[s][r] != 0 and hand_scores[s][r] > max:
                    max = hand_scores[s][r]
                    max_s = s
                    max_r = r
        c = card.Card(max_s, max_r)
        #print('computer best discard: ' + c.display())
        return [c, max]

    def pickup_discard_or_pass(self, discard_top: card.Card, hand: hand.Hand):
        '''
        Compare HandScores.findBestDiscard() with Hand.ScoreHand() assuming no discard-pickup/pass. 
        If the findBestDiscard has a higher score, pickup the discard. Otherwise pass.
        return new move object
        '''
        # hand score if pass
        #print("PICKUP NEW CARD OR PASS")
        # print(hand.display())
        current_hand_score = hand.score_hand()
        hand.add_card(discard_top)
        # hand score if pick up discard
        pickup_discard_score = self.find_best_discard()[1]
        hand.remove_card(discard_top)
        if pickup_discard_score > current_hand_score:
            #print('computer decided to pickup discard')
            return move.Move(self, "pickupDiscard", None)
        else:
            #print('computer passed')
            return move.Move(self, 'pass', None)

    def pickup_discard_or_new(self, discard_top: card.Card, hand: hand.Hand, last_move: move.Move):
        '''
        Compare HandScores.findBestDiscard() with Hand.ScoreHand() assuming no discard-pickup/pass. 
        If the findBestDiscard has a higher score, pickup the discard. Otherwise pickup new.
        return move
        '''
        #print('PICKUP DISCARD OR NEW')
        # print(hand.display())
        # hand score without discard
        current_hand_score = hand.score_hand()
        hand.add_card(discard_top)
        # hand score if pick up discard
        pickup_discard_score = self.find_best_discard()[1]
        hand.remove_card(discard_top)
        if pickup_discard_score > current_hand_score:
            #print('computer decided to pickup discard')
            return move.Move(self, "pickupDiscard", None)
        else:
            #print('computer decided to pickup new card')
            return move.Move(self, 'pickupNewCard', None)

    def set_discard_or_gin(self, hand: hand.Hand, move: move.Move, moves: list):
        '''
        •	The Hand has 11 cards now, because you have either picked up the discard, or the new card.
        •	If you picked up the discard, you already know which card to put down (from findBestDiscard()).
        •	If you picked up the new card, run findBestDiscard() on the hand with the new card in it.

        Then determine move:
        •	If Gin hand…then gin…duh!
        •	If early game, knock if deadwood < deadwood_threshold = 10
        •	If mid game, deadwood_threshold = 5
        •	If late game, deadwood_threshold = 3

        Early game = 0..5 moves
        Mid game = 6..10 moves
        Late game  > 10 moves
        '''
        #print('DISCARD OR FOLD')
        # print(hand.display())
        game_length = len(moves)
        best_melds = hand.find_best_melds(hand.find_melds(), [], 0)[0]
        deadwood = hand.calc_unmatched_card_values(
            best_melds) - hand.get_highest_card_value(best_melds)
        # see if gin hand... hand has 11 cards and removing highest unmatched = 0
        if deadwood == 0:
            move.set_type('gin')
            move.set_fold_true()
        elif game_length <= 5 and deadwood < EARLY_DEADWOOD_THRESHOLD:
            move.set_type('knock')
            move.set_fold_true()
        elif game_length <= 10 and deadwood < MID_DEADWOOD_THRESHOLD:
            move.set_type('knock')
            move.set_fold_true()
        elif game_length > 10 and deadwood < LATE_DEADWOOD_THRESHOLD:
            move.set_type('knock')
            move.set_fold_true()
        else:
            # discard
            discard = self.find_best_discard()[0]
            #print("computer chose to discard: " + discard.display())
            move.set_discard(discard)
