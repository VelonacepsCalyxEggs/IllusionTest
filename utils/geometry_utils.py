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
    
    def magnitude(self):
        '''
        returns the magnitude of the vector
        '''
        return math.sqrt(self.x ** 2 + self.y ** 2)

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

    def rotate_around_point(self, angle, point: Vector2D):
        '''
        rotates the line around a given point by the given angle
        '''
        self.org = self.org - point
        self.secn = self.secn - point
        self.org = self.org.rotate(angle)
        self.secn = self.secn.rotate(angle)
        self.org = self.org + point
        self.secn = self.secn + point
        self.dir = self.secn - self.org

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
    
    def calculate_intersection(self, line1, line2):
        '''
        calculates the intersection point of two lines
        '''
        a1 = line1.secn.y - line1.org.y
        b1 = line1.org.x - line1.secn.x
        c1 = a1 * line1.org.x + b1 * line1.org.y

        a2 = line2.secn.y - line2.org.y
        b2 = line2.org.x - line2.secn.x
        c2 = a2 * line2.org.x + b2 * line2.org.y

        det = a1 * b2 - a2 * b1

        if det == 0:
            return False
        else:
            x = (b2 * c1 - b1 * c2) / det
            y = (a1 * c2 - a2 * c1) / det
            return Vector2D(x, y)
    