import operations as op

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Edge:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def compareToPoint(self, point):
        if op.compareTwoPoints(self.begin, point) or op.compareTwoPoints(self.end, point):
            return True
        else:
            return False

class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def compareToPoint(self, point):
        if point.compare(self.a) or point.compare(self.b) or point.compare(self.c):
            return True
        else:
            return False

class Circle:
    def __init__(self, center, r):
        self.center = center
        self.r = r