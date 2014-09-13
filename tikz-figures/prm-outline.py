#! /usr/bin/python


"""
Simple demo of PRM in the plane

This is generated using Python code that generates a TeX code (using
PGF/TikZ), which is, in turn, integrated into the main beamer file. Note
that the generated TeX code cannot be used as a stand alone, rather has
to be part of a beamer presentation.
"""

from array import array
import math

class Point:
    """
    A 2D point
    """
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def coord(self):
        return "("+str(self.x)+","+str(self.y)+")"
    def draw(self,overlay,attr,label):
        return "\\fill"+overlay+attr +self.coord() + label  + "circle (3pt);\n"

class Edge:
    def __init__(self,P,Q):
        self.P=P
        self.Q=Q
    def draw(self,overlay):
        return "\\draw" + overlay + "[thick]" + self.P.coord() \
        + " -- " +self.Q.coord() + ";\n"

def ccw(A,B,C):
    return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

# Intersection of segments defined by four points
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

# Squared distance between two points
def sqr_dist(A,B):
    return math.pow(A.x-B.x,2)+math.pow(A.y-B.y,2)

# poly - a list of edges in ccw order forming a CONVEX polygon
def is_free_edge(e,polys):
    """
    Returns trun if the edge e does not intersect
    any of the obstacles in the list polys
    """
    for poly in polys:
        # Check if e intersect any of the polygons
        for curr_pt,next_pt in zip(poly,poly[1:]):
            if intersect(e.P,e.Q,curr_pt,next_pt):
                return False
                # check the last edge
        if intersect(e.P,e.Q,poly[0],poly[len(poly)-1]):
            return False
    return True

def is_inside_polygon(x, y, points):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].

    Reference: http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(points)
    inside = False
    p1x = points[0].x
    p1y = points[0].y
    for i in range(1, n + 1):
        p2x = points[i % n].x
        p2y = points[i % n].y
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def draw_poly(poly,out,attr,overlay):
    out.write("\\draw"+overlay+"["+attr+"]"+ " ")
    for p in poly:
        out.write(p.coord() + " -- ")
    out.write("cycle;\n")

xmax = 20
ymax = 14
n_pts = 150

dist_threshold = 4.5

# Generate grid points
pts = []
for i in range(1, xmax,2):
    for j in range(1,ymax,2):
        pts.append(Point(i,j))

f = open('prm-outline.tex','w')
f.write("\\begin{tikzpicture}[x=15pt,y=15pt]\n")
f.write("\\path [use as bounding box,red] (0,0) rectangle ("+str(xmax)+","+str(ymax)+");\n")

src = Point(0.5,0.5)
trgt = Point(19.5,9.5)

f.write(src.draw("","[green!50!black]"," node[left]{\(s\)}"))
f.write(trgt.draw("","[green!50!black]"," node[right]{\(t\)}"))

# Draw the points
for i in range(0,len(pts)):
    f.write(pts[i].draw("<2>","",""))

obsts = [
    [Point(7.5,3.5),Point(11,3.5),Point(9,6.5)],
    [Point(2.5,10),Point(6,10),Point(6,12),Point(2,12),Point(1.5,11)],
    [Point(13.5,2.5),Point(16.5,2.5),Point(16.5,12),Point(13.5,12)]
    ]

free_pts = []
for i in range(0,len(pts)):
    is_free = True
    for p in obsts:
        if is_inside_polygon(pts[i].x,pts[i].y,p):
            is_free = False
            break
    if is_free:
        free_pts.append(pts[i])
for i in range(0,len(free_pts)):
    f.write(free_pts[i].draw("<3-7>","",""))

for i in range(0,len(obsts)):
    draw_poly(obsts[i],f,"thick,blue,fill=blue!50","<1,3->")
    draw_poly(obsts[i],f,"thick,blue,fill=blue!50,fill opacity=0.5","<2>")

# Draw ALL connectors between neigbohring points
for i in range(0,len(free_pts)-1):
    for j in range (i+1,len(free_pts)):
        if sqr_dist(free_pts[i],free_pts[j]) <= math.pow(dist_threshold,2):
            e = Edge (free_pts[i],free_pts[j])
            f.write(e.draw("<4>"))

# Draw free connectors between neigbohring points
for i in range(0,len(free_pts)-1):
    for j in range (i+1,len(free_pts)):
        if sqr_dist(free_pts[i],free_pts[j]) <= math.pow(dist_threshold,2):
            e = Edge (free_pts[i],free_pts[j])
            if is_free_edge(e,obsts):
                f.write(e.draw("<5-7>"))

f.write("\\draw<6-8>[line width = 4pt,green!50,line cap=round] " + src.coord() + "-- (1,1)" + "(19,9) -- " + trgt.coord() + ";\n")
f.write("\\draw<7-8>[line width = 4pt,green!50] " + src.coord() + " -- (1,1) -- (5,3) -- (7,3) -- (9,7) -- (13,11) -- (13,13) -- (19,13) -- (19,9) -- " + trgt.coord() + ";\n")
# Redraw the source&target so they will be on top of the free path
f.write(src.draw("<6-8>","[green!50!black]"," node[left]{\(s\)}"))
f.write(trgt.draw("<6-8>","[green!50!black]"," node[right]{\(t\)}"))

f.write("\\end{tikzpicture}\n")
f.close()
