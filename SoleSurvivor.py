import pygame
import random
import math
from math import atan2, degrees, pi

class Player ():
    def __init__(self, pos=(250,250), life=1000):
        self.pos = pos
        self.color = pygame.Color(255, 255, 255)
        self.size = 50
        self.life = 3
        self.speed = 0.5
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
    def __init__(self, pos=(0,0), target=(0,0)):
        self.pos = pos
        self.target = target
        self.color = pygame.Color(0, 255, 80)
        self.damage = 1
        self.size = 50
        self.life = 3
        self.speed = 550 # amount of frames it takes to reach target
        self.dead = False
        self.alpha = 255
        self.surface = self.update_surface()
        #find vector to target
        x1 = self.pos[0]
        y1 = self.pos[1]
        x2 = self.target[0]
        y2 = self.target[1]
        self.dx = (x2 - x1)
        self.dy = (y2 - y1)
        
    def update(self):
        if self.life < 1:
            self.dead = True
        #update projectile position
        x=self.pos[0]
        y=self.pos[1]
        x += self.dx / self.speed
        y += self.dy / self.speed
        self.pos = [x,y]
        
        
        
        
        
    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.color)
        pygame.draw.rect(surf, self.color, (self.size, self.size, self.size, self.size))
        return surf
    
    def draw(self, surface):
        if self.dead == True:
            return
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)
    

class Enemy ():
    def __init__(self, pos=(0,0)):
        return 0
    
class Game ():
    def __init__(self, screen_res):
        self.resolution = screen_res
        self.player = Player()
        self.projectiles = []
        self.birth_tracker = 1
        self.attack_rate = 800
        
    def update(self):
        self.player.update()
        self.make_projectile()
        self.update_projectiles()
        
    def draw(self, surf):
        self.player.draw(surf)
        for projectile in self.projectiles:
            projectile.draw(surf)
        
    def make_projectile(self):
        if self.birth_tracker % self.attack_rate == 0:
            bullet = Projectile(self.player.pos, pygame.mouse.get_pos())
            self.projectiles.insert(0, bullet)
        self.birth_tracker += 1
        
    def update_projectiles(self):
        for idx, projectile in enumerate(self.projectiles):
            projectile.update()
            if self._projectile_is_offscreen(projectile):
                del self.projectiles[idx]
                
    def _projectile_is_offscreen(self, projectile):
        projectile_is_offscreen = False
        if projectile.pos[0] > self.resolution[0]:
            projectile_is_offscreen = True
        if projectile.pos[1] > self.resolution[1]:
            projectile_is_offscreen = True
        return projectile_is_offscreen
        

def main():
    #game setup
    pygame.init()
    pygame.display.set_caption("Sole Survivor")
    resolution = (1280, 720)
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