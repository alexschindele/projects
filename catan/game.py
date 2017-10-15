from catan.board import *
from catan.utils import *
from catan.player import *
from catan.board import *
import pygame


def main():
    screen = pygame.display.set_mode(1024, 768)
    board = Board()
    resource_cards = ResourceCardDeck()
    dev_cards = DevelopmentCardDeck()

if __name__ == "__main__":
    main()