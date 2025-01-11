import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP, KEYUP, K_ESCAPE
import graphics
from graphics import WINDOW_WIDTH, WINDOW_HEIGHT
from decks import *
import random
from cards import Card
from itertools import chain


class Context:
    def __init__(self):
        self.state: State = Running()  # by default, start the title screen

    def handle_events(self):
        self.state = self.state.handle_events()

    def is_running(self):
        return self.state.is_running()


class State:
    def __init__(self, objects=None, animations=None, transition=False):
        self.objects: dict[str, Button | Card | Deck] = objects if objects else {}
        self.animations: list = animations if animations else []
        self.transition = transition

    def handle_events(self):
        return self

    def is_running(self):
        return True


class TitleScreen(State):
    def __init__(self, objects=None, animations=None, transition=False):
        super().__init__(objects, animations, transition)

        # play_button
        self.objects['play_button'] = Button(
            0, 0, WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3, 'Play',
            z_index=5
        )
        self.objects['play_button'].in_neutral = True

        # play_standard_mode_button
        self.objects['play_standard_mode_button'] = Button(
            0, 0, WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3, 'Standard Mode',
            z_index=3, is_visible=False, is_clickable=False
        )

    def handle_events(self):
        if _check_for_quit():
            return Quit(objects=self.objects, animations=self.animations)

        x, y = pygame.mouse.get_pos()
        for button in self.objects.values():
            button.hover(x, y)

        for event in pygame.event.get(MOUSEBUTTONUP):
            x, y = event.pos
            play_button = self.objects['play_button']
            if play_button.is_clickable and play_button.rect.collidepoint(x, y):
                play_button.is_clickable = False
                if play_button.in_neutral:
                    play_button.in_neutral = False
                    self.animations.append(self.get_play_button_neutral_to_active_animation())
                else:
                    play_button.in_neutral = True
                    self.animations.append(self.get_play_button_active_to_neutral_animation())

            play_standard_mode_button = self.objects['play_standard_mode_button']
            if play_standard_mode_button.is_clickable and play_standard_mode_button.rect.collidepoint(x, y):
                play_standard_mode_button.is_clickable = False
                play_standard_mode_button.is_hovered = False
                return Running(transition=True)

        return self

    def get_play_button_neutral_to_active_animation(self):
        play_button = self.objects['play_button']
        play_standard_mode_button = self.objects['play_standard_mode_button']
        play_standard_mode_button.is_visible = True

        animation_speed = 10
        for offset in range(0, 301, animation_speed):
            scalar = 1 - offset / 750
            play_button.update(
                scale=(int(WINDOW_WIDTH / 4 * scalar), int(WINDOW_HEIGHT / 4 * scalar)),
                rect=pygame.Rect(0, 0, int(WINDOW_WIDTH / 4 * scalar), int(WINDOW_HEIGHT / 4 * scalar)),
                center=(WINDOW_WIDTH // 2 - offset // 2, WINDOW_HEIGHT // 3)
            )
            play_standard_mode_button.update(center=(WINDOW_WIDTH // 2 + offset // 3, WINDOW_HEIGHT // 3))
            yield {'play_button': play_button, 'play_standard_mode_button': play_standard_mode_button}

        self.objects['play_button'].is_clickable = True
        self.objects['play_standard_mode_button'].is_clickable = True

    def get_play_button_active_to_neutral_animation(self):
        play_button = self.objects['play_button']
        play_standard_mode_button = self.objects['play_standard_mode_button']
        play_standard_mode_button.is_clickable = False

        animation_speed = 10  # should divide 300
        for offset in range(0, 301, animation_speed):
            scalar = (450 + offset) / 750
            play_button.update(
                scale=(int(WINDOW_WIDTH / 4 * scalar), int(WINDOW_HEIGHT / 4 * scalar)),
                rect=pygame.Rect(0, 0, int(WINDOW_WIDTH / 4 * scalar), int(WINDOW_HEIGHT / 4 * scalar)),
                center=(WINDOW_WIDTH // 2 - 150 + offset // 2, WINDOW_HEIGHT // 3)
            )
            play_standard_mode_button.update(center=(WINDOW_WIDTH // 2 + 100 - offset // 3, WINDOW_HEIGHT // 3))
            yield {'play_button': play_button, 'play_standard_mode_button': play_standard_mode_button}

        self.objects['play_button'].rect = pygame.Rect(0, 0, WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4)
        self.objects['play_button'].rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        self.objects['play_button'].is_clickable = True

        self.objects['play_standard_mode_button'].is_visible = False


class Running(State):
    def __init__(self, objects=None, animations=None, transition=False):
        super().__init__(objects, animations, transition)

        # self.objects['player_1_caravan_A_background'] = Button(0, 0, 98, 128 + 40 * 6, center_x=200, center_y=290 + 40*3, z_index=-5, is_clickable=False)
        # self.objects['player_1_caravan_B_background'] = Button(0, 0, 98, 128 + 40 * 6, center_x=400, center_y=290 + 40*3, z_index=-5, is_clickable=False)
        # self.objects['player_1_caravan_C_background'] = Button(0, 0, 98, 128 + 40 * 6, center_x=600, center_y=290 + 40*3, z_index=-5, is_clickable=False)
        # self.objects['player_2_caravan_A_background'] = Button(0, 0, 98, 128 + 40 * 6, center_x=100, center_y=90 + 40*3, z_index=-5, is_clickable=False)
        # self.objects['player_2_caravan_B_background'] = Button(0, 0, 98, 128 + 40 * 6, center_x=300, center_y=90 + 40*3, z_index=-5, is_clickable=False)
        # self.objects['player_2_caravan_C_background'] = Button(0, 0, 98, 128 + 40 * 6, center_x=500, center_y=90 + 40*3, z_index=-5, is_clickable=False)

        self.objects['player_1_caravan_A'] = Caravan(player=1, caravan='A')
        self.objects['player_1_caravan_B'] = Caravan(player=1, caravan='B')
        self.objects['player_1_caravan_C'] = Caravan(player=1, caravan='C')
        self.objects['player_2_caravan_A'] = Caravan(player=2, caravan='A')
        self.objects['player_2_caravan_B'] = Caravan(player=2, caravan='B')
        self.objects['player_2_caravan_C'] = Caravan(player=2, caravan='C')
        self.caravan_names = [
            'player_1_caravan_A',
            'player_1_caravan_B',
            'player_1_caravan_C',
            'player_2_caravan_A',
            'player_2_caravan_B',
            'player_2_caravan_C'
        ]

        self.objects['go_back_button'] = Button(10, WINDOW_HEIGHT - 50, 80, 40, text='Go back')
        self.objects['trash_button'] = Button(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50, 40, 40, text='trash')

        self.objects['player_1_playing_deck']: PlayingDeck = PlayingDeck()
        self.objects['drawing_deck']: DrawingDeck = DrawingDeck()

    def handle_events(self):
        if _check_for_quit():
            return Quit(objects=self.objects, animations=self.animations)

        previously_selected = None  # store previously selected object (mainly interested in cards)
        currently_selected = None  # store currently selected object

        # print([(self.objects[name].calculate_value(), self.objects[name].calculate_suit(), self.objects[name].calculate_direction()) for name in self.caravan_names])
        print(str([str(card) for name in self.caravan_names for card in self.objects[name].cards]))

        # """
        # Handle mouse hovering over objects.
        # """
        x, y = pygame.mouse.get_pos()
        for value in self.objects.values():
            value.hover(x, y)
            if value.check_if_selected():
                previously_selected = value.get_selected()

        # """
        # Handle mouse click on objects.
        # """
        for event in pygame.event.get(MOUSEBUTTONUP):
            x, y = event.pos

            if self.objects['go_back_button'].collides_with(x, y):
                return TitleScreen(transition=True)

            for value in self.objects.values():
                value.click(x, y)
                if value.check_if_selected():
                    currently_selected = value.get_selected()

        # """
        # Handle scenario if card from player_1_playing_deck is played.
        # """
        player_1_playing_deck: PlayingDeck = self.objects['player_1_playing_deck']
        if player_1_playing_deck.contains(previously_selected):
            # """
            # Handle card being discarded.
            # """
            if currently_selected == self.objects['trash_button']:
                player_1_playing_deck.remove_card(previously_selected)
                self.animations.append(self.respace_player_1_hand_animation(PlayingDeck(cards=player_1_playing_deck.cards[:])))

                player_1_playing_deck.add_card(self.objects['drawing_deck'].cards[0])

                self.animations.append(
                    chain(
                        self.translate_card_animation(previously_selected, -200, random.randint(0, WINDOW_HEIGHT), -500),
                        self.wait_animation(.2),
                        self.flip_over_card_animation(self.objects['drawing_deck'].cards[0]),
                        self.wait_animation(.2),
                        self.add_card_to_playing_deck_animation(self.objects['drawing_deck'].cards[0]),
                        self.wait_animation(.2),
                        self.respace_player_1_hand_animation(player_1_playing_deck)
                    )
                )
            # """
            # Handle card being placed on a caravan.
            # """
            elif (
                    any(self.objects[name].contains(currently_selected) for name in self.caravan_names) and previously_selected.is_face()
                    or any(self.objects[name].contains(currently_selected) for name in self.caravan_names[:3]) and previously_selected.is_numerical()
            ):
                at_deck = 'anonymous_card'
                for name in self.caravan_names:
                    if self.objects[name].contains(currently_selected):
                        at_deck = name
                        break
                if self.objects[at_deck].check_if_move_is_valid(previously_selected, currently_selected):
                    player_1_playing_deck.remove_card(previously_selected)
                    self.objects[at_deck].add_card_on(previously_selected, currently_selected)
                    currently_selected.is_selected = False
                    if previously_selected.rank not in [RANK_J, RANK_JOKER]:
                        self.animations.append(chain(
                            self.translate_card_on_top_of_card_animation(previously_selected, currently_selected, self.objects[at_deck]),
                            self.remove_outline_card_of_caravan(self.objects[at_deck])
                        ))
                    elif previously_selected.rank == RANK_J:
                        self.animations.append(chain(
                            self.translate_card_on_top_of_card_animation(previously_selected, currently_selected, self.objects[at_deck]),
                            self.remove_outline_card_of_caravan(self.objects[at_deck]),
                            self.wait_animation(.2),
                            self.activate_jack_card_animation(previously_selected, currently_selected, self.objects[at_deck]),
                            self.wait_animation(.5),
                            self.readjust_caravan_animation(self.objects[at_deck])
                        ))
                    else:
                        self.animations.append(chain(
                            self.translate_card_on_top_of_card_animation(previously_selected, currently_selected, self.objects[at_deck]),
                            self.remove_outline_card_of_caravan(self.objects[at_deck]),
                            self.wait_animation(.2),
                            # TODO: Add joker animation
                        ))
                    self.animations.append(self.respace_player_1_hand_animation(player_1_playing_deck))

        return self

    def translate_card_animation(self, card, cx, cy, angle, at_deck='anonymous_card'):
        curr_x, curr_y = card.center
        curr_angle = card.angle
        animation_speed = 45
        for t in range(animation_speed):
            offset_x = curr_x + (cx - curr_x) * t / (animation_speed - 1)
            offset_y = curr_y + (cy - curr_y) * t / (animation_speed - 1)
            offset_angle = curr_angle + (angle - curr_angle) * t / (animation_speed - 1)
            card.set_at(offset_x, offset_y, offset_angle)
            yield {'anonymous_card': card}
        # for key, value in self.objects.items():
        #     if key == at_deck and at_deck != 'anonymous_card':
        #         self.objects[at_deck] = card
        #         # value.cards.append(card)
        #         return
        self.objects[at_deck] = card
        yield self.objects

    def flip_over_card_animation(self, card):
        curr_image = card.get_image()
        image_w, image_h = curr_image.get_size()
        animation_speed = 20
        for ts in [range(animation_speed), range(animation_speed, -1, -1)]:
            for t in ts:
                offset_image_w = image_w * (1 - t / animation_speed)
                offset_image_h = image_h * (1 + 0.2 * t / animation_speed)
                offset_image = pygame.transform.scale(curr_image, (offset_image_w, offset_image_h))
                card.set_image(offset_image)
                yield {'anonymous_card': card}
            if ts == range(animation_speed, -1, -1):
                continue
            card.is_flipped = not card.is_flipped
            card.set_at(*card.center, -card.angle)
            curr_image = card.get_image()

    def respace_player_1_hand_animation(self, deck):
        positions = list(deck.respace_cards_positions())
        old_positions = [(*card.center, card.angle) for card in deck.cards]

        animation_speed = 45
        for t in range(animation_speed):
            cards = []
            for card, (x, y, angle), (curr_x, curr_y, curr_angle) in zip(deck.cards, positions, old_positions):
                offset_x = curr_x + (x - curr_x) * t / (animation_speed - 1)
                offset_y = curr_y + (y - curr_y) * t / (animation_speed - 1)
                offset_angle = curr_angle + (angle - curr_angle) * t / (animation_speed - 1)
                card.set_at(offset_x, offset_y, offset_angle)
                cards.append(card)
            yield {'player_1_playing_deck': PlayingDeck(cards=cards)}

    def wait_animation(self, seconds):
        for t in range(int(graphics.FPS * seconds)):
            yield self.objects

    def add_card_to_playing_deck_animation(self, card):
        self.objects['player_1_playing_deck'].cards.append(card)
        self.objects['drawing_deck'].cards.pop(0)
        yield self.objects

    def translate_card_on_top_of_card_animation(self, card, on_top_of_card, deck):
        angle = random.randint(-5, 0)  # TODO: OCD Mode (when the angle is set to just 0)
        if deck.cards[0] == on_top_of_card:
            return self.translate_card_animation(card, *on_top_of_card.center, angle)
        if card.is_numerical():
            for layer_card, adjacents in deck.layers:
                if layer_card == on_top_of_card or on_top_of_card in adjacents:
                    return self.translate_card_animation(card, layer_card.center[0], layer_card.center[1] + 40, angle)
        if card.is_face():
            for layer_card, adjacents in deck.layers:
                if layer_card == on_top_of_card or on_top_of_card in adjacents:
                    offset_x = len(adjacents) * 20
                    return self.translate_card_animation(card, layer_card.center[0] + offset_x, layer_card.center[1], angle)

    def remove_outline_card_of_caravan(self, deck):
        if 'Placeholder' in str(type(deck.cards[0])):
            deck.cards[0].is_visible = False
        yield self.objects

    def activate_jack_card_animation(self, card, on_top_of_card, deck):
        for layer_card, adjacents in deck.layers:
            if on_top_of_card == layer_card or on_top_of_card in adjacents:
                break
        deck.remove_card(layer_card)
        cards = [card, layer_card, *adjacents]
        for i, c in enumerate(cards):
            self.animations.append(self.translate_card_animation(c, -200, random.randint(0, WINDOW_HEIGHT), -500, at_deck=f'anonymous_card_{i}'))
        deck.update()
        yield {f'anonymous_card_{i}': c for i, c in enumerate(cards)}

    def readjust_caravan_animation(self, deck: Caravan):
        starting_x = {1: 200, 2: 100}
        starting_y = {1: 290, 2: 90}
        offset_x = {'A': 0, 'B': 200, 'C': 400}

        player = deck.player
        caravan = deck.caravan

        for i, (layer_card, adjacents) in enumerate(deck.layers):
            layer_card: Card
            self.animations.append(self.translate_card_animation(layer_card, starting_x[player] + offset_x[caravan], starting_y[player] + 40 * i, layer_card.angle, at_deck=f'ac_{i}'))
            # layer_card.set_at(starting_x[player] + offset_x[caravan], starting_y[player] + 40 * i, layer_card.angle)
            layer_card.z_index = i * 5
            for j, adj in enumerate(adjacents):
                adj: Card
                self.animations.append(self.translate_card_animation(adj, starting_x[player] + offset_x[caravan] + 20 * (j + 1), starting_y[player] + 40 * i, adj.angle, at_deck=f'ac_{i}_{j}'))
                # adj.set_at(starting_x[player] + offset_x[caravan] + 20 * (j + 1), starting_y[player] + 40 * i, adj.angle)
                adj.z_index = i * 5 + j + 1
        deck.update()
        yield self.objects


class Quit(State):
    def __init__(self, objects=None, animations=None, transition=False):
        super().__init__(objects, animations, transition)

    def handle_events(self):
        raise NotImplemented('Quit state should not be handling events.')

    def is_running(self):
        return False


def _check_for_quit():
    if len(pygame.event.get(eventtype=QUIT)) > 0:
        return True
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            return True
        pygame.event.post(event)
    return False


class Button:
    def __init__(self, left, top, width, height, center_x=None, center_y=None, text='', is_clickable=True,
                 is_hovered=False, is_visible=True, z_index=0):
        self.original_image = pygame.Surface((width, height)).convert_alpha()
        self.original_image.fill((255, 255, 255, 255))
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.fill((255, 255, 255, 255))
        self.rect = pygame.Rect(left, top, width, height)
        if center_x and center_y:
            self.rect.center = (center_x, center_y)
        self.center = self.rect.center
        self.text = text

        self.hovered_image = pygame.Surface((width + 10, height + 10)).convert_alpha()
        self.hovered_image.fill((255, 255, 0, 255))

        self.is_clickable = is_clickable
        self.is_hovered = is_hovered
        self.is_visible = is_visible
        self.z_index = z_index
        self.is_selected = False

    def update(self, scale: tuple[int, int] | None = None, rect: pygame.Rect | None = None,
               center: tuple[float, float] | None = None):
        if scale:
            self.image = pygame.transform.scale(self.image, scale)
            w, h = self.image.get_size()
            self.hovered_image = pygame.Surface((w + 10, h + 10)).convert_alpha()
            self.hovered_image.fill((255, 255, 0, 255))
        if rect:
            self.rect = rect
        if center:
            self.rect.center = center
        self.center = self.rect.center

    def get_hovered_params(self):
        hovered_image_rect = self.hovered_image.get_rect()
        hovered_image_rect.center = self.rect.center

        return self.hovered_image, hovered_image_rect, self.image, self.rect, self.text

    def get_clicked_params(self):
        hovered_image_rect = self.hovered_image.get_rect()
        hovered_image_rect.center = self.rect.center

        return self.hovered_image, hovered_image_rect, self.image, self.rect, self.text

    def hover(self, x, y):
        if self.rect.collidepoint(x, y):
            self.is_hovered = True
        else:
            self.is_hovered = False
            self.is_selected = False

    def click(self, x, y):
        if self.rect.collidepoint(x, y):
            self.is_selected = True
        else:
            self.is_selected = False

    def get_image(self):
        return self.image

    def collides_with(self, x, y):
        return self.rect.collidepoint(x, y)

    def dump(self):
        return [self]

    def check_if_selected(self):
        return self.is_selected

    def get_selected(self):
        return self
