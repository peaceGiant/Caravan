import pygame
import math


# Display surface
display_surf = ...

# Window constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
WINDOW_FLAGS = pygame.RESIZABLE | 0

# Colors
BG_COLOR = (255, 150, 0)

clock = pygame.time.Clock()
FPS = 60


def init():
    global display_surf
    display_surf = pygame.display.set_mode(
        size=(WINDOW_WIDTH, WINDOW_HEIGHT),
        flags=WINDOW_FLAGS
    )
    pygame.display.set_caption('Caravan')


def handle_events():
    return None


def display(state):
    global display_surf
    old_surface = display_surf.copy()

    display_surf.fill(BG_COLOR)

    font = pygame.font.Font(None, size=50)
    surf = font.render(f'{state}', True, (255, 0, 255), (40, 40, 40))
    display_surf.blit(surf, (20, 20))

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

        text_surf = font.render(object.text, True, (255, 0, 0)).convert_alpha()
        rect = text_surf.get_rect()
        rect.center = object.rect.center
        display_surf.blit(text_surf, rect)

    if currently_hovered == currently_selected and currently_hovered:
        currently_hovered = None

    if currently_selected:
        selected_image, selected_image_rect, image, image_rect, text = currently_selected.click()

        display_surf.blit(selected_image, selected_image_rect)
        display_surf.blit(image, image_rect)

        text_surf = font.render(currently_selected.text, True, (255, 0, 0)).convert_alpha()
        rect = text_surf.get_rect()
        rect.center = image_rect.center
        display_surf.blit(text_surf, rect)
    if currently_hovered:
        hovered_image, hovered_image_rect, image, image_rect, text = currently_hovered.hover()

        display_surf.blit(hovered_image, hovered_image_rect)
        display_surf.blit(image, image_rect)

        text_surf = font.render(currently_hovered.text, True, (255, 0, 0)).convert_alpha()
        rect = text_surf.get_rect()
        rect.center = image_rect.center
        display_surf.blit(text_surf, rect)

    new_surface = display_surf.copy()

    if state.transition:
        state.transition = False
        display_transition_animation(old_surface, new_surface)

    pygame.display.update()
    clock.tick(FPS)


def get_visible_objects(objects):
    result = [object for object in objects.values() if object.is_visible]
    return sorted(result, key=lambda x: x.z_index)


def display_transition_animation(old_surface, new_surface):
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
                if t <= 30 * box:
                    continue
                if t >= 30 * box + 90:
                    index = 90
                else:
                    index = (t - 30 * box) % 90
                boxx = box_width // 2 + box * box_width
                box_coords = [(boxx + x, y) for x, y in coords[index]]
                pygame.draw.polygon(display_surf, (255, 100, 255), box_coords)
            pygame.display.update()
            clock.tick(FPS * 8.2)

        pygame.time.wait(200)
        display_surf.fill(BG_COLOR)
        old_surface = new_surface
