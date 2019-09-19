class Shape():
    def __init__(self):
        pass
    def getArea(self):
        pass

class Rectangle(Shape):
    def __init__ (self, length, width):
        self.l = length
        self.w = width
    def getArea(self):
        return self.l * self.w
class Triangle(Shape):
    def __init__(self, base, height):
        self.b = base
        self.h = height
    def getArea(self):
        return (0.5 * self.b * self.h)
class Circle(Shape):
    def __init__(self, radius):
        self.r = radius
    def getArea(self):
        return (3.14 * (self.r * self.r))

file = open(r'P:\\GEOG 392\GEOG_392_Lab\Lab3\shapes.txt', 'r')
lines = file.readlines()
file.close()

idx_rec = 1
idx_circle = 1
idx_tri = 1
for line in lines:
    components = line.split(",")
    Shape = components[0]
    
    if Shape == "Rectangle":
        x = int(components[1])
        y = int(components[2])
        rect1 = Rectangle(x,y)
        area1 = rect1.getArea()
        print('Rectangle', idx_rec, ': Area:', area1)
        idx_rec = idx_rec + 1    
    elif Shape == "Circle":
        x = int(components[1])
        circle1 = Circle(x)
        area2 = circle1.getArea()
        print('Circle', idx_circle, ': Area:', area2)
        idx_circle = idx_circle + 1
    
    elif Shape == "Triangle":
        x = int(components[1])
        y = int(components[2])
        tri1 = Triangle(x,y)
        area3 = tri1.getArea()
        print('Triangle', idx_tri, ': Area:', area3)
        idx_tri = idx_tri + 1
    else:
        pass
