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

# Helper methods
def degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 180.0

def random_float(min: float, max: float) -> float:
    return random.random() * (max - min) + min


# Constants
EMPTY_INTERVAL = interval(float("inf"), float("-inf"))
UNIVERSE_INTERVAL = interval(float("-inf"), float("inf"))