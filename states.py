import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP, KEYUP, K_ESCAPE
from graphics import WINDOW_WIDTH, WINDOW_HEIGHT
import decks
import random
from cards import Card


class Context:
    def __init__(self):
        self.state: State = TitleScreen()  # by default, start the title screen

    def handle_events(self):
        self.state = self.state.handle_events()

    def is_running(self):
        return self.state.is_running()


class State:
    def __init__(self, objects=None, animations=None, transition=False):
        self.objects: dict[str, Button | Card] = objects if objects else {}
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
        for object in self.objects.values():
            if object.rect.collidepoint(x, y):
                object.is_hovered = True
            else:
                object.is_hovered = False

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

        for offset in range(0, 301, 15):
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

        for offset in range(0, 301, 15):
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

        deck = decks.generate_full_deck()
        random.shuffle(deck)
        for i in range(len(deck)):
            self.objects[f'test_card_{i}'] = deck[i]
            self.objects[f'test_card_{i}'].set_at(random.randint(70, 100), random.randint(70, 200), random.randint(-40, 40))

    def handle_events(self):
        if _check_for_quit():
            return Quit(objects=self.objects, animations=self.animations)

        x, y = pygame.mouse.get_pos()
        for object in self.objects.values():
            if object.collides_with(x, y):
                object.is_hovered = True
                if not object.is_flipping:
                    self.animations.append(self.flip_over_card_animation(object))
                    object.is_flipping = True
            else:
                object.is_hovered = False

        for event in pygame.event.get(MOUSEBUTTONUP):
            x, y = event.pos
            selected_objects = []
            for object in self.objects.values():
                if object.collides_with(x, y):
                    object.is_selected = not object.is_selected
                    selected_objects.append(object)
                else:
                    object.is_selected = False
            if selected_objects:
                self.animations.append(self.translate_card_animation(selected_objects[-1], 800, 400, -45))
        return self

    def translate_card_animation(self, card, cx, cy, angle):
        curr_x, curr_y = card.center
        curr_angle = card.angle
        animation_speed = 45
        for t in range(animation_speed):
            offset_x = curr_x + (cx - curr_x) * t / (animation_speed - 1)
            offset_y = curr_y + (cy - curr_y) * t / (animation_speed - 1)
            offset_angle = curr_angle + (angle - curr_angle) * t / (animation_speed - 1)
            card.set_at(offset_x, offset_y, offset_angle)
            yield {key: card for key in self.objects if self.objects[key] == card}

    def flip_over_card_animation(self, card):
        curr_image = card.get_image()
        image_w, image_h = curr_image.get_size()
        animation_speed = 15
        for ts in [range(animation_speed), range(animation_speed, -1, -1)]:
            for t in ts:
                offset_image_w = image_w * (1 - t / animation_speed)
                offset_image_h = image_h * (1 + 0.2 * t / animation_speed)
                offset_image = pygame.transform.scale(curr_image, (offset_image_w, offset_image_h))
                card.set_image(offset_image)
                yield {key: card for key in self.objects if self.objects[key] == card}
            if ts == range(animation_speed, -1, -1):
                continue
            card.is_flipped = not card.is_flipped
            card.set_at(*card.center, -card.angle)
            curr_image = card.get_image()


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

    def hover(self):
        hovered_image_rect = self.hovered_image.get_rect()
        hovered_image_rect.center = self.rect.center

        return self.hovered_image, hovered_image_rect, self.image, self.rect, self.text

    def get_image(self):
        return self.image
