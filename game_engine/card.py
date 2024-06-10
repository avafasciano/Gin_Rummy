class Card:
    '''
    Class to represent a card 
    Attributes
    ----------
    suit- int 1..4, where 1 = hearts, 2 = spades, 3 = clubs 
    rank- 
    value- int 1..10 (jack, queen, king valued at 10)
    id- int 1..52


    '''

    def __init__(self, suit: int, rank: int, id=1):
        assert type(suit) is int, "suit not an int"
        assert type(rank) is int, "rank not an int"
        assert suit >= 0 and suit <= 3, "suit not in range"
        assert rank >= 0 and rank <= 12, "rank not in range"

        self.suit = suit
        self.rank = rank
        self.id = id

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_id(self):
        return self.id

    def get_value(self):
        if self.rank <= 9:
            return self.rank + 1
        else:
            return 10

    def display(self):
        '''
        lookup string in card dictionary
        '''
        suits = ["H", "D", "C", "S"]
        ranks = ["A", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "J", "Q", "K"]

        return ranks[self.rank] + suits[self.suit]
