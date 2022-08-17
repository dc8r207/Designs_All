#Program BESTFIT for constant strain triangle element
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
file1 = "bestfitq.inp"
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
v = np.zeros((ne,4), dtype = float)
se = np.zeros((4,4), dtype = float)
fe = np.zeros((4), dtype = float)
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
print(li[ptr])
for i in range(0,ne):
   ptr = ptr + 1
   tmp=li[ptr].split()
   n = int(tmp[0])-1
   for j in range(0, 4):
       v[n,j] = float(tmp[1+j])
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
def elemstiff(fe) :
#--- element stiffness formation
    al = 0.5773502692
#----- shape function values
    sh = np.zeros((4,4), dtype = float)
    sh[0][0] = 0.25 * (1 + al) * (1 + al)
    sh[0][1] = 0.25 * (1 - al * al)
    sh[0][2] = 0.25 * (1 - al) * (1 - al)
    sh[0][3] = sh[0][1]
    sh[1][0] = sh[0][1]
    sh[1][1] = sh[0][0]
    sh[1][2] = sh[0][1]
    sh[1][3] = sh[0][2]
    sh[2][0] = sh[0][2]
    sh[2][1] = sh[0][1]
    sh[2][2] = sh[0][0]
    sh[2][3] = sh[0][1]
    sh[3][0] = sh[0][1]
    sh[3][1] = sh[0][2]
    sh[3][2] = sh[0][1]
    sh[3][3] = sh[0][0]
#----- element stiffness se and load fe
    for i in range(0,4):
        c1 = 0
        for j in range(0, 4):
            c = 0
            c1 = c1 + sh[i][j] * v[n][j]
            for k in range(0, 4):
                c = c + sh[i][k] * sh[k][j]
            se[i][j] = c
        fe[i] = c1
    return se
# end of ElemStiff
# ---  Global Stiffness Matrix and Loads
for n in range(0, ne):
    se = elemstiff(fe)
    #..... Placing in Banded Locations
    for ii in range(0,4):
        nr = noc[n][ii] - 1
        for jj in range(0, 4):
            nc = noc[n][jj] - nr
            if nc > 0:
                s[nr][nc-1] = s[nr][nc-1] + se[ii][jj]
        f[nr] = f[nr] + fe[ii]    
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



