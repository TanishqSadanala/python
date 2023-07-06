import pygame
import sys
import random
from vector import vector


Window_size = 600
WindowSurface = pygame.display.set_mode([Window_size]* 2)
pygame.display.set_caption('Snake')



Window_Config = {
    'background' : 'beige',
    'MenuFont'   : 'sans.tff',
    'gridline'   : '#EEEEEE'
}

Snake_Config = {
    'SnakeColor'    : '#8c6e4f',
    'SnakePosition' : vector(Window_size/3, Window_size/3),  # default position
    'SnakeSize'     : vector(20,20),
    }

Food_config = {
    'FoodColor'    : '#ed755c',
    'FoodPosition' : vector(random.randrange(Snake_Config['SnakeSize'].x,Window_size, Snake_Config['SnakeSize'].y), 
                            random.randrange(Snake_Config['SnakeSize'].x,Window_size, Snake_Config['SnakeSize'].y)),  #in screen bounds
    'FoodSize'     : vector(20,20) 
}

MovementKey_config = {
    pygame.K_UP    :  vector(0, -20),
    pygame.K_RIGHT :  vector(20, 0),
    pygame.K_DOWN  :  vector(0, 20),
    pygame.K_LEFT  :  vector(-20, 0)
}


    
class Grid(object):
    def drawGrid(self) -> None:
        [pygame.draw.line(surface=WindowSurface, color=Window_Config['gridline'], 
                        start_pos=(x, 0), end_pos=(x, Window_size),width=1) for x in range(0, Window_size, Snake_Config['SnakeSize'].x)]
        [pygame.draw.line(surface=WindowSurface, color=Window_Config['gridline'], 
                        start_pos=(0, y), end_pos=(Window_size, y),width=1)for y in range(0, Window_size, Snake_Config['SnakeSize'].y)]

class GenerateRectangles(object):
    def __init__(self, color: str, size: vector, position: vector) -> None:
        self._genRect_color = color
        self._genRect_size = size
        self._genRect_position = position
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._genRect_position == other._genRect_position    
       
    def draw(self):
        self.rect = pygame.Rect(self._genRect_position.x, self._genRect_position.y,
                                self._genRect_size.x,self._genRect_size.y)
        pygame.draw.rect(WindowSurface, self._genRect_color, self.rect)

class Snake(GenerateRectangles):
    
    def __init__(self, color: str, size: vector, position: vector) -> None:
        super().__init__(color, size, position)
        self._snakeColor = color
        self._snakeSize = size 
        self._snakeDirection = MovementKey_config[pygame.K_RIGHT]
        self.snake_rects = [GenerateRectangles(color, size, position)]
        self.snake_alive = True
        

    def draw(self):
        for snake_rects in self.snake_rects:
            snake_rects.draw()
            
    def move(self):
        keys =  pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self._snakeDirection = MovementKey_config[pygame.K_LEFT]
        if keys[pygame.K_RIGHT]:
                self._snakeDirection = MovementKey_config[pygame.K_RIGHT]
        if keys[pygame.K_UP]:
            self._snakeDirection = MovementKey_config[pygame.K_UP]
        if keys[pygame.K_DOWN]:
            self._snakeDirection = MovementKey_config[pygame.K_DOWN]
        
        
        self.NextPos_Snake = GenerateRectangles(self._snakeColor,self._snakeSize, (self.snake_rects[-1]._genRect_position + self._snakeDirection))
        
        
        if ( self.NextPos_Snake in self.snake_rects or self.NextPos_Snake._genRect_position.x > Window_size or 
            self.NextPos_Snake._genRect_position.x < 0 or
            self.NextPos_Snake._genRect_position.y > Window_size or
            self.NextPos_Snake._genRect_position.y < 0):
            self.snake_alive =  False
            
        self.snake_rects.append(self.NextPos_Snake)
        return self.NextPos_Snake
        
    def delete_Trail(self):
        self.snake_rects.pop(0)
        
    def add_tail(self):
        self.snake_rects.append(self.NextPos_Snake)
        
    def collision(self):
        return self.snake_alive
        
class Food(GenerateRectangles):
    def __init__(self, color: str, size: vector, position: vector) -> None:
        super().__init__(color, size, position)
        self.foodcolor = color
        self.foodsize = size
        self.foodposition = position
        
class Application():
    
    def __init__(self) -> None:
        pygame.init()
        self.ScoreCount = 0
        self.clock = pygame.time.Clock()
        self.new_game()
        
    def fps(self):
        self.clock.tick(20)
        self.frames = round(self.clock.get_fps(), 2)
        return self.frames
    
    def FPS_score_display(self):
        fps_font = pygame.font.SysFont("Arial", 20)
        self.FPScount = fps_font.render(f"FPS:{self.fps()}", 'black', '#B0B0B0')
        score_font = pygame.font.SysFont("Arial", 20)
        self.Scorecount = score_font.render(f"Score:{self.ScoreCount}", 'black', '#B0B0B0')
        return self.FPScount, self.Scorecount
        
    def DisplayObjects(self):
        fps, score = self.FPS_score_display()
        WindowSurface.fill(Window_Config['background'])
        self._menu  = Grid().drawGrid()
        self._snake.draw()
        self._food.draw()
        WindowSurface.blit(fps,(2,2))
        WindowSurface.blit(score,(Window_size-100,2))
        pygame.display.flip()

    def generateNewFood(self):
        self._food  = Food(Food_config['FoodColor'], Food_config['FoodSize'],
                           vector(random.randrange(Snake_Config['SnakeSize'].x,Window_size, Snake_Config['SnakeSize'].y), 
                            random.randrange(Snake_Config['SnakeSize'].x,Window_size, Snake_Config['SnakeSize'].y)))
        
    def new_game(self):
        self._food  = Food(Food_config['FoodColor'], Food_config['FoodSize'], Food_config['FoodPosition'])
        self._snake = Snake(Snake_Config['SnakeColor'], Snake_Config['SnakeSize'], Snake_Config['SnakePosition'])
        self.generateNewFood()
        
    def translate(self):
        self.Snakeposition = self._snake.move() 
        self._snake.delete_Trail()
        
    def Collision(self):
        if self._snake.snake_alive and self.Snakeposition._genRect_position == self._food._genRect_position:
            self.generateNewFood()
            self.ScoreCount += 1
            self._snake.add_tail()
        if not self._snake.snake_alive:
            self.ScoreCount = 0
            self.new_game()
        
    def quit_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
    
    def run(self):
        while(1):
            self.DisplayObjects()
            self.translate()
            self.Collision()
            self.quit_handler()
    
    
if __name__ == '__main__':
    Application().run()
