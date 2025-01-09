from cards import *
from graphics import WINDOW_WIDTH, WINDOW_HEIGHT
import numpy as np
import random


DESC = -1
UNDEFINED = 0
ASC = 1

MIN_CARAVAN_THRESHOLD = 21
MAX_CARAVAN_THRESHOLD = 26


class Deck:
    def __init__(self, cards):
        self.cards: list[Card] = cards

        self.is_hoverable = True

    def add_card(self, card):
        card.z_index = max(self.cards[-1].z_index + 1, card.z_index)
        self.cards.append(card)

    def contains(self, card):
        return any(card == s_card for s_card in self.cards)

    def remove_card(self, card):
        if self.contains(card):
            self.cards.remove(card)

    def hover(self, x, y):
        for card in self.cards:
            card.hover(x, y)

    def click(self, x, y):
        for reset_card in self.cards:
            reset_card.is_selected = False

        for card in reversed(self.cards):
            if card.collides_with(x, y) and card.is_hoverable:
                card.click(x, y)
                break

    def check_if_selected(self):
        return any(card.is_selected for card in self.cards)

    def get_selected(self):
        for card in self.cards:
            if card.is_selected:
                return card

    def dump(self):
        return self.cards


class PlayingDeck(Deck):
    def __init__(self, cards=None):
        if not cards:
            cards = generate_player_1_hand_cards(8)
        super().__init__(cards)

        self.is_selected = False

    def add_card(self, card):
        super().add_card(card)
        card.is_hoverable = True

    def respace_cards_positions(self):
        return generate_player_1_hand_card_positions(len(self.cards))


class DrawingDeck(Deck):
    def __init__(self, cards=None):
        if not cards:
            cards = generate_drawing_deck_cards(52)
        super().__init__(cards)

        self.is_selected = False


def generate_all_cards():
    return ([Card(rank, suit) for rank in RANKS[:-1] for suit in SUITS[:-2]] +
            [Card(RANK_JOKER, SUIT_BLACK_JOKER), Card(RANK_JOKER, SUIT_RED_JOKER)])


def generate_random_cards(num_cards=None):
    deck = generate_all_cards()
    assert num_cards <= len(deck)
    random.shuffle(deck)
    return deck[:num_cards]


def generate_player_1_hand_cards(num_cards: int = 5, cards=None):
    if cards:
        deck = cards
    else:
        deck = generate_random_cards(num_cards)

    positions = generate_player_1_hand_card_positions(num_cards)
    res = []
    for i, (x, y, angle) in enumerate(positions):
        card = deck[i]
        card.set_at(x, y, angle)
        card.is_flipped = True
        card.z_index = i
        res.append(card)

    return res


def generate_player_1_hand_card_positions(num_cards: int = 5):
    x_coords = list(np.linspace(WINDOW_WIDTH - 250, WINDOW_WIDTH - 50, num_cards))
    unit_x_coords = list(np.linspace(25, 225, num_cards))
    unit_y_coords = list(map(lambda x: -np.sqrt(150 ** 2 * (1 - 1 / (225 ** 2) * (x - 225) ** 2)), unit_x_coords))
    offset_x, offset_y = WINDOW_WIDTH - 50 - unit_x_coords[-1], WINDOW_HEIGHT - 175 - unit_y_coords[-1]
    y_coords = list(map(lambda y: y + offset_y, unit_y_coords))
    angles = [40 * (num_cards - 1 - i) / (num_cards - 1) for i in range(num_cards)]
    return list(zip(x_coords, y_coords, angles))


def generate_drawing_deck_cards(num_cards: int = 52):
    cards = generate_random_cards(num_cards)
    for i, card in enumerate(cards):
        card.set_at(WINDOW_WIDTH - 80 - 3 * i / num_cards, WINDOW_HEIGHT // 2, 3 * i / num_cards)
        card.is_flipped = False
        card.is_hoverable = False
        card.z_index = num_cards - i
    cards[0].is_hoverable = True
    return cards


class Caravan:
    def __init__(self):
        self.rows: list[tuple[Card, list[Card]]] = []
        self.value = 0
        self.direction = UNDEFINED

