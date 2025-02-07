import pygame
from pygame.locals import QUIT
import math


# Display surface
display_surf = ...

# Window constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
WINDOW_FLAGS = pygame.RESIZABLE | pygame.DOUBLEBUF | 0

# Colors
BG_COLOR = (255, 150, 0)
TEXT_COLOR = (0, 0, 0)

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load('assets/backgrounds/background.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
BUTTON_IMAGE = pygame.image.load('assets/backgrounds/button.png')

player_1_turn_sound = ...
player_2_turn_sound = ...

clock = pygame.time.Clock()
FPS = 80


def init():
    global display_surf, player_1_turn_sound, player_2_turn_sound
    display_surf = pygame.display.set_mode(
        size=(WINDOW_WIDTH, WINDOW_HEIGHT),
        flags=WINDOW_FLAGS
    )
    pygame.display.set_caption('Caravan')
    pygame.display.set_icon(pygame.image.load('assets/cards/card_red_joker.png'))

    pygame.mixer.init()
    pygame.mixer.music.load('assets/music/Smash Sketch.mp3')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)

    player_1_turn_sound = pygame.mixer.Sound('assets/audio/player_1_turn.mp3')
    player_2_turn_sound = pygame.mixer.Sound('assets/audio/player_2_turn.mp3')
    player_1_turn_sound.set_volume(1)
    player_2_turn_sound.set_volume(1)


def handle_events():
    global WINDOW_WIDTH, WINDOW_HEIGHT, display_surf

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            new_width = max(round(event.w, -2), 600)
            new_height = max(round(event.h, -2), 400)
            WINDOW_WIDTH, WINDOW_HEIGHT = new_width, new_height
            display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=WINDOW_FLAGS)
        else:
            pygame.event.post(event)


def display(state):
    global display_surf
    old_surface = display_surf.copy()

    # display_surf.fill(BG_COLOR)
    display_surf.blit(BACKGROUND_IMAGE, BACKGROUND_IMAGE.get_rect())

    font = pygame.font.Font('assets/fonts/THE_FONT.ttf', size=26)
    # surf = font.render(f'{state}', True, (255, 0, 255), (40, 40, 40))
    # display_surf.blit(surf, (20, 20))

    for animation in state.animations[:]:
        objects = next(animation, {})

        if not objects:
            state.animations.remove(animation)
            continue

        for key, val in objects.items():
            state.objects[key] = val

    currently_hovered = None
    currently_selected = None
    for object in get_visible_objects(state.objects):
        if object.is_hovered:
            currently_hovered = object
        if object.is_selected:
            currently_selected = object

        display_surf.blit(object.get_image(), object.rect)

        text_surf = font.render(object.text, True, object.font_color).convert_alpha()
        rect = text_surf.get_rect()
        rect.center = object.rect.center
        display_surf.blit(text_surf, rect)

    if currently_hovered == currently_selected and currently_hovered:
        currently_hovered = None

    if currently_selected:
        selected_image, selected_image_rect, image, image_rect, text = currently_selected.get_clicked_params()

        display_surf.blit(selected_image, selected_image_rect)
        display_surf.blit(image, image_rect)

        text_surf = font.render(currently_selected.text, True, currently_selected.font_color).convert_alpha()
        rect = text_surf.get_rect()
        rect.center = image_rect.center
        display_surf.blit(text_surf, rect)
    if currently_hovered:
        hovered_image, hovered_image_rect, image, image_rect, text = currently_hovered.get_hovered_params()

        display_surf.blit(hovered_image, hovered_image_rect)
        display_surf.blit(image, image_rect)

        text_surf = font.render(currently_hovered.text, True, currently_hovered.font_color).convert_alpha()
        rect = text_surf.get_rect()
        rect.center = image_rect.center
        display_surf.blit(text_surf, rect)

    new_surface = display_surf.copy()

    if state.transition:
        state.transition = False
        if state.audible:
            pygame.mixer.music.fadeout(100)
            if 'TitleScreen' in str(type(state)):
                pygame.mixer.music.load('assets/music/Smash Sketch.mp3')
                pygame.mixer.music.set_volume(.1)
            elif 'StandardMode' in str(type(state)):
                pygame.mixer.music.load('assets/music/Thief in the Night (Standard).mp3')
                pygame.mixer.music.set_volume(.3)
            elif 'PvPMode' in str(type(state)):
                pygame.mixer.music.load('assets/music/Walking Along (PvP).mp3')
                pygame.mixer.music.set_volume(.7)
        
        display_transition_animation(old_surface, new_surface, state.audible)
        return

    pygame.display.update()
    clock.tick(FPS)


def get_visible_objects(objects):
    result = []
    for object in objects.values():
        result.extend(object.dump())
    result = [object for object in result if object.is_visible]
    return sorted(result, key=lambda x: x.z_index)


def display_transition_animation(old_surface, new_surface, audible):
    box_width = 50
    coords = []
    for angle_offset in range(0, 91, 1):
        angle = math.radians(90 + angle_offset)
        x, y = box_width // 2 * math.cos(angle), box_width // 2 * math.sin(angle)
        coord = [
            (x, y),
            (-x, -y),
            (-x, WINDOW_HEIGHT - y),
            (x, WINDOW_HEIGHT + y)
        ]
        coords.append(coord)

    for ts in [range(60 + WINDOW_WIDTH // box_width * 30), range(60 + WINDOW_WIDTH // box_width * 30, -1, -1)]:
        for t in ts:
            display_surf.blit(old_surface, (0, 0))
            for box in range(WINDOW_WIDTH // box_width):
                pygame.event.get()
                if t <= 30 * box:
                    continue
                if t >= 30 * box + 90:
                    index = 90
                else:
                    index = (t - 30 * box) % 90
                boxx = box_width // 2 + box * box_width
                box_coords = [(boxx + x, y) for x, y in coords[index]]
                pygame.draw.polygon(display_surf, (128, 0, 0), box_coords)
            pygame.display.update()
            clock.tick(FPS * 6)
        if ts != range(60 + WINDOW_WIDTH // box_width * 30, -1, -1):
            if audible:
                pygame.mixer.music.play(loops=-1)
        pygame.time.wait(200)
        old_surface = new_surface
