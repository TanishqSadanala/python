import sys
import pygame
import random
from vector import Vector

Window = 700 
pygame.display.set_caption("Space Invasion Clone")
WindowSurface = pygame.display.set_mode([Window]*2)


Window_Config = {
    'background' : 'grey12',
    'MenuFont'   : 'Consolas',
    'gridline'   : '#EEEEEE'
}

Objects_Config = {
    'size'          : Vector(random.randrange(20, 100), random.randrange(20,200)), # not used
    'position'      : Vector(random.randrange(10, 200), random.randrange(10,200)), # not used
    'color'         : ['lightblue', 'lightgreen', 'beige', 'orange']
}

Player_Config = {
    'color'          : 'white',
    'size'           : Vector(60,20),
    'position'       : Vector((Window/2 - 20), 650),
    'bulletsize'     : Vector(10,10),
    'bulletposition' : Vector((Window/2 - 20), 500)
}

class fallingObjects(pygame.sprite.Sprite):
    def __init__(self, color, size: 'Vector', position: 'Vector') -> None:
        super().__init__()
        self.objectColor = color
        self.objectsize = size
        self.objectPosition = position
        self.image = pygame.Surface((self.objectsize.x, self.objectsize.y))
        self.image.fill(self.objectColor)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.objectPosition.x, self.objectPosition.y)
        
    def update(self) -> None:
        self.rect.y += 3 
        if self.rect.top > Window or self.objectsize.x > 30 or self.objectsize.y > 30:
            self.kill()
    
class player(pygame.sprite.Sprite):
    def __init__(self, color: str, size: 'Vector', position: 'Vector') -> None:
        super().__init__()
        self.playerColor = color
        self.playerSize = size
        self.playerPosition = position
        self.playerImage = pygame.Surface((self.playerSize.x, self.playerSize.y))
        self.playerImage.fill(self.playerColor)
        self.rect = self.playerImage.get_rect()
        self.rect.topleft = (self.playerPosition.x, self.playerPosition.y)
        
    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < Window:
            self.playerPosition.x += 5
        if keys[pygame.K_LEFT]and self.rect.left > 0: 
            self.playerPosition.x -= 5

            
    def bullet_respwn(self):
        return bullets(self.playerPosition)

class bullets(pygame.sprite.Sprite):
        def __init__(self, position: Vector):
            super().__init__()
            self.bulletposition = position
            self.image = pygame.Surface((10,10))
            self.image.fill('white')
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.bulletposition.x+5, self.bulletposition.y+5)

        def update(self) -> None:
            self.rect.y -= 1
            if self.rect.top < 0:
                self.kill()            

class Application():
    
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.ScoreCount = 0
        self.faiingObjGroup = pygame.sprite.Group()
        self.bulletgroup = pygame.sprite.Group()    
        
        
    def fps(self):
        self.clock.tick(60)
        self.frames = round(self.clock.get_fps(), 2)
        return self.frames
    
    def FPS_score_display(self):
        fps_font = pygame.font.SysFont(Window_Config['MenuFont'], 20)
        self.FPScount = fps_font.render(f"FPS:{self.fps()}", 'black', '#B0B0B0')
        score_font = pygame.font.SysFont(Window_Config['MenuFont'], 20)
        self.Scorecount = score_font.render(f"Score:{self.ScoreCount}", 'black', '#B0B0B0')
        return self.FPScount, self.Scorecount
    
    def fallingObjects(self):
            self.square = fallingObjects(random.choice(Objects_Config['color']),Vector(random.randrange(20, 60), random.randrange(20,60)), Vector(random.randrange(20, 600), random.randrange(-200,-100)))
            self.faiingObjGroup.add(self.square)
            self.faiingObjGroup.draw(WindowSurface)
            self.faiingObjGroup.update()
            
    def playerObject(self):
        self.player = player(Player_Config['color'], Player_Config['size'], Player_Config['position'])
        WindowSurface.blit(self.player.playerImage, (self.player.playerPosition.x, self.player.playerPosition.y))
        self.player.update()
        
    def bulletobject(self):
        self.bullets = bullets(Player_Config['bulletposition'])
        for event in self.quit_handler():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:    
                    self.bulletgroup.add(self.player.bullet_respwn())
        for bullet in self.bulletgroup:
            self.bulletgroup.draw(WindowSurface)
            self.bulletgroup.update()

    def DisplayObjects(self):
        fps, score = self.FPS_score_display()
        WindowSurface.fill(Window_Config['background'])
        self.playerObject()
        self.bulletobject()
        self.fallingObjects()
        WindowSurface.blit(fps,(2,2))
        WindowSurface.blit(score,(Window-100,2))
        pygame.display.flip()
        
    def collision(self):
        bullet_obj_collision = pygame.sprite.groupcollide(self.bulletgroup, self.faiingObjGroup, False, True)
        for collisions in bullet_obj_collision:
            self.ScoreCount +=1
        player_obj_collision = pygame.sprite.spritecollide(self.player, self.faiingObjGroup, False)
        for collisions in player_obj_collision:
            self.ScoreCount = 0
            print("game over")
            sys.exit()
      
    def quit_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
            yield event  
             
             
    def run(self):
        while(1):
            self.DisplayObjects()
            self.collision()
            self.quit_handler()
            
if __name__ == '__main__':
    Application().run()



