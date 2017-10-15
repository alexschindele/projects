# from blackjack.deck_utils import *
import os
import random
import traceback
import statistics
import pandas as pd
import matplotlib.pyplot as plt

CARD_SUITS = ['♦', '♠', '♣', '♥']
CARD_FACES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


def hand_value(cards):
    value = (0,0)
    for card in cards:
        if isinstance(card.value, tuple):
            value = (card.value[0] + value[0], card.value[1] + value[1])
        else:
            value = (card.value + value[0], card.value + value[1])
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
                self.deck.extend([Card(suit = suit, face = face)] * decks)


    @property
    def number_of_cards(self):
        return len(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)


    def draw(self):
        return self.deck.pop()

class BlackJack(object):


    def __init__(self, min_bet = 10,
                 hit_on_soft_seventeen = False,
                 penetration = .25,
                 ):
        self.min_bet = min_bet
        self.shoe = Deck(decks=5)
        self.shoe.shuffle()
        self.player = BJPlayer()
        self.dealer = Dealer()


    def play(self):
        while True:
            if len(self.shoe.deck) < 10:
                self.shoe = Deck(decks=5)
                self.shoe.shuffle()
            bet = input("How much would you like to bet?")
            self.player.hand.append(self.shoe.draw())
            self.dealer.hand.append(self.shoe.draw())
            self.player.hand.append(self.shoe.draw())
            self.dealer.hand.append(self.shoe.draw())
            for card in self.player.hand:
                print("Player holds: " + card)
            print("Dealer holds: " + self.dealer.hand[0])
            user_input = input('What would you like to do?')
            if user_input == 'S':
                self.player.hand.append(self.shoe.draw())
            elif user_input == 'H':
                continue
            elif user_input == 'E':
                break
            else:
                print("not valid")
            while max(hand_value(self.dealer.hand)) < 17:
                pass

    def autoplay(self, player_bet):
        self.player.hand.append(self.shoe.draw())
        self.dealer.hand.append(self.shoe.draw())
        self.player.hand.append(self.shoe.draw())
        self.dealer.hand.append(self.shoe.draw())
        self.player.play(self.shoe, self.dealer)
        self.dealer.play(self.shoe)
        if max(hand_value(self.player.hand)) > 21:
            self.player.pnl -= player_bet
            self.player.bank -= player_bet
        elif max(hand_value(self.dealer.hand)) > 21:
            self.player.pnl += player_bet
            self.player.bank += player_bet
        elif max(hand_value(self.dealer.hand)) > max(hand_value(self.player.hand)):
            self.player.pnl -= player_bet
            self.player.bank -= player_bet
        elif max(hand_value(self.dealer.hand)) < max(hand_value(self.player.hand)):
            self.player.pnl += player_bet
            self.player.bank += player_bet




class BJPlayer(object):

    def __init__(self, starting_cash = None):
        if starting_cash is None:
            self.bank = 1E12
        else:
            self.bank = starting_cash
        self.pnl  = 0
        self.hands = [[]]
        self.optimal_play_matrix = {}


class Dealer(object):

    def __init__(self, hit_on_soft_seventeen = True
                 ):
        self.hand = []

    def play(self, shoe):
        if len(self.hand) < 2:
            raise BaseException("Need to deal cards first")
        while max(hand_value(self.hand)) <= 17:
            self.hand.append(shoe.draw())


def dictify(df):
    d = {}
    for idx, row in df.iterrows():
        r = {}
        for ind, k in enumerate(row):
            r[df.columns[ind]] = row[df.columns[ind]]
        d[idx] = r
    return d

def hi_lo_count(card):
    face = card.face
    if face in ["2", "3", "4", "5", "6"]:
        return 1
    if face in ["7", "8", "9"]:
        return 0
    if face in ["J", "Q", "K", "A", "10"]:
        return -1

