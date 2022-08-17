#Program HEAT1D
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
file1 = "heat1d.inp"
f = open(file1, "r")
li=f.read().splitlines()
f.close
title = li[1]
tmp=li[3].split()
ne = int(tmp[0])
nbc = int(tmp[1])
nq = int(tmp[2])
nn = ne + 1
#nbw is bandwidth
nbw = 2
x = np.zeros((nn),dtype = float)
bc = np.zeros((nbc),dtype = str)
tc = np.zeros((ne),dtype = float)
f = np.zeros((nn),dtype = float)
v = np.zeros((nbc),dtype = float)
h = np.zeros((nbc),dtype = float)
nb = np.zeros((nbc),dtype = int)
ptr = 4
#----- element conductivities -----
for i in range(0,ne):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    tc[n-1] = float(tmp[1])
ptr = ptr+1
#----- coordinates -----
for i in range(0,nn):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    x[n-1] = float(tmp[1])
ptr = ptr+1
#----- boundary conditions -----
for i in range(0,nbc):
    ptr = ptr + 1
    tmp=li[ptr].split()
    nb[i] = int(tmp[0])
    c = tmp[1]
    ptr = ptr + 1
    tmp=li[ptr].split()
    if c == "CONV" or c == "conv":
        h[i] = float(tmp[0])
        v[i] = float(tmp[1])
        bc[i] = "c"
    elif c == "TEMP" or c == "temp":
        v[i] = float(tmp[0])
        bc[i] = "t"
    else:
        v[i] = float(tmp[0])
        bc[i] = "f"
ptr = ptr + 1
#----- nodal heat source vector -----
for i in range(0,nq):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    f[n-1] = float(tmp[1])
#--- stiffness matrix ---
s = np.zeros((nn,nbw),dtype = float)
for i in range(0,ne):
    i1 = i
    i2 = i + 1
    ell = abs(x[i2] - x[i1])
    ekl = tc[i] / ell
    s[i1, 0] = s[i1, 0] + ekl
    s[i2, 0] = s[i2, 0] + ekl
    s[i1, 1] = s[i1, 1] - ekl
#--- account for b.c.'s ---
amax = 0
for i in range(0,nn):
    if s[i, 0] > amax:
        amax = s[i, 0]
cnst = amax * 10000
for i in range(0, nbc):
    n = nb[i] - 1
    if bc[i] == "c":
        s[n, 0] = s[n, 0] + h[i]
        f[n] = f[n] + h[i] * v[i]
    elif bc[i] == "f":
        f[n] = f[n] - v[i]
    else:
        s[n, 0] = s[n, 0] + cnst
        f[n] = f[n] + cnst * v[i]
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
print("Results")
print("for data in file",file1)
print("node#   temperature")
for i in range(0,nn):
    print('{:5d} {:12.4e}'.format(i+1,f[i]))