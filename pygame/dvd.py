import random
import sys

import pygame

class game:
    def __init__(self):
        pygame.init()
        self.window_size = 400
        self.window = pygame.display.set_mode([self.window_size] * 2)
        self.fpd = pygame.time.Clock()
        self.x_pos = random.randrange(0, 300)
        self.y_pos = random.randrange(0, 300)
        self.speed = random.randrange(1, 6)
        self.speed2 = 2
        self.random_angle = random.randrange(1,5)
        self.color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))


    def window_update(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def random(self):
        self.randdomxy = (random.randrange(0,300),random.randrange(0,300))
        return self.randdomxy

    def delta_time(self):
        self.fpd.tick(60) / 1000

    def move(self):
        pygame.draw.rect(self.window, self.color, (self.x_pos,self.y_pos,30,30))
        print(self.x_pos, self.y_pos)
        self.x_pos += self.speed
        self.y_pos += self.speed2
        if self.x_pos >= 370 or self.x_pos < 1:
            self.speed = -self.speed
            self.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))

        if self.y_pos <1 or self.y_pos >=370:
            self.speed2 = -self.speed2
            self.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))



        pygame.display.flip()
        self.window.fill((0, 0, 0))

    def app_run(self):
        while True:
            self.move()
            self.delta_time()
            self.window_update()
            self.random()




if __name__ == "__main__":
    obj = game()
    obj.app_run()
