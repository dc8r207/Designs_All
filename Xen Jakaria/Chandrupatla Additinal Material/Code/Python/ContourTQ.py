#Program CONTOURTQ for color contours in Triangles and Quadrilaterals
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import turtle
turtle.screensize(800,600)
ttl = turtle.Turtle()
ttl.pensize(2)
style = ('Courier', 10, 'italic','bold')
colors = ["Violet","Indigo","Blue","LightSeaGreen","Green","GreenYellow","Yellow","Orange","OrangeRed","Red"]
file1 = "contourt.inp"
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
x = np.zeros((nen,ndim), dtype = float)
stress = np.zeros((nn), dtype = float)
st = np.zeros((3), dtype = float)
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
    tmp = li[ptr].split()
    n = int(tmp[0])
    for j in range(0,nen):
        noc[n-1,j] = int(tmp[1+j])
#Read nodal values of stresses
ptr = ptr + 1
for i in range(0, nn):
    ptr = ptr + 1
    tmp = li[ptr].split()
    stress[i] = float(tmp[0])
    if i == 0:
      smin = stress[i]
      smax = stress[i]
    else:
      if smin > stress[i]:
          smin = stress[i]
      if smax < stress[i]:
          smax = stress[i]
delta =(smax - smin)/10

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

def plotmesh(noc,xp,stress,ne,nen,smin,delta):
    xt = np.zeros((3), dtype = int)
    yt = np.zeros((3), dtype = int)
    st = np.zeros((3), dtype = float)
    for i in range(0, ne):
        if nen < 4:
            # Triangle element
            i1 = noc[i][0]-1
            i2 = noc[i][1]-1
            i3 = noc[i][2]-1 
            xt[0] = xp[i1][0]
            xt[1] = xp[i2][0]
            xt[2] = xp[i3][0]
            yt[0] = xp[i1][1]
            yt[1] = xp[i2][1]
            yt[2] = xp[i3][1]
            st[0] = stress[i1]
            st[1] = stress[i2]
            st[2] = stress[i3]        
            tplot(st,xt,yt,smin,delta)
        else:
            #Quadrilateral
            i1 = noc[i][0]-1
            xc = xp[i1][0]
            yc = xp[i1][1]
            sc = stress[i1]/4
            for j in range(1, nen):
                i1 = noc[i][j]-1
                xc = xc + xp[i1][0]
                yc = yc + xp[i1][1]       
                sc = sc + stress[i1]/4
            xc = xc//4
            yc = yc//4
            for j in range(0, nen):
                jj = j + 1
                if jj > 3:
                    jj = 0
                i1 = noc[i][j]-1
                i2 = noc[i][jj]-1 
                xt[0] = xc
                yt[0] = yc
                st[0] = sc        
                xt[1] = xp[i1][0]
                yt[1] = xp[i1][1]        
                xt[2] = xp[i2][0]
                yt[2] = xp[i2][1]        
                st[1] = stress[i1]
                st[2] = stress[i2]
                tplot(st,xt,yt,smin,delta)
def tplot(st,xt,yt,smin,delta):
    #Contour plot
    #Three nodes in ascending order of stresses
    nod = np.zeros((3), dtype = int)
    nod[0] = 0
    nod[1] = 1
    nod[2] = 2
    for k in range(0,2):
        for kk in range(k + 1, 3):
            if st[nod[k]] > st[nod[kk]]:
                i1 = nod[k]
                nod[k] = nod[kk]
                nod[kk] = i1
    eps = 0.01 * delta
    x1 = xt[nod[0]]
    y1 = yt[nod[0]]
    s1 = st[nod[0]]
    x2 = xt[nod[1]]
    y2 = yt[nod[1]]
    s2 = st[nod[1]]
    x3 = xt[nod[2]]
    y3 = yt[nod[2]]
    s3 = st[nod[2]]
    ic = int((s2 - smin)//delta)
    # If stresses are almost equal one color for triangle
    if abs(s3 - s1) < eps:
        triangle(x1,y1,x2,y2,x3,y3,ic)
    else:
        #Line x2,y2 and xm,ym divides triangle into two triangles
        xi = (s2 - s1)/(s3 - s1)
        xm = x1 + int(xi*(x3 - x1))
        ym = y1 +int(xi*(y3 - y1))
        #Colors in lower triangle
        if abs(s2 - s1) > eps:
            ic = int((s2 - smin)/delta - 0.01)
            x4 = x2
            y4 = y2
            x5 = xm
            y5 = ym
            ifl = 0
            while ifl == 0:
                triangle(x4,y4,x5,y5,x1,y1,ic)
                s = smin + ic * delta
                ic = ic - 1
                if s > s1:
                    xi = (s - s1)/(s2 - s1)
                    x4 = x1 + int(xi*(x2 - x1))
                    y4 = y1 + int(xi*(y2 - y1))
                    x5 = x1 + int(xi*(xm - x1))
                    y5 = y1 +int( xi*(ym - y1))
                else:
                    ifl = 1
        # Colors in upper triangle
        if abs(s3 - s2) > eps:
            ic = int((s2 - smin)/delta + 0.01)
            x4 = x2
            y4 = y2
            x5 = xm
            y5 = ym
            ifl = 0
            while ifl == 0:
                triangle(x4,y4,x5,y5,x3,y3,ic)
                ic = ic + 1
                s = smin + ic * delta
                if s < s3:
                    xi = (s3 - s)/(s3 - s2)
                    x4 = x3 + int(xi*(x2 - x3))
                    y4 = y3 + int(xi*(y2 - y3))
                    x5 = x3 + int(xi*(xm - x3))
                    y5 = y3 + int(xi*(ym - y3))
                else:
                    ifl = 1
def triangle(xa,ya,xb,yb,xc,yc,ic):
    ttl.fillcolor(colors[ic])
    ttl.pencolor(colors[ic])
    ttl.begin_fill()
    ttl.penup()
    ttl.goto(xa,ya)
    ttl.pendown()
    ttl.goto(xb,yb)
    ttl.goto(xc,yc)
    ttl.goto(xa,ya)
    ttl.end_fill()
    ttl.penup()
def legend():
    s = smin - delta/2
    for i in range(0,10):
        a = 40*i
        s = s + delta
        ttl.penup()
        ttl.fillcolor(colors[i])
        ttl.pencolor(colors[i])
        ttl.begin_fill()
        ttl.goto(a,290)
        ttl.pendown()
        ttl.goto(a+40,290)
        ttl.goto(a+40,300)
        ttl.goto(a,300)
        ttl.goto(a,290)
        ttl.end_fill()
        ttl.penup()
        ttl. goto(a,260)
        ttl.pendown()
        ttl.write(str(round(s)),False, font=("Times New Roman", 12, "bold"))
        
plotmesh(noc,xp,stress,ne,nen,smin,delta)
legend()
ttl.hideturtle()
turtle.done()
turtle.bye()