class BlackJackGame(object):

    def __init__(self, decks=8, min_bet = 25, hit_on_soft_seventeen = False, penetration = .75, bet_spread_matrix = None):
        file_location = r"C:\Users\alexschindele\PycharmProjects\projects\blackjack"
        self.min_bet = min_bet
        self.decks = decks
        self.shoe = Deck(decks=decks)
        self.shoe.shuffle()
        self.original_card_count = decks * 52
        self.player = BJPlayer()
        self.dealer = Dealer()
        self.penetration = penetration
        self.bj_count = 0
        self.optimal_play_matrix = dictify(pd.read_csv(os.path.join(file_location, "optimal_bj_regular.csv"), index_col = 0))
        self.optimal_play_matrix_softs = dictify(pd.read_csv(os.path.join(file_location, "optimal_bj_soft.csv"), index_col = 0))
        self.optimal_play_matrix_twos = dictify(pd.read_csv(os.path.join(file_location, "optimal_bj_pairs.csv"), index_col = 0))
        if bet_spread_matrix is None:
            self.bet_spread_matrix = [1,2,4,8,12]
        else:
            self.bet_spread_matrix = bet_spread_matrix

    def reshuffle_deck(self):
        self.shoe = Deck(decks=self.decks)
        self.shoe.shuffle()

    def play(self, keep_count = False, debug=False):
        true_count = int(self.bj_count / (self.shoe.number_of_cards / 52))
        if true_count < 0:
            bet_multiple = self.bet_spread_matrix[0]
        elif true_count >= len(self.bet_spread_matrix):
            bet_multiple = self.bet_spread_matrix[-1]
        else:
            bet_multiple = self.bet_spread_matrix[true_count]

        if keep_count:
            player_bet = self.min_bet * bet_multiple
        else:
            player_bet = self.min_bet
        card = self.shoe.draw()
        self.bj_count += hi_lo_count(card)
        self.player.hands[0].append(card)
        card = self.shoe.draw()
        self.dealer.hand.append(card)
        self.bj_count += hi_lo_count(card)
        card = self.shoe.draw()
        self.player.hands[0].append(card)
        self.bj_count += hi_lo_count(card)
        card = self.shoe.draw()
        self.dealer.hand.append(card)
        self.bj_count += hi_lo_count(card)

        surrender = False
        bj        = False
        multiplier = [1]
        # self.player.hands[0] = [Card("♦", "7"  ), Card("♠","7")]
        # self.player.hands[0] = [Card("♥", "J" ), Card("♠","A")]
        # self.dealer.hand = [Card("♥", "6" ), Card("♠","5")]
        if debug:
            print("Player: " + " ".join([str(x) for x in self.player.hands[0]]))
            print("Dealer: " + str(self.dealer.hand[0]))
        try:
            for idx, hand in enumerate(self.player.hands):
                counter = 0
                if max(hand_value(self.player.hands[idx])) == 21:
                    bj = True
                    break
                while True:
                    if max(hand_value(self.dealer.hand)) == 21:
                        break
                    if len(hand) == 1:
                        card = self.shoe.draw()
                        self.bj_count += hi_lo_count(card)
                        self.player.hands[idx].append(card)
                    if len(self.player.hands[idx]) <= 2 and self.player.hands[idx][0].value == self.player.hands[idx][1].value:
                        if self.player.hands[idx][0].value == (1, 11):
                            player = "A"
                        else:
                            player = self.player.hands[idx][0].value
                        if self.dealer.hand[0].value == (1, 11):
                            dealer = "A"
                        else:
                            dealer = self.dealer.hand[0].value
                        decision = self.optimal_play_matrix_twos[str(player)][str(dealer)]
                    elif any([x.face == "A" for x in self.player.hands[idx]]):
                        card = sum([x.value for x in self.player.hands[idx] if x.face != "A"])
                        if str(self.dealer.hand[0].face) in ["K", "J" ,"Q"]:
                            dealer = "10"
                        else:
                            dealer =str(self.dealer.hand[0].face)
                        if card < 10:
                            decision = self.optimal_play_matrix_softs[card][dealer]
                        elif card == 10:
                            break
                        else:
                            decision = self.optimal_play_matrix[card + 1][dealer]
                    else:
                        if self.dealer.hand[0].value == (1, 11):
                            dealer = "A"
                        else:
                            dealer = self.dealer.hand[0].value
                        decision = self.optimal_play_matrix[max(hand_value(self.player.hands[idx]))][str(dealer)]
                    if decision == "D" and counter == 0:
                        card = self.shoe.draw()
                        self.bj_count += hi_lo_count(card)
                        self.player.hands[idx].append(card)
                        multiplier[idx] = 2
                        break
                    elif decision == "S":
                        break
                    elif decision == "Spl":
                        self.player.hands.append([self.player.hands[idx].pop()])
                        multiplier.append(1)
                    elif decision == "Surr" and counter == 0:
                        self.player.pnl -= player_bet / 2
                        surrender = True
                        if debug:
                            print("Surrendering!")
                        break
                    else:
                        card = self.shoe.draw()
                        self.bj_count += hi_lo_count(card)
                        self.player.hands[idx].append(card)
                        if min(hand_value(self.player.hands[idx])) > 21:
                            break
                    if decision != "Spl":
                        counter += 1
            if not surrender:
                if max(hand_value(self.dealer.hand)) == 21 and bj:
                    pass
                elif bj:
                    if debug:
                        print("Player Blackjack!")
                    self.player.pnl += player_bet * 1.5
                    self.player.bank += player_bet * 1.5
                else:
                    dealer_hand = min(hand_value(self.dealer.hand)) if max(hand_value(self.dealer.hand)) > 21 else max(hand_value(self.dealer.hand))
                    while dealer_hand < 17:
                        card = self.shoe.draw()
                        self.bj_count += hi_lo_count(card)
                        self.dealer.hand.append(card)
                        dealer_hand = min(hand_value(self.dealer.hand)) if max(hand_value(self.dealer.hand)) > 21 else max(hand_value(self.dealer.hand))

                    for idx, hand in enumerate(self.player.hands):
                        if debug:
                            print("Player: " + " ".join([str(x) for x in hand]))
                            print("Dealer: " + " ".join([str(x) for x in self.dealer.hand]))
                        if min(hand_value(hand)) > 21:
                            self.player.pnl -= player_bet * multiplier[idx]
                            self.player.bank -= player_bet * multiplier[idx]
                            continue
                        elif min(hand_value(self.dealer.hand)) > 21:
                            self.player.pnl += player_bet * multiplier[idx]
                            self.player.bank += player_bet * multiplier[idx]
                            continue
                        if max(hand_value(hand)) > 21:
                            player_hand = min(hand_value(hand))
                        else:
                            player_hand = max(hand_value(hand))
                        if max(hand_value(self.dealer.hand)) > 21:
                            dealer_hand = min(hand_value(self.dealer.hand))
                        else:
                            dealer_hand = max(hand_value(self.dealer.hand))
                        if dealer_hand > player_hand:
                            self.player.pnl -= player_bet * multiplier[idx]
                            self.player.bank -= player_bet * multiplier[idx]
                        elif dealer_hand < player_hand:
                            self.player.pnl += player_bet * multiplier[idx]
                            self.player.bank += player_bet * multiplier[idx]
            self.player.hands = [[]]
            self.dealer.hand = []
            if (1 - self.penetration) * self.original_card_count > self.shoe.number_of_cards:
                self.reshuffle_deck()
                self.bj_count = 0
        except:
            print(traceback.format_exc())

