import random

class Board(object):

    def __init__(self):
        # need some sort of 2d data structure to hold tiles
        self.tiles = []

    def randomize_board(self):
        pass


class Tile(object):

    def __init__(self, number = None, resource_type = None):
        self.resource_type = resource_type
        self.number = number

    def next_to(self, tile):
        pass


class DevelopmentCardDeck(object):

    def __init__(self):
        pass

class DevelopmentCard(object):

    def __init__(self, card_type):
        self.card_type = card_type

class ResourceCard(object):

    def __init__(self):
        pass

class ResourceCardDeck(object):

    number_of_cards = 52
    def __init__(self):
        self.deck = [ResourceCard()] * self.number_of_cards

class Die(object):


    def __init__(self):
        pass

    def roll(self):
        value = random.randint(6) + 1
        return value
