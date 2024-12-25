import pygame
import graphics
from states import Context


def start():
    pygame.init()
    graphics.init()

    context = Context()
    while context.is_running():  # game loop

        # handle events and update state
        graphics.handle_events()
        context.handle_events()

        # update display
        graphics.display(context.state)

    pygame.quit()
