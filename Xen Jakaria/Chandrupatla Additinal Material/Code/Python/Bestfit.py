#Program BESTFIT for constant strain triangle element
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
file1 = "bestfit.inp"
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
x = np.zeros((nn,ndim), dtype = float)
noc = np.zeros((ne,nen),dtype = int)
fs = np.zeros((ne), dtype = float)
se = np.zeros((3,3), dtype = float)
fe = np.zeros((3), dtype = float)
f = np.zeros((nn), dtype = float)
ptr = 6
#----- coordinates -----
for i in range(0,nn):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    for j in range(0,ndim):
        x[n-1,j] = float(tmp[1+j])
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
# ---  Read Element Values --- 
ptr = ptr + 1
for i in range(0,ne):
   ptr = ptr + 1
   fs[i] = float(li[ptr])
# InputData finished
# ----- Bandwidth Evaluation ----- 
nbw = 0
for i in range(0, ne):
    nmin = noc[i][0]
    nmax = noc[i][0]
    for j in range(1,nen):
        if nmin > noc[i][j]:
            nmin = noc[i][j]
        if nmax < noc[i][j]:
            nmax = noc[i][j]
        ntmp = nmax - nmin + 1
        if nbw < ntmp:
            nbw = ntmp
s = np.zeros((nn,nbw), dtype = float)
def elstiff(n, x, noc,fe):
# --- Element Stiffness Formation
    i1 = noc[n][0] - 1
    i2 = noc[n][1] - 1
    i3 = noc[n][2] - 1
    x1 = x[i1][0]
    y1 = x[i1][1]
    x2 = x[i2][0]
    y2 = x[i2][1]
    x3 = x[i3][0]
    y3 = x[i3][1]
    x32 = x3 - x2
    x13 = x1 - x3
    y23 = y2 - y3
    y31 = y3 - y1
    dj = x13 * y23 - x32 * y31      #determinant of jacobian
    ae = abs(dj) / 24
    se[0][0] = 2 * ae
    se[0][1] = ae
    se[0][2] = ae
    se[1][0] = ae
    se[1][1] = 2 * ae
    se[1][2] = ae
    se[2][0] = ae
    se[2][1] = ae
    se[2][2] = 2 * ae
    a1 = fs[n] * abs(dj) / 6
    fe[0] = a1
    fe[1] = a1
    fe[2] = a1
    return se
# end element stiffness
#---Stiffness()
    # ---  Global Stiffness Matrix
for n in range(0, ne):
    se = elstiff(n, x, noc,fe)
    for ii in range(0, 3):
        nr = noc[n][ii] - 1
        f[nr] = f[nr] + fe[ii]
        for jj in range(0, 3):
            nc = noc[n][jj] - nr
            if nc > 0:
                s[nr][nc-1] = s[nr][nc-1] + se[ii][jj]
#Function bandsolver
def bansol(a,b,nb):
    n = len(b)
  # Forward Elimination
    for k in range(0,n-1):
        nk = k+nb
        if nk > n:
            nk = n
        for i in range(k+1,nk):
            c = a[k,i-k]/a[k,0]
            b[i] = b[i] - c*b[k]
            for j in range(0,nk-i):
             jk = i-k+j
             a[i,j] = a[i,j] - c*a[k,jk]
#Backsubstitution
    b[n-1]=b[n-1]/a[n-1,0]
    for i in range(n-2,-1,-1):
       ni = n-i
       if ni>nb:
            ni=nb
       c = 0
       for j in range(1,ni):
           c=c+a[i,j]*b[i+j]         
       b[i]=(b[i]-c)/a[i,0] 
    
    return b
f = bansol(s,f,nbw)
results = results + "Nodal Values\n"
for i in range(0,nn):
    results = results + str(round(10000*f[i])/10000) +"\n"
print(results)



