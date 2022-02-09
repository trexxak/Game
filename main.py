import pygame
from scenes import *

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.USEREVENT+0])
make_font("Assets/Sidewinder2022-Regular.otf", 84)
make_font("Assets/fonts/FatSkelly-Regular.ttf", 84)
make_font("Assets/fonts/ThinPharao-Regular.ttf", 84)

def start():
    paused = False
    active_scene = Splash()
    screen = pygame.display.set_mode(get_dimensions(), pygame.FULLSCREEN | pygame.DOUBLEBUF, 8)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if paused:
                        pygame.mixer.music.unpause()
                        paused = False
                    else:
                        pygame.mixer.music.pause()
                        paused = True
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            if quit_attempt:
                active_scene.terminate()
            else:
                filtered_events.append(event)
        active_scene.input(filtered_events, pressed_keys)
        active_scene.update()
        active_scene.render(screen)
        active_scene = active_scene.next
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    start()
