class Move:
    """
    class to represent a player's move
    Attributes
    ----------
    player : Player
    type : "pickupDiscard", "pickupNewCard", "pass", "knock", "gin"
    discard : pydealer.Card (null if player passes this round)
    fold : boolean

    """

    def __init__(self, player, type, discard):
        self.player = player
        self.type = type
        self.discard = discard
        self.fold = False

    def set_discard(self, card):
        '''
        to be called in player once the player devides which card they'd like to discard
        '''
        self.discard = card

    def set_fold_true(self):
        '''
        for when player decides to gin or knock
        '''
        self.fold = True

    def set_type(self, type: str):
        '''
        for when player decides to gin or knock
        '''
        self.type = type

    def get_type(self):
        '''
        returns type of move as a string
        '''
        return self.type
