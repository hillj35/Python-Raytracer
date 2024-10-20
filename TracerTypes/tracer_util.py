import math
import random

# Helper classes
class interval:
    def __init__(self, min: float = float("inf"), max: float = float("-inf")):
        self.min = min
        self.max = max

    def size() -> float:
        return max - min
    
    def contains(self, x: float) -> bool:
        return self.min <= x <= self.max
    
    def surrounds(self, x: float) -> bool:
        return self.min < x < self.max
    
    def clamp(self, x: float) -> float:
        if x < self.min:
            return self.min
        if x > self.max:
            return self.max
        return x 

# Helper methods
def degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 180.0

def random_float(min: float = 0, max: float = 1) -> float:
    return random.random() * (max - min) + min


# Constants
EMPTY_INTERVAL = interval(float("inf"), float("-inf"))
UNIVERSE_INTERVAL = interval(float("-inf"), float("inf"))