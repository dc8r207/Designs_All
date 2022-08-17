#Program PLOT2D for plotting 2D Meshes
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import turtle
turtle.screensize(800,600)
ttl = turtle.Turtle()
ttl.pensize(2)
style = ('Courier', 10, 'italic','bold')
file1 = "plot2.inp"
f = open(file1, "r")
li=f.read().splitlines()
f.close
results = "file for input to contour\n"
tmp=li[3].split()
nn = int(tmp[0])
ne = int(tmp[1])
tmp=li[5].split()
ndim = int(tmp[0])
nen = int(tmp[1])
ndn = int(tmp[2])
#Allocate arrays
xn = np.zeros((nn,ndim), dtype = float)
noc = np.zeros((ne,nen),dtype = int)
xp = np.zeros((nn,ndim), dtype = int)
x = np.zeros((nen,ndim), dtype = int)
ptr = 6
#----- coordinates -----
for i in range(0,nn):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    for j in range(0,ndim):
        xn[n-1,j] = float(tmp[1+j])
ptr = ptr+1
#----- connectivity -----
for i in range(0,ne):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    for j in range(0,nen):
        noc[n-1,j] = int(tmp[1+j])
for i in range(1,ptr+1):
    results = results + li[i] +"\n"
#xp are scaled coordinates for plotting
def scaled(x,nn,a,b):
    xmin=x[0][0]
    xmax=x[0][0]
    ymin=x[0][1]
    ymax=x[0][1]

    for i in range(1, nn):
        if xmin > x[i][0]:
            xmin = x[i][0]
        if xmax < x[i][0]:
            xmax = x[i][0]
        if ymin > x[i][1]:
            ymin = x[i][1]
        if ymax < x[i][1]:
            ymax = x[i][1]
    scale = 0.9*a/(xmax-xmin);
    if scale > 0.9*b/(ymax-ymin):
        scale = 0.9*b/(ymax-ymin)    
    #Scaled coordinates
    #Scaled coordinates
    for i in range(0,nn):
        xp[i][0]=0.05*a+scale*(x[i][0]-xmin) - 0.5*a
        xp[i][1]=0.05*b+scale*(x[i][1]-ymin) - 0.5*b
    return xp
xp = scaled(xn,nn,800,600)
def element(x,nen,n):
    ttl.penup()
    ttl.goto(x[0][0],x[0][1])
    ttl.pendown()
    xc = x[0][0]
    yc = x[0][1]
    for i in range(0,nen):
        i1 = i + 1
        if i1 < nen:
            xc = xc + x[i+1][0]
            yc = yc + x[i+1][1]
        else:
            i1 = 0
        ttl.goto(x[i1][0],x[i1][1])
    ttl.penup()
    xc = xc//nen
    yc = yc//nen
    ttl.goto(xc,yc)
    ttl.write(str(n+1), font=style, align='center')
for n in range(0,ne):
    for j in range(0,nen):
        jj = noc[n][j]-1
        x[j][0]=xp[jj][0]
        x[j][1]=xp[jj][1]
    element(x,nen,n)
def nodenum(x,n):
    ttl.color('red')
    style = ('Courier', 10, 'italic','bold')
    for i in range(0,n):
        ttl.penup()
        ttl.goto(x[i][0],x[i][1])
        ttl.pendown()
        p = str(i+1)
        ttl.write(p, font=style, align='center')
    ttl.penup()
nodenum(xp,nn)
ttl.hideturtle()
turtle.done()
turtle.bye()