#Program HEAT2D
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "heat2d.inp"
f = open(file1, "r")
li=f.read().splitlines()
f.close
title = li[1]
tmp=li[3].split()
nn = int(tmp[0])
ne = int(tmp[1])
nm = int(tmp[2])
nd = int(tmp[3])
nl = int(tmp[4])
nmpc = int(tmp[5])
tmp=li[5].split()
ndim = int(tmp[0])
nen = int(tmp[1])
ndn = int(tmp[2])
#note!!  npr =1 (thermal conductivity) and nmpc = 0 for this program
npr = 1
nmpc = 0
#--- nd = no. of specified temperatures
#--- nl = no. of nodal heat sources
#--- ehs(i) = element heat source, i = 1,...,ne
x = np.zeros((nn,2),dtype = float)
noc = np.zeros((ne, 3),dtype = int)
mat = np.zeros((ne),dtype = int)
pm = np.zeros((nm,npr),dtype = float)
f = np.zeros((nn),dtype = float)
nu = np.zeros((nd),dtype = int)
u = np.zeros((nd),dtype = float)
ehs = np.zeros((ne),dtype = float)
q = np.zeros((ne,2),dtype = float)
ptr = 6
#----- coordinates -----
for i in range(0,nn):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    x[n-1, 0] = float(tmp[1])
    x[n-1, 1] = float(tmp[2])
ptr = ptr + 1
#----- connectivity -----
for i in range(0,ne):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    for j in range(0,nen):
        noc[n-1,j] = int(tmp[1+j])
    mat[n-1] = int(tmp[nen+1]) 
    ehs[n-1] = float(tmp[nen+2])
ptr = ptr + 1
#----- temperature BC -----
for i in range(0,nd):
    ptr = ptr + 1
    tmp=li[ptr].split()
    nu[i] = int(tmp[0])
    u[i] = float(tmp[1])
ptr = ptr + 1
#----- nodal heat source vector -----
for i in range(0,nl):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    f[n-1] = float(tmp[1])
ptr = ptr + 1
#----- material properties -----
for i in range(0,nm):
    ptr = ptr + 1
    tmp=li[ptr].split()
    n = int(tmp[0])
    for j in range(0,npr):
        pm[n-1,j]=float(tmp[1+j])
ptr = ptr + 2
nhf = int(li[ptr])
if nhf > 0:
    ptr = ptr + 1
    nflux = np.zeros((nhf,2), dtype = int)
    flux = np.zeros((nhf), dtype = float)
    for i in range(0,nhf):
        ptr = ptr + 1
        tmp = li[ptr].split()
        nflux[i, 0] =int(tmp[0])
        nflux[i, 1] =int(tmp[1])
        flux[i] = float(tmp[2])
ptr = ptr + 2
ncv = int(li[ptr])
if ncv > 0:
    nconv = np.zeros((ncv,2), dtype = int)
    htf = np.zeros((ncv,2), dtype = float)
    for i in range(0,ncv):
        ptr = ptr + 1
        tmp = li[ptr].split()
        nconv[i, 0] =int(tmp[0])
        nconv[i, 1] =int(tmp[1])
        htf[i,0] = float(tmp[2])
        htf[i,1] = float(tmp[3])
#----- Bandwidth Evaluation ----- 
nbw = 0
for i in range(0, ne):
    nmin = noc[i][0]
    nmax = noc[i][0]
    for j in range(0, nen):
        if nmin > noc[i][j]:
            nmin = noc[i][j]
        if nmax < noc[i][j]:
            nmax = noc[i][j]
        ntmp = nmax - nmin + 1
    if nbw < ntmp:
        nbw = ntmp
stiff = np.zeros((nn,nbw),dtype = float)
# ----- stiffness matrix ----- 
#--- Stiffness ---
bt = np.zeros((2, 3), dtype = float)
#--- heat flux addition   
if nhf > 0:
    for i in range(0,nhf):
        n1 = nflux[i][0] - 1
        n2 = nflux[i][1] - 1
        v = flux[i]
        elen = math.sqrt((x[n1][0]-x[n2][0])**2+ (x[n1][1]-x[n2][1])**2)
        f[n1] = f[n1] - elen * v / 2
        f[n2] = f[n2] - elen * v / 2
