import operations as op
import structures as st
import pointGenerator as pg
from matplotlib import pyplot as plt
import cv2

def divide(triangles, point):
    #generator kluczy
    miliard, milion, tysiac = 1000000000, 1000000, 1000

    tmptriangles = []
    #słownik krawedzi (nie moga sie powtarzac)
    edge_buffer = {}
    for t in triangles:
        c = op.findExcircle(t)
        if c == None:
            continue
        if op.ifPointInCircle(point, c):
            if t.a.x <= t.b.x:
                tmpkey = miliard*t.a.x+milion*t.a.y+tysiac*t.b.x+t.b.y
                if edge_buffer.get(tmpkey) is not None:
                    edge_buffer.pop(tmpkey)
                else:
                    edge_buffer[tmpkey] = st.Edge(t.a, t.b)
            else:
                tmpkey = miliard*t.b.x +milion* t.b.y +tysiac* t.a.x + t.a.y
                if edge_buffer.get(tmpkey) is not None:
                    edge_buffer.pop(tmpkey)
                else:
                    edge_buffer[tmpkey] = st.Edge(t.b, t.a)
            if t.b.x <= t.c.x:
                tmpkey = miliard*t.b.x +milion* t.b.y +tysiac* t.c.x + t.c.y
                if edge_buffer.get(tmpkey) is not None:
                    edge_buffer.pop(tmpkey)
                else:
                    edge_buffer[tmpkey] = st.Edge(t.b, t.c)
            else:
                tmpkey = miliard*t.c.x +milion* t.c.y + tysiac*t.b.x + t.b.y
                if edge_buffer.get(tmpkey) is not None:
                    edge_buffer.pop(tmpkey)
                else:
                    edge_buffer[tmpkey] = st.Edge(t.c, t.b)
            if t.c.x <= t.a.x:
                tmpkey = miliard*t.c.x +milion* t.c.y + tysiac*t.a.x + t.a.y
                if edge_buffer.get(tmpkey) is not None:
                    edge_buffer.pop(tmpkey)
                else:
                    edge_buffer[tmpkey] = st.Edge(t.c, t.a)
            else:
                tmpkey = miliard*t.a.x +milion* t.a.y + tysiac*t.c.x + t.c.y
                if edge_buffer.get(tmpkey) is not None:
                    edge_buffer.pop(tmpkey)
                else:
                    edge_buffer[tmpkey] = st.Edge(t.a, t.c)
        else:
            tmptriangles.append(t)

    for key in edge_buffer:
        tmptriangles.append(st.Triangle(edge_buffer[key].begin, edge_buffer[key].end, point))

    return tmptriangles

def delaunay():
    #generowanie punktów
    points, pointsToSave = pg.generatePoints()

    #superprostokąt
    tetragon = op.generateSuperTetragon(points)

    #supertrójkąt
    supertriangle = op.generateSuperTriangle(tetragon)
    triangle_list = [supertriangle]

    #proces tworzenia siatki
    for p in points:
        triangle_list = divide(triangle_list, p)

    # usuwanie supertrójkąta
    todelete = []
    for i in range(len(triangle_list)):
        if op.compareTwoPoints(triangle_list[i].a, supertriangle.a) or op.compareTwoPoints(triangle_list[i].a,supertriangle.b) or op.compareTwoPoints(triangle_list[i].a, supertriangle.c) or op.compareTwoPoints(triangle_list[i].b, supertriangle.a) or op.compareTwoPoints(triangle_list[i].b,supertriangle.b) or op.compareTwoPoints(triangle_list[i].b, supertriangle.c) or op.compareTwoPoints(triangle_list[i].c, supertriangle.a) or op.compareTwoPoints(triangle_list[i].c,supertriangle.b) or op.compareTwoPoints(triangle_list[i].c, supertriangle.c):
            todelete.append(i)
    todelete = list(dict.fromkeys(todelete))
    todelete.sort(reverse=True)
    for i in todelete:
        triangle_list.remove(triangle_list[i])


    #rysowanie
    image = cv2.imread('singleSlice.png')
    file = open('mesh.geo','w')
    for p in pointsToSave:
        cv2.circle(image, (pointsToSave[p].x, pointsToSave[p].y), radius=0, color=(0, 0, 0), thickness=1)
        file.write("//+\n")
        file.write("Point(%d) = {%d,%d,0,0.5};\n"%(p,pointsToSave[p].x,pointsToSave[p].y))

    #zapis do pliku .geo
    i = 1
    for t in triangle_list:
        cv2.line(image, (t.a.x,t.a.y), (t.b.x,t.b.y), (0,0,0), thickness=1)
        file.write("//+\n")
        file.write("Line(%d) = {%d,%d};\n" % (i, (t.a.x*1000+t.a.y), (t.b.x*1000+t.b.y)))
        i+=1
        cv2.line(image, (t.b.x,t.b.y), (t.c.x,t.c.y), (0,0,0), thickness=1)
        file.write("//+\n")
        file.write("Line(%d) = {%d,%d};\n" % (i, (t.b.x * 1000 + t.b.y), (t.c.x * 1000 + t.c.y)))
        i+=1
        cv2.line(image, (t.c.x,t.c.y), (t.a.x,t.a.y), (0,0,0), thickness=1)
        file.write("//+\n")
        file.write("Line(%d) = {%d,%d};\n" % (i, (t.c.x * 1000 + t.c.y), (t.a.x * 1000 + t.a.y)))
        i+=1
    file.write("//+\n")
    curve_loop = "Curve Loop(1) = {"
    for j in range(1,i):
        curve_loop += str(j)
        curve_loop += ','
    curve_loop = curve_loop.rstrip(',')
    curve_loop += "};\n"
    file.write(curve_loop)
    file.write("//+\n")
    file.write("Plane Surface(1) = {1};\n")
    file.close()
    #koniec zapisu do pliku mesh.geo

    #zapis do png, wyswietlenie wyniku
    cv2.imshow('image', image)
    cv2.imwrite('microstructure_mesh.png', image)
    cv2.waitKey(0)

#wywołanie programu
delaunay()