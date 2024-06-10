import random
import card


class Deck:
    """
    class representing a deck of cards
    Attributes:
    -----------
    deck

    Methods:
    ---------
    remove_top
    is_empty
    card_lookup
    display
    """

    def __init__(self):
        '''
        order integers 1-52 in a stack randomly
        '''
        stack = []
        i = 0
        for s in range(0, 4):
            for v in range(0, 13):
                new_card = card.Card(s, v, i)
                stack.append(new_card)
                i += 1

        stack_copy = stack[:]
        random.shuffle(stack_copy)

        self.deck = stack_copy

    def display(self):
        '''
        pretty print a deck. for testing
        '''
        for c in self.deck:
            print(c.display())

    def remove_top(self):
        '''
        card coming out of deck, return card so it can be added to hand
        return: int 
        '''
        top = self.deck[-1]
        self.deck.remove(top)
        return top

    def get_top(self):
        '''
        peek top card
        '''
        return self.deck[-1]

    def is_empty(self):
        '''
        indicate if deck is empty for error handling
        '''
        if len(self.deck) < 1:
            return True
        return False

# --------printline testing----------
#deck1 = Deck()
# deck1.display()
# print(len(deck1.deck))
# deck1.remove_top()
# print(len(deck1.deck))
# print(deck1.is_empty())
