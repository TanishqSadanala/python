import random
# vector module

class vector(object):
    
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        
    def __add__(self, other):
       return vector(self.x + other.x, self.y + other.y)
      
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    
    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y
    