if ncv > 0:
    for i in range(0,ncv):
        n1 = nconv[i][0] - 1
        n2 = nconv[i][1] - 1
        elen = math.sqrt((x[n1][0]-x[n2][0])**2+ (x[n1][1]-x[n2][1])**2)
        f[n1] = f[n1] + elen * htf[i,0] * htf[i,1] / 2
        f[n2] = f[n2] + elen * htf[i,0] * htf[i,1] / 2
        stiff[n1][0] = stiff[n1][0] + htf[i,0] * elen / 3
        stiff[n2][0] = stiff[n2][0] + htf[i,0] * elen / 3
        if n1 >= n2:
            n3 = n1
            n1 = n2
            n2 = n3
        stiff[n1][n2 - n1] = stiff[n1][n2 - n1] + htf[i,0] * elen / 6
#----- conductivity matrix
for i in range(0,ne):
    i1 = noc[i][0] - 1
    i2 = noc[i][1] - 1
    i3 = noc[i][2] - 1
    x32 = x[i3][0] - x[i2][0]
    x13 = x[i1][0] - x[i3][0]
    x21 = x[i2][0] - x[i1][0]
    y23 = x[i2][1] - x[i3][1]
    y31 = x[i3][1] - x[i1][1]
    y12 = x[i1][1] - x[i2][1]
    detj = x13 * y23 - x32 * y31
    area = 0.5 * abs(detj)
#--- element heat sources
    if ehs[i] != 0:
        c = ehs[i] * area / 3
        f[i1] = f[i1] + c
        f[i2] = f[i2] + c
        f[i3] = f[i3] + c
    bt[0][0] = y23
    bt[0][1] = y31
    bt[0][2] = y12
    bt[1][0] = x32
    bt[1][1] = x13
    bt[1][2] = x21
    for ii in range(0,3):
        for jj in range(0,2):
            bt[jj][ii] = bt[jj][ii] / detj
    for ii in range(0,3):
        for jj in range(0,3):
            ii1 = noc[i][ii] - 1
            ii2 = noc[i][jj] - 1
            if ii1 <= ii2:
                sum = 0
                for j in range(0,2):
                    sum = sum + bt[j][ii] * bt[j][jj]
            ic = ii2 - ii1
            stiff[ii1][ic] = stiff[ii1][ic] + sum * area * pm[mat[i]-1]
#---function ModifyForBC---
if nd > 0:
#--- modify for temp. boundary conditions
    sum = 0
    for i in range(0,nn):
        sum = sum + stiff[i][0]
    sum = sum / nn
    cnst = sum * 1000000
    for i in range(0,nd):
        n = nu[i] - 1
        stiff[n][0] = stiff[n][0] + cnst
        f[n] = f[n] + cnst * u[i]
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
f = bansol(stiff,f,nbw)
#----- Heat Flow Calculation ----- 
for i in range(0,ne):
    i1 = noc[i][0] - 1
    i2 = noc[i][1] - 1
    i3 = noc[i][2] - 1
    x32 = x[i3][0] - x[i2][0]
    x13 = x[i1][0] - x[i3][0]
    x21 = x[i2][0] - x[i1][0]
    y23 = x[i2][1] - x[i3][1]
    y31 = x[i3][1] - x[i1][1]
    y12 = x[i1][1] - x[i2][1]
    detj = x13 * y23 - x32 * y31
    bt[0][0] = y23
    bt[0][1] = y31
    bt[0][2] = y12
    bt[1][0] = x32
    bt[1][1] = x13
    bt[1][2] = x21
    for ii in range (0,3):
        for jj in range(0,2):
            bt[jj][ii] = bt[jj][ii] / detj
    qx = bt[0][0] * f[i1] + bt[0][1] * f[i2] + bt[0][2] * f[i3]
    qx = -qx * pm[mat[i]-1]
    qy = bt[1][0] * f[i1] + bt[1][1] * f[i2] + bt[1][2] * f[i3]
    qy = -qy * pm[mat[i]-1]
    q[i][0] = qx
    q[i][1] = qy

print("Results")
print("for data in file",file1)
print("node#   temperature")
for i in range(0,nn):
    print('{:5d} {:12.4e}'.format(i+1,f[i]))
print("conduction heat flow per unite area in each element")
print("elem#   qx           qy")
for i in range(0,ne):
    print('{:5d} {:12.4e} {:12.4e}'.format(i+1,q[i,0],q[i,1]))

