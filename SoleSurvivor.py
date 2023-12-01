import pygame
import random

class Player ():
    def __init__(self, location=(0,0)):
        self.location = location


    def update_player(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.location[0] -= 1
                if event.key == pygame.K_RIGHT:
                    self.location[0] += 1
                if event.key == pygame.K_DOWN:
                    self.location[1] -= 1
                if event.key == pygame.K_UP:
                    self.location[1] += 1

class Projectile ():
    def __init__(self, pos=(0,0)):


class Enemy ():
    def __init__(self, pos=(0,0)):


def main():
    #game setup
    pygame.init
    pygame.display.set_caption("Sole Survivor")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (1920, 1060)
    screen = pygame.display.set_mode(resolution)
    game = game(resolution)
    running = True
    #game loop
    while running:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # game logic
        # render
        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        pygame.display.flip()
        dt = clock.tick(12)
    pygame.quit
    
if __name__ == "__main__":
    main()