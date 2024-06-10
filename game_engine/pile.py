import numpy as np
import card


class DiscardPile:
    '''
    4 X 13 matrix of 0s and 1s representing a discard pile. 
    Attributes
    ----------
    discard_pile: 2d array
    top: tuple representing 

    Methods
    -------
    add_card
    remove_card
    get_top

    '''

    def __init__(self):
        '''
        matrix for ML, 4 x 13 matrix of 0s
        '''
        x = np.arange(52)
        x = x.reshape((4, 13))

        self.discard_pile = np.zeros_like(x)
        self.top = (0, 0)

    def display(self):
        '''
        pretty print hand for testing
        '''
        # print(self.hand)
        col_label = ['H', 'D', 'C', 'S']
        print()
        print('  A   2   3   4   5   6   7   8   9   10  J   Q   K')
        # add col label to front of each row
        i = 0
        n = len(self.discard_pile)
        for r in range(n):
            string = col_label[i] + " "
            for e in range(len(self.discard_pile[0])):
                if self.discard_pile[r][e] < 10:
                    string += str(self.discard_pile[r][e]) + '   '
                else:
                    string += str(self.discard_pile[r][e]) + '  '
            print(string)
            i += 1
        return ""

    def add_card(self, card: card):
        '''
        set top card, return null
        '''
        s = card.get_suit()
        v = card.get_rank()
        self.discard_pile[s][v] = 1
        self.top = (s, v)

    def remove_top(self):
        '''
        set top card to 0 in matrix, return top card
        '''
        s = self.top[0]
        v = self.top[1]
        self.discard_pile[s][v] = 0
        return card.Card(s, v)

    def get_top_card(self):
        '''
        return position in matrix of card at top of pile (tuple)
        '''
        s = self.top[0]
        v = self.top[1]
        return card.Card(s, v)

    # for discard pile, whenever we add a card, that card become the new top card
    # when we remove a card from discard, we always remove the top card
