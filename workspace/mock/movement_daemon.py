import numpy as np
import math
import time
from threading import Thread
from workspace.utils.geometry import rotate

class MovementDaemon(Thread):
    def __init__(self, shared_memory):
        super(MovementDaemon, self).__init__()
        self.daemon = True
        self.shared_memory = shared_memory
        self.x_speed = 0
        self.y_speed = 0
        self.direction_speed = 0

    def run(self):
        while True:
            direction = self.shared_memory.get_direction_simulation()
            direction += self.direction_speed
            self.shared_memory.set_direction_simulation(direction)
            
            walk_vector = rotate([self.x_speed, self.y_speed], math.radians(direction))
            current_position = self.shared_memory.get_position_simulation()
            self.shared_memory.set_position_simulation(walk_vector + current_position)

    def move(self, x, y, direction):
        if x >= 0:
            self.x_speed = x * 11.5 # NAO real forward speed 11.5cm/sec
        else:
            self.x_speed = x * 9.5 # Nao real backward speed 9.5cm/sec
        self.y_speed = y
        self.direction_speed = direction * 26 # NAO real rotation speed (26deg/sec)
        


