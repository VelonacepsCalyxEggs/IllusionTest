import math

class Vector2D():
    '''
    this is a class for 2D vectors with x and y components and some basic operations
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        '''
        adds the other vector to the current vector
        '''
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        '''
        subtracts the other vector from the current vector
        '''
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, param):
        '''
        if the parameter is a vector, it returns the dot product
        
        if the parameter is a scalar, it returns the scaled vector
        '''
        if isinstance(param, Vector2D):
            return self.x * param.y - self.y * param.x 
        return Vector2D(self.x * param, self.y * param)
    

    def __str__(self):
        '''
        returns a string representation of the vector
        '''
        return f"({self.x}, {self.y})"
    
    def rotate(self, angle):
        '''
        rotates the vector by the given angle
        '''
        angle = math.radians(angle)
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        return Vector2D(x, y)

class Line():
    '''
    this is a custom class for 2D lines with origin, direction and length
    '''
    def __init__(self, org: Vector2D, dir: Vector2D, len: float):
        '''
        org: origin of the line
        dir: direction of the line
        len: length of the line
        '''
        self.org = org
        self.dir = dir
        self.len = len
        
        self.calculate_second()

    def calculate_second(self):
        '''
        should be called after changing the dir or len of the line
        '''
        self.secn = self.dir * self.len + self.org
    
    def rotate(self, angle):
        '''
        rotates the line by the given angle
        '''
        self.dir = self.dir.rotate(angle)
        self.calculate_second()

    def swap_origin(self):
        '''
        swaps the origin and the second point of the line
        '''
        self.org, self.secn = self.secn, self.org
        self.dir = self.dir * -1

    def __str__(self):
        '''
        returns a string representation of the line
        '''
        return f"({self.org}, {self.secn}, {self.dir}, {self.len})"
    