def basic_stats(ls, init_bet=25, trials=60):
    import numpy as np
    arr = np.array(ls)
    print("Player Advantage: %f" % (statistics.mean(ls)/ init_bet / (trials / 60))) # about 60 hands every hour, so EV per hour
    print("EV per hour: %f" % (statistics.mean(ls)/ trials*60 )) # about 60 hands every hour, so EV per hour
    print("Mean: %f" % statistics.mean(ls))
    # print("Mode: %f" % statistics.mode(ls))
    print("Median: %f" % statistics.median(ls))
    print("Stdev: %f" % statistics.stdev(ls))
    print("Max: %f" % max(ls))
    print("Min: %f" % min(ls))
    print("98pct Conf. Interval: (%f, %f)" % (np.percentile(arr, 1),np.percentile(arr, 99)))

def main(keep_count=True,decks=6,init_bet = 25, runs = 1000, trials_per_run=1000):
    pnls = []
    running_avg = []
    for i in range(runs):
        bj = BlackJackGame(decks=decks, min_bet=init_bet)
        for j in range(trials_per_run):
            bj.play(keep_count = keep_count, debug=False)
        pnls.append(bj.player.pnl)
        if len(running_avg) == 0:
            running_avg.append(bj.player.pnl)
        else:
            running_avg.append((running_avg[-1] * len(running_avg)+ bj.player.pnl) / (len(running_avg) + 1))

    basic_stats(pnls, init_bet, trials_per_run)
    plt.plot([x for x in range(len(running_avg))], running_avg, 'ro')
    plt.axis([0, len(running_avg), -100, 100])
    plt.show()

if __name__ =='__main__':
    main(keep_count=True,
         decks=6,
         init_bet=25,
         runs= 100000,
         trials_per_run=600)