from cards import *
import random


DESC = -1
UNDEFINED = 0
ASC = 1

MIN_CARAVAN_THRESHOLD = 21
MAX_CARAVAN_THRESHOLD = 26


class Deck:
    def __init__(self, cards):
        self.cards: list[Card] = cards


def generate_full_deck():
    numerical_cards = [
        Card(rank, suit) for rank in RANKS[:-4]
        for suit in SUITS[:-2]
    ]
    face_cards = [
        Card(rank, suit) for rank in range(RANK_J, RANK_K + 1)
        for suit in range(SUIT_SPADES, SUIT_CLUBS + 1)
    ]
    joker_cards = [
        Card(RANK_JOKER, SUIT_BLACK_JOKER),
        Card(RANK_JOKER, SUIT_RED_JOKER)
    ]
    return numerical_cards + face_cards + joker_cards


def generate_random_deck(num_cards=None):

    num_cards = num_cards if num_cards else random.randint(30, 54)


class Caravan:
    def __init__(self):
        self.rows: list[tuple[Card, list[Card]]] = []
        self.value = 0
        self.direction = UNDEFINED

