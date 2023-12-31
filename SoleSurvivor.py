import pygame
import random
import math
from math import atan2, degrees, pi

class Player ():
    def __init__(self, pos=(250,250)):
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
    def __init__(self, pos=(250,250)):
        self.pos = pos
        self.color = pygame.Color(255, 0, 0)
        self.size = 50
        self.life = 1
        self.speed = 2500
        self.dead = False
        self.alpha = 255
        self.surface = self.update_surface()
        self.last_movement = (0,0)
        
    def update(self, player_pos):
        pos = player_pos
        if self.life < 1:
            self.dead = True
        #update enemy position
        x=self.pos[0]
        y=self.pos[1]
        x1 = self.pos[0]
        y1 = self.pos[1]
        x2 = pos[0]
        y2 = pos[1]
        dx = (x2 - x1)
        dy = (y2 - y1)
        temp_speed = self.speed * ((math.sqrt((dx * dx) + (dy * dy))) / 500)
        x += dx / temp_speed
        y += dy / temp_speed
        self.pos = [x,y]
        self.last_movement = (dx/temp_speed,dy/temp_speed)
    
    def undo_movement(self):
        x=self.pos[0]
        y=self.pos[1]
        dx = self.last_movement[0]
        dy = self.last_movement[1]
        temp_speed = self.speed * ((math.sqrt((dx * dx) + (dy * dy))) / 500)
        x -= dx / temp_speed
        y -= dy / temp_speed
        self.pos = (x + random.randrange(-10, 10),y + random.randrange(-3, 3))
        
    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill((255, 0, 0))
        pygame.draw.rect(surf, self.color, (self.size, self.size, self.size, self.size))
        return surf
    
    def draw(self, surface):
        if self.dead == True:
            return
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)
    def is_intersecting(self, pos, size):
        return False
    
class Game ():
    def __init__(self, screen_res):
        self.resolution = screen_res
        self.player = Player()
        self.projectiles = []
        self.birth_tracker = 1
        self.attack_rate = 800 # lower number equals faster firing
        self.spawn_rate = 750 # lower number equals faster spawning
        self.spawn_tracker = 1
        self.enemies = []
        
    def update(self):
        self.player.update()
        self.make_projectile()
        self.update_projectiles()
        self.make_enemy()
        self.update_enemies()
        self.check_collision()
        
    def check_collision(self):
        #check enemies are not touching enemies
        for idx1, enemy1 in enumerate(self.enemies):
            for idx2, enemy2 in enumerate(self.enemies):
                if self.is_touching_enemy(enemy1, enemy2):
                    enemy1.undo_movement()
                    enemy2.undo_movement()
                    
        #check enemies are not touching projectiles
        for idx, enemy in enumerate(self.enemies):
            for idx2, projectile in enumerate(self.projectiles):
                if self.is_touching_projectile(enemy, projectile):
                    del self.enemies[idx]
                    del self.projectiles[idx2]
        #check enemies are not touching player
        for idx, enemy in enumerate(self.enemies):
            if self.is_touching_player(enemy):
                del self.enemies[idx]
                self.player.life -= 1

        return
    
    def is_touching_enemy(self, enemy1, enemy2):
        touching = False
        enemy1x = (enemy1.pos[0] + 25)
        enemy1y = (enemy1.pos[1] + 25)
        enemy2x = (enemy2.pos[0] + 25)
        enemy2y = (enemy2.pos[1] + 25)
        distance = math.sqrt(((enemy2x - enemy1x)*(enemy2x - enemy1x)) + ((enemy2y - enemy1y)*(enemy2y - enemy1y)))
        if distance <36 and enemy1.pos[0] != enemy2.pos[0] and enemy1.pos[1] != enemy2.pos[1]:
            touching = True
        return touching
        
    def is_touching_player(self, enemy):
        touching = False
        player_centerx = (self.player.pos[0] + 25)
        player_centery = (self.player.pos[1] + 25)
        enemy_centerx = (enemy.pos[0] + 25)
        enemy_centery = (enemy.pos[1] + 25)
        distance = math.sqrt(((enemy_centerx - player_centerx)*(enemy_centerx - player_centerx)) + ((enemy_centery - player_centery)*(enemy_centery - player_centery)))
        if distance <36:
            touching = True
        return touching

    def is_touching_projectile(self, enemy, projectile):
        touching = False
        projectile_centerx = (projectile.pos[0] + 25)
        projectile_centery = (projectile.pos[1] + 25)
        enemy_centerx = (enemy.pos[0] + 25)
        enemy_centery = (enemy.pos[1] + 25)
        distance = math.sqrt(((enemy_centerx - projectile_centerx)*(enemy_centerx - projectile_centerx)) + ((enemy_centery - projectile_centery)*(enemy_centery - projectile_centery)))
        if distance <36:
            touching = True
        return touching
        
    def draw(self, surf):
        self.player.draw(surf)
        for projectile in self.projectiles:
            projectile.draw(surf)
        for enemy in self.enemies:
            enemy.draw(surf)
    
    def make_enemy(self):
        screen_width = self.resolution[0] 
        screen_height = self.resolution[1]
        spawn_side = random.randrange(0, 3)
        if spawn_side == 0:
            x = screen_width
            y = random.randrange(0, screen_height)
        if spawn_side == 1:
            x = random.randrange(0, screen_width)
            y = screen_height
        if spawn_side == 2:
            x = 0
            y = random.randrange(0, screen_height)
        if spawn_side == 3:
            x = random.randrange(0, screen_width)
            y = 0
        
        spawn_location = (x,y)
        if self.spawn_tracker % self.spawn_rate == 0:
            enemy = Enemy(spawn_location)
            self.enemies.insert(0, enemy)
        self.spawn_tracker += 1

    def update_enemies(self):
        for idx, enemy in enumerate(self.enemies):
            enemy.update(self.player.pos)
    
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
        if game.player.dead == True:
            running = False
        # render
        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        game.draw(screen)
        pygame.display.flip()
    pygame.quit
    
if __name__ == "__main__":
    main()