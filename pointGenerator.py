import math
import cv2
import structures as st
import random

def generatePoints():
    image = cv2.imread('singleSlice.png')
    height, width, channels = image.shape
    points = {}
    d = 25
    file = open('mesh_file.txt', 'w')
    #brzegi
    for i in range(0,height,20):
        key = i
        points[key] = st.Point(0,i)
        key = width*1000+i
        points[key] = st.Point(width, i)
    for i in range(0, width, 20):
        key = 1000*i
        points[key] = st.Point(i,0)
        key = 1000*i+height
        points[key] = st.Point(i, height)
    #podstawa siatki
    for i in range(d,height-d,d):
        for j in range(d,width-d,d):
            r = image[i][j][0]
            g = image[i][j][1]
            b = image[i][j][2]
            if (image[i-d][j][0]==r and image[i-d][j][1]==g and image[i-d][j][2]==b):
                if (image[i + d][j][0] == r and image[i + d][j][1] == g and image[i + d][j][2] == b):
                    if (image[i][j-d][0] == r and image[i][j-d][1] == g and image[i][j-d][2] == b):
                        if (image[i][j + d][0] == r and image[i][j + d][1] == g and image[i][j + d][2] == b):
                            continue
            key = j*1000+i
            p = st.Point(j, i)
            points[key] = p
            line = "%.f; %.f; 0.0;%d;%d;%d\n" % (p.x, p.y, r, g, b)
            file.write(line)

    #zagęszczenie po brzegach ziaren
    d=7
    for i in range(d,height-d,d):
        for j in range(d,width-d,d):
            r = image[i][j][0]
            g = image[i][j][1]
            b = image[i][j][2]
            if (image[i-d][j][0]==r and image[i-d][j][1]==g and image[i-d][j][2]==b):
                if (image[i + d][j][0] == r and image[i + d][j][1] == g and image[i + d][j][2] == b):
                    if (image[i][j-d][0] == r and image[i][j-d][1] == g and image[i][j-d][2] == b):
                        if (image[i][j + d][0] == r and image[i][j + d][1] == g and image[i][j + d][2] == b):
                            continue
            key = j*1000+i
            p = st.Point(j, i)
            points[key] = p
            #points.append(p)
            line = "%.f; %.f; 0.0;%d;%d;%d\n" % (p.x, p.y, r, g, b)
            file.write(line)

    file.close()
    points_final = []
    for p in points:
        points_final.append(points[p])
    #zwraca listę punktów i słownik punktów, który jest potrzebny przy eksporcie do geo
    return points_final, points
