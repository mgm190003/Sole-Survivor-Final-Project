import pygame
import random

class Player ():
    def __init__(self, pos=(50,50), life=1000):
        self.pos = pos
        self.color = pygame.Color(255, 255, 255)
        self.size = 50
        self.life = 3
        self.speed = 0.2
        self.dead = False
        self.alpha = 255
        self.surface = self.update_surface()
        
    def update(self):
        if self.life < 1:
            self.dead = True
        #update player position
        keys = pygame.key.get_pressed()
        x=self.pos[0]
        y=self.pos[1]
        x += (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed
        y += (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed
        self.pos = [x,y]
        
            

        
    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill((255, 255, 255))
        pygame.draw.rect(surf, self.color, (self.size, self.size, self.size, self.size))
        return surf
    
    def draw(self, surface):
        if self.dead == True:
            return
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)
        
        

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
    def update(self):
        self.player.update()
    def draw(self, surf):
        self.player.draw(surf)
        

def main():
    #game setup
    pygame.init()
    pygame.display.set_caption("Sole Survivor")
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
        game.update()
        # render
        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        game.draw(screen)
        pygame.display.flip()
    pygame.quit
    
if __name__ == "__main__":
    main()