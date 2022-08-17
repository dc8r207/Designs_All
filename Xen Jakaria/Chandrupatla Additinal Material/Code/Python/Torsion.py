#Program Torsion
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "torsion.inp"
#Set lc = 1 for plane stess; 2 for plane strain
lc = 1
#Set ipl = 1 for for vonMises stress; 2 for max shear stress
ipl = 1
f = open(file1, "r")
li=f.read().splitlines()
f.close
tmp=li[3].split()
nn = int(tmp[0])
ne = int(tmp[1])
nm = int(tmp[2])
nd = int(tmp[3])
nl = int(tmp[4])
nmpc = int(tmp[5])
npr = int(tmp[6])
tmp=li[5].split()
ndim = int(tmp[0])
nen = int(tmp[1])
ndn = int(tmp[2])
#Allocate arrays
x = np.zeros((nn,ndim), dtype = float)
noc = np.zeros((ne,nen),dtype = int)
f = np.zeros((nq), dtype = float)
mat = np.zeros((ne),dtype = int)
pm = np.zeros((nm,npr), dtype = float)
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd), dtype = int)
bt = np.zeros((2,3), dtype = float)
tau = np.zeros((ne,2), dtype = float)
ptr = 7
#----- coordinates -----
for i in range(0,nn):
    tmp=li[ptr+i].split()
    n = int(tmp[0])
    for j in range(0,ndim):
        x[n-1,j] = float(tmp[1+j])
ptr = ptr+nn+1
#----- connectivity -----
for i in range(0,ne):
    tmp=li[ptr+i].split()
    n = int(tmp[0])
    for j in range(0,nen):
        noc[n-1,j] = int(tmp[1+j])
    mat[n-1] = int(tmp[nen+1]) 
ptr = ptr+ne+1
#----- specified displacements -----
for i in range(0,nd):
    tmp=li[ptr+i].split()
    nu[i] = int(tmp[0])
    u[i] = float(tmp[1])
ptr = ptr+nd+1
#----- component loads -----
for i in range(0,nl):
    tmp=li[ptr+i].split()
    n = int(tmp[0])
    f[n-1] = float(tmp[1])
ptr = ptr+nl+1    
#----- material properties -----
for i in range(0,nm):
    tmp=li[ptr+i].split()
    n = int(tmp[0])
    for j in range(0,npr):
        pm[n-1,j]=float(tmp[1+j])
ptr = ptr+nm+1 
#----- torque ---------
torque = float(li[ptr])
#----- symmetry factor (eg. if 1/4 symmetry, then = 4.0)  ---
sfac = float(li[ptr+2])
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
#--- Stiffness ---
#----- stiffness matrix
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
#--- load calculation
    c = 2 * area / 3
    f[i1] = f[i1] + c
    f[i2] = f[i2] + c
    f[i3] = f[i3] + c
    bt[0][0] = y23 / detj
    bt[0][1] = y31 / detj
    bt[0][2] = y12 / detj
    bt[1][0] = x32 / detj
    bt[1][1] = x13 / detj
    bt[1][2] = x21 / detj
    for ii in range(0,3):
        for jj in range(0,3):
            ii1 = noc[i][ii] - 1
            ii2 = noc[i][jj] - 1
            if ii1 <= ii2:
                sum = 0
                for j in range(0,2):
                    sum = sum + bt[j][ii] * bt[j][jj]
            ic = ii2 - ii1
            stiff[ii1][ic] = stiff[ii1][ic] + sum * area
#--- modify for boundary conditions
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
#--- Angle of twist and shear stress calculations
#----- Angle of Twist per unit length ----- 
sum = 0
for i in range(0,ne):
    m = mat[i] - 1
    smod = pm[m]
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
    sum = sum + abs(detj) / 3 * (f[i1] + f[i2] + f[i3])
smod = pm[0]
alpha = torque / smod / sum / sfac
#-----  and Shear Stress Calculations ----- 
for i in range(0,ne):
     m = mat[i] - 1
     smod = pm[m]
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
     bt[0][0] = y23 / detj
     bt[0][1] = y31 / detj
     bt[0][2] = y12 / detj
     bt[1][0] = x32 / detj
     bt[1][1] = x13 / detj
     bt[1][2] = x21 / detj
     tauyz = -(bt[0][0] * f[i1] + bt[0][1] * f[i2] + bt[0][2] * f[i3])
     tauyz = tauyz * smod * alpha
     tauxz = bt[1][0] * f[i1] + bt[1][1] * f[i2] + bt[1][2] * f[i3]
     tauxz = tauxz * smod * alpha
     tau[i][0] = tauyz
     tau[i][1] = tauxz
print("Results")
print("for data in file",file1)
print("node#   stress function value")
for i in range(0,nn):
    print('{:5d} {:12.4e}'.format(i+1,f[i]))
print("twist per unit length")
print('{:12.4e}'.format(alpha[0]))
print("Shear Stresses TauYZ, TauXZ in Each Element")
print("elem#   TauYZ        TauXZ")
for i in range(0,ne):
    print('{:5d} {:12.4e} {:12.4e}'.format(i+1,tau[i,0],tau[i,1]))

