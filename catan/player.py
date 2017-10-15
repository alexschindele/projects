
class Player(object):

    def __init__(self):
        self.points = 0
        self.dev_cards = {}
        self.resource_cards = {'wood'  : 0,
                               'ore'   : 0,
                               'wool'  : 0,
                               'wheat' : 0,
                               'brick' : 0}

