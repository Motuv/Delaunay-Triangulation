import random as rd
import structures as st
import math


def calcDistance(p1, p2):
    return math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))


def generateRandomPoints(n):
    points = []
    for i in range(n):
        x = rd.randint(0, 1000)
        y = rd.randint(0, 1000)
        p = st.Point(x, y)
        points.append(p)
    return points


def generateSuperTetragon(pts):
    left, right, top, bottom = None, None, None, None
    tetragon = []
    for i in pts:
        if left is None or i.x < left.x:
            left = i
        if right is None or i.x > right.x:
            right = i
        if bottom is None or i.y < bottom.y:
            bottom = i
        if top is None or i.y > top.y:
            top = i
    tetragon.append(st.Point(left.x - 5, top.y + 5))
    tetragon.append(st.Point(right.x + 5, top.y + 5))
    tetragon.append(st.Point(left.x - 5, bottom.y - 5))
    tetragon.append(st.Point(right.x + 5, bottom.y - 5))
    return tetragon


def generateSuperTriangle(tetragon):
    mid = (tetragon[1].x + tetragon[0].x) / 2
    high = (tetragon[0].y + 100*(tetragon[0].y - tetragon[2].y))
    left = tetragon[0].x - 100 * (tetragon[1].x - tetragon[0].x)
    right = tetragon[1].x + 100 * (tetragon[1].x - tetragon[0].x)
    p1 = st.Point(mid, high)
    p2 = st.Point(left, tetragon[2].y - 10)
    p3 = st.Point(right, tetragon[2].y - 10)
    triangle = st.Triangle(p1, p2, p3)
    return triangle


def findExcircle(triangle):
    a = triangle.a
    b = triangle.b
    c = triangle.c
    if ((a.x*b.y)+(b.x*c.y)+(c.x*a.y))-((c.x*b.y)+(b.x*a.y)+(a.x*c.y)) == 0:
        return None

    x0 = 0.5 * ((((b.x * b.x * c.y) + (b.y * b.y * c.y) - (a.x * a.x * c.y) - (a.y * a.y * c.y)) / (
                (a.y * c.x) - (a.y * b.x) + (b.y * a.x) - (b.y * c.x) + (c.y * b.x) - c.y * a.x)) + (
                            ((a.x * a.x * b.y) + (a.y * a.y * b.y) - (c.x * c.x * b.y) - (c.y * c.y * b.y)) / (
                                (a.y * c.x) - (a.y * b.x) + (b.y * a.x) - (b.y * c.x) + (c.y * b.x) - (c.y * a.x))) + (
                            ((c.x * c.x * a.y) + (c.y * c.y * a.y) - (b.x * b.x * a.y) - (b.y * b.y * a.y)) / (
                                (a.y * c.x) - (a.y * b.x) + (b.y * a.x) - (b.y * c.x) + (c.y * b.x) - (c.y * a.x))))
    y0 = 0.5 * ((((a.x * a.x * c.x) + (a.y * a.y * c.x) - (b.x * b.x * c.x) - (b.y * b.y * c.x)) / (
            (a.y * c.x) - (a.y * b.x) + (b.y * a.x) - (b.y * c.x) + (c.y * b.x) - c.y * a.x)) + (
                        ((c.x * c.x * b.x) + (c.y * c.y * b.x) - (a.x * a.x * b.x) - (a.y * a.y * b.x)) / (
                        (a.y * c.x) - (a.y * b.x) + (b.y * a.x) - (b.y * c.x) + (c.y * b.x) - (c.y * a.x))) + (
                        ((b.x * b.x * a.x) + (b.y * b.y * a.x) - (c.x * c.x * a.x) - (c.y * c.y * a.x)) / (
                        (a.y * c.x) - (a.y * b.x) + (b.y * a.x) - (b.y * c.x) + (c.y * b.x) - (c.y * a.x))))

    center = st.Point(x0, y0)
    r = calcDistance(a, center)
    excircle = st.Circle(center, r)
    return excircle


def countDistance(p1, p2):
    return math.sqrt((math.pow((p2.x - p1.x), 2) + math.pow((p2.y - p1.y), 2)))


def ifPointInCircle(point, circle):
    dist = countDistance(point, circle.center)
    if dist <= circle.r:
        return True
    else:
        return False


def isTwoEdgesEqual(e1, e2):
    if (e1.begin == e2.begin and e1.end == e2.end) or (e1.begin == e2.end and e1.end == e2.begin):
        return True
    else:
        return False


def compareTwoPoints(p1, p2):
    if p1.x == p2.x and p1.y == p2.y:
        return True
    else:
        return False

'''def ifTriangleHaveCommonEdge(t1, t2):
    result = 0
    if compareTwoPoints(t1.a,t2.a) or compareTwoPoints(t1.a,t2.b) or compareTwoPoints(t1.a,t2.c):
        result += 1
    if compareTwoPoints(t1.b, t2.a) or compareTwoPoints(t1.b, t2.b) or compareTwoPoints(t1.b, t2.c):
        result += 1
    if compareTwoPoints(t1.c,t2.a) or compareTwoPoints(t1.c,t2.b) or compareTwoPoints(t1.c,t2.c):
        result += 1
    if result == 2:
        return True
    else:
        return False

def connectAll(points):
    edges = []
    for p1 in points:
        for p2 in points:
            if p1 != p2:
                edges.append(st.Edge(p1,p2))
    return edges

def doesIntersect(e1, e2):
    a1 = round((e1.begin.y - e1.end.y) / (e1.begin.x - e1.end.x), 2)
    b1 = round((e1.begin.y - a1 * e1.begin.x), 2)
    a2 = round((e2.begin.y - e2.end.y) / (e2.begin.x - e2.end.x), 2)
    b2 = round((e2.begin.y - a2 * e2.begin.x), 2)
    if a1 != a2:
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1
        p = st.Point(x,y)
        if doesPointBelongToSegment(p, e1):
            return True
        else:
            return False
    else:
        return False

def doesPointBelongToSegment(p,e):
    if e.begin.x > e.end.x:
        xu = e.begin.x
        xl = e.end.x
    else:
        xu = e.end.x
        xl = e.begin.x
    if e.begin.y > e.end.y:
        yu = e.begin.y
        yl = e.end.y
    else:
        yu = e.end.y
        yl = e.begin.y
    if xl <= p.x <= xu and yl <= p.y <= yu:
        return True
    else:
        return False

def findPerpendicular(e1):
    midx = math.fabs(e1.begin.x - e1.end.x)/2
    midy = math.fabs(e1.begin.y - e1.end.y)/2
    a1 = round((e1.begin.y - e1.end.y) / (e1.begin.x - e1.end.x), 2)
    b1 = round((e1.begin.y - a1 * e1.begin.x), 2)
    a = -(1/a1)
    b = round((midy - a*midx), 2)
    edge = st.Edge(st.Point(midx-20,a*(midx-20)+b), st.Point(midx+20, a*(midx+20)+b))
    return edge'''