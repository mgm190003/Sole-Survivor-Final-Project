import pygame
import random

class Player ():
    def __init__(self, location=(0,0)):
        self.location = location
        self.life = 3


    def update_player(self):
        #update position
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
        self._draw_player()
    
    def _draw_player(self):
        surf = pygame.Surface((25, 25))
        surf.fill((0, 0, 0))
        pygame.draw.rect(surf, (255, 255, 255), (25, 25, 25, 25))
        return surf
        
        

class Projectile ():
    def __init__(self, pos=(0,0)):
        return 0

class Enemy ():
    def __init__(self, pos=(0,0)):
        return 0
    
class Game ():
    def __init__(self, screen_res):
        self.resolution = screen_res
        self.player = Player()
    def update(self, dt):
        self.player.update_player()
        

def main():
    #game setup
    pygame.init()
    pygame.display.set_caption("Sole Survivor")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    game = Game(resolution)
    running = True
    #game loop
    while running:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # game logic
        game.update(dt)
        # render
        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        pygame.display.flip()
        dt = clock.tick(12)
    pygame.quit
    
if __name__ == "__main__":
    main()