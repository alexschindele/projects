import random
CARD_SUITS = ['♦', '♠', '♣', '♥']
CARD_FACES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


def hand_value(cards):
    value = 0
    for card in cards:
        if isinstance(card.value, tuple):
            value = (card.value[0] + 1, card.value[1] + 11)
        else:
            value = (card.value + value, card.value + value)
    return value

class Card(object):

    def __init__(self, suit, face):
        self.suit = suit
        self.face = face
        try:
            self.value = int(face)
        except ValueError:
            if face == 'A':
                self.value = (1, 11)
            else:
                self.value = 10

    def __str__(self):
        return self.suit + ' ' + self.face


class Deck(object):

    def __init__(self, decks = 1):
        self.deck = []
        for face in CARD_FACES:
            for suit in CARD_SUITS:
                self.deck = [Card(suit = suit, face = face)] * decks


    def shuffle(self):
        random.shuffle(self.deck)


    def draw(self):
        return self.deck.pop()

if __name__ == "__main__":
    deck = Deck()
    print(deck.draw())