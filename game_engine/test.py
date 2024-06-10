import unittest
import hand
import card
import pile
import deck
import player
import numpy as np


class TestHandMethods(unittest.TestCase):
    '''
    class for testing hand methods
    '''

    def test_add_card(self):
        '''test case for add_card() method'''
        print("testing add_card")
        hand_array = np.array([
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]])
        result1 = np.array([
            [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]])
        result2 = np.array([
            [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]])
        hand1 = hand.Hand(array=hand_array)
        card1 = card.Card(0, 0)
        card2 = card.Card(3, 12)
        hand1.add_card(card1)
        self.assertTrue(np.array_equal(hand1.hand, result1,
                        equal_nan=True), "failed to add ace of hearts")
        hand1.add_card(card2)
        self.assertTrue(np.array_equal(hand1.hand, result2,
                        equal_nan=True), "failed to add king of spades")

        hand2 = hand.Hand()
        hand2.add_card(card1)
        self.assertEqual(
            hand2.hand[0][0], 1, "failed to represent card as 1 in the array")

    def test_deal(self):
        '''
        test that there are 10 cards in hand after deal is called
        also test that there are 10 less cards in the deck
        '''
        print("testing deal")
        hand1 = hand.Hand()
        d = deck.Deck()
        hand1.deal(d)
        count = 0
        for r in range(len(hand1.hand)):
            for c in range(len(hand1.hand[0])):
                if hand1.hand[r][c] > 0:
                    count += 1
        self.assertEqual(count, 10, "fail to deal 10 cards")
        self.assertEqual(
            len(d.deck), 42, "fail to remove 10 cards from deck during deal")

    def test_remove_card(self):
        '''
        test remove_card method in hand- make sure it returns card and removes card in hand
        '''
        print("testing remove")
        hand_array = np.array([
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]])
        result = np.array([
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]])
        hand1 = hand.Hand(array=hand_array)
        card1 = card.Card(1, 11)
        return_card = hand1.remove_card(card1)
        self.assertTrue(np.array_equal(
            a1=hand_array, a2=result), "remove unsuccessful")
        self.assertEqual(return_card, card1, "does not return card")

    def print_meld_helper(self, melds):
        '''
        pretty print melds
        '''
        for meld in melds:
            for card in meld:
                print(card.display())
            print('---')

    def test_meld_functions(self):
        '''
        test find_melds and find_max_melds
        '''
        print("test find_melds")
        # -------HAND 1----------
        hand_array_1 = np.array([
            [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ])
        hand1 = hand.Hand(hand_array_1)
        two_h = card.Card(0, 1)
        three_h = card.Card(0, 2)
        four_h = card.Card(0, 3)
        five_h = card.Card(0, 4)
        eight_h = card.Card(0, 7)
        nine_h = card.Card(0, 8)
        ten_h = card.Card(0, 9)
        eight_d = card.Card(1, 7)
        eight_s = card.Card(3, 7)

        meld1 = [eight_h, eight_d, eight_s]
        meld2 = [two_h, three_h, four_h]
        meld3 = [three_h, four_h, five_h]
        meld4 = [two_h, three_h, four_h, five_h]
        meld5 = [eight_h, nine_h, ten_h]

        melds_list = [meld1, meld2, meld3, meld4, meld5]
        melds = hand1.find_melds()

        self.assertEqual(
            len(melds), len(melds_list), "failure to compute the correct number of melds")

        not_disjoint = hand1.are_melds_disjoint(meld1, melds_list)
        self.assertFalse(not_disjoint, "failure to find non-disjoint melds")
        disjoint = hand1.are_melds_disjoint(meld1, [meld2, meld3, meld4])
        self.assertTrue(disjoint, "failed to find disjoint melds")

        best_melds_result = [meld4, meld5]
        trial_melds = [meld2, meld5]
        self.assertEqual(hand1.calc_unmatched_card_values(trial_melds), 31)
        best_melds_unmatched = hand1.calc_unmatched_card_values(
            best_melds_result)
        self.assertEqual(best_melds_unmatched, 26,
                         "failed to calc unmatched cards: you got " + str(best_melds_unmatched))

        [best_meld_set, best_meld_set_value] = hand1.find_best_melds(melds, [
        ], 0)
        self.assertEqual(best_meld_set_value, 26,
                         "hand1: failure to get meld set with minimum value unmatched cards")
        # ------------HAND 2--------------
        hand_array_2 = np.array([
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        ])
        hand2 = hand.Hand(array=hand_array_2)
        [best_meld_set_2, best_meld_set_value_2] = hand2.find_best_melds(
            hand2.find_melds(), [], 0)
        self.assertEqual(best_meld_set_value_2, 10,
                         "hand2: failure to get meld set with minimum value unmatched cards")
        # ------------HAND 3----------------
        hand_array_3 = np.array([
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        hand3 = hand.Hand(array=hand_array_3)
        [best_meld_set_3, best_meld_set_value_3] = hand3.find_best_melds(
            hand3.find_melds(), [], 0)
        self.assertEqual(best_meld_set_value_3, 9,
                         "hand3: failure to get meld set with minimum value unmatched cards")

        hand_array_4 = np.array([
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        hand4 = hand.Hand(array=hand_array_4)
        meld_set_4 = hand4.find_melds()
        self.assertEqual(hand4.find_best_melds(meld_set_4, [], 0)[1], 8)

    def test_get_highest_card_value(self):
        '''
        test
        '''
        hand_array = np.array([
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        h = hand.Hand(array=hand_array)
        best_meld_set = h.find_best_melds(h.find_melds(), [], 0)[0]
        result = h.get_highest_card_value(best_meld_set)
        self.assertEqual(result, 9)

        hand_array_1 = np.array([
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        h_1 = hand.Hand(array=hand_array_1)
        best_meld_set_1 = h_1.find_best_melds(h_1.find_melds(), [], 0)[0]
        result_1 = h_1.get_highest_card_value(best_meld_set_1)
        self.assertEqual(result_1, 7)

    def test_validate_gin(self):
        '''
        test
        '''
        gin_hand_array = np.array([
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        ])
        gin_hand = hand.Hand(array=gin_hand_array)
        best_meld_set = gin_hand.find_best_melds(
            gin_hand.find_melds(), [], 0)[0]
        self.assertTrue(gin_hand.validate_gin(best_meld_set))

        not_gin_hand_array = np.array([
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        ])
        not_gin_hand = hand.Hand(array=not_gin_hand_array)
        best_meld_set_2 = not_gin_hand.find_best_melds(
            not_gin_hand.find_melds(), [], 0)[0]
        self.assertFalse(not_gin_hand.validate_gin(best_meld_set_2))

    def test_calc_rank_match(self):
        '''
        given rank see if calc_rank_match returns the right score allocated to that number of cards in the match
        '''
        hand_array_1 = np.array([
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        ])
        hand1 = hand.Hand(hand_array_1)
        self.assertEqual(hand1.calc_rank_match(
            1), 2, 'failed to score rank 1 (2s)')
        self.assertEqual(hand1.calc_rank_match(0), 0, 'failed to score Ace')
        self.assertEqual(hand1.calc_rank_match(4), 3, 'failed to score rank 5')
        self.assertEqual(hand1.calc_rank_match(12), 4, 'failed to score King')
        self.assertEqual(hand1.calc_rank_match(10), 1, 'failed to score Jack')

    def test_calc_suit_runs(self):
        '''
        blah
        '''
        hand_array = np.array([
            [1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        ])
        h = hand.Hand(hand_array)
        self.assertEqual(h.calc_suit_runs(0), [2, 3])
        self.assertEqual(h.calc_suit_runs(1), [4])
        self.assertEqual(h.calc_suit_runs(3), [3, 2, 2])

    def test_score_hand(self):
        hand_array_1 = np.array([
            [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        h1 = hand.Hand(hand_array_1)
        result1 = h1.score_hand()
        print("result of score hand 1 (great hand): " + str(result1))
        hand_array_2 = np.array([
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        ])
        h2 = hand.Hand(hand_array_2)
        result2 = h2.score_hand()
        print("result of score hand 2 (bad hand ): " + str(result2))
        hand_array_3 = np.array([
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        h3 = hand.Hand(hand_array_3)
        result3 = h3.score_hand()
        print("result of score hand 3 (ok hand ): " + str(result3))


class TestPileMethods(unittest.TestCase):
    '''
    class for testing pile methods
    '''

    def test_add_card(self):
        '''
        make sure add card add card to pile matrix and assigns top card
        '''
        print('testing add card to pile')
        pile1 = pile.DiscardPile()
        card1 = card.Card(0, 0)
        card2 = card.Card(0, 1)
        pile1.add_card(card1)
        # print(pile1.get_top_card().display())
        self.assertEqual(pile1.get_top_card().get_suit(), 0,
                         "failed to add card to pile")
        self.assertEqual(pile1.get_top_card().get_rank(), 0,
                         "failed to add card to pile")
        pile1.add_card(card2)
        self.assertEqual(pile1.get_top_card().get_suit(), 0,
                         "failed to add card to top of pile, suit is " + str(pile1.get_top_card().get_suit()))
        self.assertEqual(pile1.get_top_card().get_rank(), 1,
                         "failed to add card to top of pile, rank is " + str(pile1.get_top_card().get_rank()))

    def test_remove_card(self):
        '''
        make sure remove card removes top card
        '''
        pile2 = pile.DiscardPile()
        card1 = card.Card(0, 0)
        card2 = card.Card(0, 1)
        card3 = card.Card(1, 1)
        pile2.add_card(card1)
        pile2.add_card(card2)
        pile2.add_card(card3)
        top = pile2.remove_top()
        self.assertEqual(top.display(), "2D", "failed to return top card")
        self.assertEqual(
            pile2.discard_pile[1][1], 0, "failed to remove top card from pile.")
        top_after_remove = pile2.get_top_card()
        # print(top_after_remove.display())

    def test_card_display(self):
        three_of_hearts = card.Card(0, 2)
        # print(three_of_hearts.display())


class TestPlayerMethods(unittest.TestCase):
    '''
    class for testing player methods
    '''

    def display(self, hand):
        '''
        pretty print hand
        '''
        # print(self.hand)
        col_label = ['H', 'D', 'C', 'S']
        print()
        print('  A   2   3   4   5   6   7   8   9   10  J   Q   K')
        # add col label to front of each row
        i = 0
        n = len(hand)
        for r in range(n):
            string = col_label[i] + " "
            for e in range(len(hand[0])):
                if hand[r][e] < 10:
                    string += str(hand[r][e]) + '   '
                else:
                    string += str(hand[r][e]) + '  '
            print(string)
            i += 1
        return ""

    def test_find_best_melds(self):
        ''''
        '''
        pl = player.AvaComputerPlayer()
        arr = np.array([
            [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        h = hand.Hand(arr)
        self.display(pl.calc_hand_scores(h))
        result = pl.find_best_discard(h)
        # print(result[0].display())
        #print('score: ' + str(result[1]))

        # print(self.display(result))
        # print(self.display(h.get_hand_array()))


if __name__ == '__main__':
    unittest.main()
