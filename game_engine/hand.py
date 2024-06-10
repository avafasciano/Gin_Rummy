import random
import deck
import math
import card
import numpy as np


class Hand:
    """
    class to represent a player's hand, which includes 10 cards
    initialize using random.
    4 x 13 matrix of Booleans. if card in a player's hand, then that element in the matrix is set to True.
    10 elements should be True after a player makes a move

    Attributes
    ----------
    hand - matrix of cards
    top - tuple indicating position of top card (the card added last)

    Methods
    -------
    add_card
    deal
    remove_card
    display
    find_melds
    find_max_melds
    calculate_score
    """

    def __init__(self, array=np.array([])):
        """
        initialize a 4x13 matrix of 0s
        """
        x = np.arange(52)
        x = x.reshape((4, 13))
        if array.size != 0:
            self.hand = array
        else:
            self.hand = np.zeros_like(x)
        self.top = (0, 0)

    def get_hand_array(self):
        return self.hand

    def is_10_cards(self):
        '''
        helper for add_card to count number of cards in hand (specifically for throwing eception)
        returns True if 10 or less cards
        '''
        rows = len(self.hand)
        cols = len(self.hand[0])
        count = 0
        for r in range(rows):
            for c in range(cols):
                if self.hand[r][c] != 0:
                    count += 1
        return count <= 11

    def add_card(self, card: card):
        """
        throw exception if more than 11 cards
        """
        if not self.is_10_cards():
            raise NameError('Already more than 10 cards in hand')
        else:
            s = card.get_suit()
            v = card.get_rank()
            self.hand[s][v] = 1
            self.top = (s, v)

    def deal(self, d: deck):
        '''
        TODO
        deal cards from deck to hand
        this deals 10 cards from the deck that is already shuffled
        calls remove_top from deck
        '''
        for i in range(10):
            self.add_card(d.remove_top())

    def remove_card(self, card):
        """
        TODO
        remove card from hand and return that card
        if card does not exist throw an error
        """
        s = card.get_suit()
        v = card.get_rank()
        if self.hand[s][v] == 0:
            raise NameError('Card does not exist in hand')
        else:
            self.hand[s][v] = 0
            return card

    def display(self):
        '''
        pretty print hand
        '''
        # print(self.hand)
        col_label = ['H', 'D', 'C', 'S']
        print()
        print('  A   2   3   4   5   6   7   8   9   10  J   Q   K')
        # add col label to front of each row
        i = 0
        n = len(self.hand)
        for r in range(n):
            string = col_label[i] + " "
            for e in range(len(self.hand[0])):
                if self.hand[r][e] < 10:
                    string += str(self.hand[r][e]) + '   '
                else:
                    string += str(self.hand[r][e]) + '  '
            print(string)
            i += 1
        return ""

    def to_card(self, x, y):
        '''
        helper to convert element in hand matrix to card
        '''
        return card.Card(x, y, self.hand[x][y])

    def print_meld(self, meld):
        string = "["
        for card in meld:
            string = string + card.display() + " "
        print(string + "]")
        return

    def find_melds(self):
        '''
        for scoring
        returns all sequences of cards values that qualify as a meld
        '''
        # first look for all same suit melds
        # list of lists of cards
        melds = []
        r = 0
        for row in self.hand:
            # get each increment of 3 and see if they are all nonzero
            # not working yet
            for c in range(len(row)-2):
                # print(str(self.hand[r][c]) + ' ' + str(self.hand[r][c+1]) + ' ' + str(self.hand[r][c+2]))
                if self.hand[r][c] != 0 and self.hand[r][c+1] != 0 and self.hand[r][c+2] != 0:
                    # print('flag 3 of same suit')
                    card1 = self.to_card(r, c)
                    card2 = self.to_card(r, c+1)
                    card3 = self.to_card(r, c+2)
                    melds.append([card1, card2, card3])
            # get each increment of 4 and see if they are all nonzero
            for co in range(len(row)-3):
                if self.hand[r][co] != 0 and self.hand[r][co+1] != 0 and self.hand[r][co+2] != 0 and self.hand[r][co+3] != 0:
                    # print('flag 4 of same suit')
                    card1 = self.to_card(r, co)
                    card2 = self.to_card(r, co+1)
                    card3 = self.to_card(r, co+2)
                    card4 = self.to_card(r, co+3)
                    melds.append([card1, card2, card3, card4])
            # increments of 5
            for col in range(len(row)-4):
                if self.hand[r][col] != 0 and self.hand[r][col+1] != 0 and self.hand[r][col+2] != 0 and self.hand[r][col+3] != 0 and self.hand[r][col+4] != 0:
                    card1 = self.to_card(r, col)
                    card2 = self.to_card(r, col+1)
                    card3 = self.to_card(r, col+2)
                    card4 = self.to_card(r, col+3)
                    card5 = self.to_card(r, col+4)
                    melds.append([card1, card2, card3, card4, card5])

            # note that any other meld size can be a sum of meld these meld sizes
            r += 1

        # now loop through each columns and see how many 1's are in each-
        #   if 3, add all those cards to list
        #   elif 4, add 4 lists of 3 and one of 4
        # WORKS
        hand_t = np.transpose(self.hand[:])
        cols = len(hand_t)
        rows = len(hand_t[0])
        for c in range(cols):
            count = 0
            for e in range(rows):
                if hand_t[c][e] != 0:
                    count += 1
            if count == 3:
                # print('flag: 3 in colum')
                cards = []
                for el in range(rows):
                    if hand_t[c][el] != 0:
                        cards.append(self.to_card(el, c))
                melds.append(cards)
            if count == 4:
                # print('flag: 4 in column')
                melds.append([self.to_card(0, c), self.to_card(
                    1, c), self.to_card(2, c), self.to_card(3, c)])
                melds.append(
                    [self.to_card(0, c), self.to_card(2, c), self.to_card(3, c)])
                melds.append(
                    [self.to_card(0, c), self.to_card(1, c), self.to_card(3, c)])
                melds.append(
                    [self.to_card(1, c), self.to_card(2, c), self.to_card(3, c)])
                melds.append(
                    [self.to_card(0, c), self.to_card(1, c), self.to_card(2, c)])

        return melds

    def compare_cards(self, c1, c2):
        '''
        helper for checking if cards have same value and suit
        '''
        if c1.get_suit() == c2.get_suit() and c1.get_rank() == c2.get_rank():
            return True
        return False

    def are_melds_disjoint(self, meld_input, meld_set):
        '''
        helper for find_max_melds
        returns true if no card in meld appears in meldSet
        '''
        for meld in meld_set:
            for card1 in meld:
                for card2 in meld_input:
                    if self.compare_cards(card1, card2):
                        return False
        return True

    def set_melds_to_zero(self, meld_set):
        '''
        helper
        '''
        hand_copy = self.hand.copy()
        for meld in meld_set:
            for card in meld:
                s = card.get_suit()
                v = card.get_rank()
                hand_copy[s][v] = 0
        return hand_copy

    def get_highest_card_value(self, best_meld_set):
        '''
        useful when a player knocks, to exclude this card in the scoring
        returns an int
        '''
        hand_copy = self.set_melds_to_zero(best_meld_set)
        # return the first unmatched largest value
        hand_t = np.transpose(hand_copy)
        cols = len(hand_t)
        rows = len(hand_t[0])
        for c in reversed(range(cols)):
            for e in range(rows):
                if hand_t[c][e] != 0:
                    highest_card = self.to_card(e, c)
                    return highest_card.get_value()
        return 0

    def calc_unmatched_card_values(self, meld_set):
        '''
        returns an int
        make a copy of hand = handCopy
        for each card that appears in meldSet, set that card to zero in handCopy
        return sum of card values in handCopy
        '''
        hand_copy = self.set_melds_to_zero(meld_set)

        total_value = 0
        row = len(hand_copy)
        col = len(hand_copy[0])
        for r in range(row):
            for c in range(col):
                if hand_copy[r][c] == 1:
                    # add card's value + 1 since index starts at 0
                    card1 = self.to_card(r, c)
                    total_value += card1.get_value()
        return total_value

    def validate_gin(self, best_meld_set):
        '''
        ensures hand only has 1 unmatched card
        '''
        hand_copy = self.set_melds_to_zero(best_meld_set)
        count_unmatched = 0
        row = len(hand_copy)
        col = len(hand_copy[0])
        for r in range(row):
            for c in range(col):
                if hand_copy[r][c] == 1:
                    count_unmatched += 1
        if count_unmatched == 1:
            return True
        return False

    def string_meld_helper(self, melds):
        '''
        pretty print melds
        '''
        string = "["
        for meld in melds:
            for card in meld:
                string = string + card.display() + " "
            string += '| '
        return string + "]"

    def find_best_melds(self, all_meld_set, trial_best_meld_set, level):
        '''
        Recursively find MeldSet with the lowest unmatched card values

        '''
        # print("---- STARTING FIND_BEST_MELDS LEVEL = " + str(level))
        # print("ALL_MELD_SET = " + self.string_meld_helper(all_meld_set))
        # print("TRIAL_BEST_MELD_SET = " +
        # self.string_meld_helper(trial_best_meld_set))

        if len(all_meld_set) == 0:
            # print("** TRIAL_BEST_MELD_SET = " +
            # self.string_meld_helper(trial_best_meld_set))
            unmatched_value = self.calc_unmatched_card_values(
                trial_best_meld_set)

            # print("BASE CASE VALUE = " + str(unmatched_value))
            return [trial_best_meld_set, unmatched_value]
        else:
            if trial_best_meld_set:
                trial_best_meld_set_1 = trial_best_meld_set.copy()
                trial_best_meld_set_2 = trial_best_meld_set.copy()
            else:
                trial_best_meld_set_1 = []
                trial_best_meld_set_2 = []

            # Find best meld set including first meld
            # get first meld from list of all melds
            # print("-- FIRST BLOCK...")
            first_meld = all_meld_set[0]
            # print("FIRST_MELD = ")
            # self.print_meld(first_meld)

            if self.are_melds_disjoint(first_meld, trial_best_meld_set_1):
                # copy and remove first meld
                # print("-- FIRST MELD IS DISJOINT")
                all_meld_set_1 = all_meld_set[:]
                all_meld_set_1.pop(0)
                trial_best_meld_set_1.append(first_meld)
                [meld_set_1, meld_set_value_1] = self.find_best_melds(
                    all_meld_set_1, trial_best_meld_set_1, level+1)
            else:
                # firstMeld contains cards in trialBestMeldSet, so ignore
                # print("-- FIRST MELD IS NOT DISJOINT")
                meld_set_value_1 = math.inf

            # Find best meld set excluding first meld
            # print("-- SECOND BLOCK...")
            all_meld_set_2 = all_meld_set.copy()
            all_meld_set_2.pop(0)
            [meld_set_2, meld_set_value_2] = self.find_best_melds(
                all_meld_set_2, trial_best_meld_set_2, level+1)

            # Return best meld set
            if meld_set_value_1 < meld_set_value_2:
                # print("BEST MELD SET IS = " +
                # self.string_meld_helper(meld_set_1))
                # print("BEST MELD SET VALUE = " + str(meld_set_value_1))
                return [meld_set_1, meld_set_value_1]
            else:
                # print("BEST MELD SET IS = " +
                # self.string_meld_helper(meld_set_2))
                # print("BEST MELD SET VALUE = " + str(meld_set_value_2))
                return [meld_set_2, meld_set_value_2]

    # ----- hand functions for Ava's computer player
    def calc_rank_match(self, rank: int):
        '''
        how many cards of the given suit are there in
        0,2,3, or 4 if there is a match of 2 cards, 3, 4 etc
        '''
        hand_t = np.transpose(self.hand)
        count = 0
        for el in hand_t[rank]:
            if el == 1:
                count += 1
        return count

    def calc_suit_runs(self, suit: int):
        '''
        returns LIST of 0, 2..13 for each run of that given suit
        '''
        output = []
        suit_list = self.hand[suit]
        n = len(suit_list)
        count = 0
        for i in range(n):
            if suit_list[i] == 1:
                count += 1
                # if last element
                if i == n-1:
                    output.append(count)
            elif suit_list[i] == 0 and count != 0:
                if count > 1:
                    output.append(count)
                count = 0
        return output

    def score_rank_match(self, c: int):
        '''
        input, result of calc_rank_match
        0 -> 0		
        2 -> 2		“means rank match of 2 scores as 2”
        3 -> 4		“means rank match of 3 scores as 4”
        4 -> 8		“means rank match of 4 scores as 8”
        returns score of rank match
        '''
        if c == 2:
            return 2
        elif c == 3:
            return 4
        elif c == 4:
            return 8
        else:
            return 0

    def score_suit_run(self, c: int):
        '''
        input: result of calc_suit_runs
        return score of given suit run
        ie:
        2 -> 2		“means suit run of 2 scores as 2”
        5 -> 9		“means suit run of 5 scores as 9”
        '''
        if c == 2:
            return 2
        elif c == 3:
            return 4
        elif c == 4:
            return 8
        elif c == 5:
            return 9
        elif c == 6:
            return 10
        elif c == 7:
            return 12
        elif c == 8:
            return 12
        else:
            return 0

    def score_hand(self):
        '''
        build points up for each rank match and suit run, based on the length (irrespective of rank value of cards), then subtract out the deadwood (even if that deadwood is part of a partial match or run)”
        returns evaluation of given hand as an integer
        '''
        score = 0
        rank_len = len(self.hand[0])
        suit_len = len(self.hand)
        for r in range(rank_len):
            score = score + self.score_rank_match(self.calc_rank_match(r))
        for s in range(suit_len):
            run_scores = self.calc_suit_runs(s)
            for run_score in run_scores:
                score = score + self.score_suit_run(run_score)
        score = score - self.calc_unmatched_card_values(self.find_melds())
        return score
