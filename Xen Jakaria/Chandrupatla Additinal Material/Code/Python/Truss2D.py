#Program TRUSS2D
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "truss2d.inp"
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
nq = nn*ndn
#Allocate arrays
x = np.zeros((nn,ndim))
noc = np.zeros((ne,nen),dtype = int)
f = np.zeros((nq))
area = np.zeros((ne))
mat = np.zeros((ne),dtype = int)
dt = np.zeros((ne))
pm = np.zeros((nm,npr))
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd))
mpc = np.zeros((nmpc,2),dtype = int)
bt = np.zeros((nmpc,3))
stress = np.zeros(ne)
se = np.zeros((4,4))
tl = np.zeros(4)
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
    area[n-1] = float(tmp[nen+2])
    dt[n-1] = float(tmp[nen+3])
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
#----- multi-point constraints b1*qi+b2*qj=b0
for i in range(0,nmpc):
    tmp=li[ptr+i].split()
    bt[i,0] = float(tmp[0])
    mpc[i,0] = int(tmp[1])
    bt[i,1] = float(tmp[2])
    mpc[i,1] = int(tmp[3])
#bandwidth determination
def bandwidth(noc,ne,mpc,nmpc,nen):
    nbw = 0
    for n in range(0,ne):
        nabs = ndn*(abs(noc[n,0]-noc[n,1])+1)
        if nbw < nabs:
            nbw = nabs
    for i in range (0,nmpc):
        nabs = abs(mpc[i,0]-mpc[i,1])+1
        if nbw < nabs:
           nbw = nabs       
    return nbw

nbw =bandwidth(noc,ne,mpc,nmpc,nen) 
s = np.zeros((nq,nbw),dtype = float)
#-----  stiffness matrix -----
for n in range(0,ne):
    i1 = noc[n,0]-1
    i2 = noc[n,1]-1
    i3 = mat[n]-1
    x21 = x[i2,0] - x[i1,0]
    y21 = x[i2,1] - x[i1,1]
    el = math.sqrt(x21 * x21 + y21 * y21)
    eal = pm[i3,0] * area[n] / el
    cx = x21 / el
    cy = y21 / el
    #----------- element stiffness matrix se() -----------
    se[0,0] = cx * cx * eal
    se[0,1] = cx * cy * eal
    se[1,1] = cy * cy * eal
    se[1,0] = se[0,1]
    se[0,2] = -se[0,0]
    se[0,3] = -se[0,1]
    se[1,2] = -se[1,0]
    se[1,3] = -se[1,1]
    se[2,0] = -se[0,0]
    se[2,1] = -se[0,1]
    se[3,0] = -se[1,0]
    se[3,1] = -se[1,1]
    se[2,2] = se[0,0]
    se[2,3] = se[0,1]
    se[3,2] = se[1,0]
    se[3,3] = se[1,1]
    #-------------- temperature load tl() ---------------
    ee0 = pm[i3,1] * dt[n] * pm[i3,0] * area[n]
    tl[0] = -ee0 * cx
    tl[1] = -ee0 * cy
    tl[2] = ee0 * cx
    tl[3] = ee0 * cy
    for ii in range(0,nen):
        nrt = ndn * (noc[n, ii] - 1)
        for it in range (0,ndn):
            nr = nrt + it
            i = ndn * ii + it
            for jj in range(0,nen):
                nct = ndn * (noc[n, jj] - 1)
                for jt in range(0,ndn):
                    j = ndn * jj + jt
                    nc = nct + jt - nr
                    if nc >= 0:
                       s[nr,nc] = s[nr,nc] + se[i,j]
            f[nr] = f[nr] + tl[i]
#----- decide penalty parameter cnst -----
cnst = 0
for i in range(0,nq):
    if cnst < s[i,0]:
        cnst = s[i,0]

cnst = cnst * 10000
#----- modify for boundary conditions -----
#--- displacement bc ---
for i in range(0,nd):
    n = int(nu[i]-1)
    s[n,0] = s[n,0] + cnst
    f[n] = f[n] + cnst * u[i]
#--- multi-point constraints ---
for i in range(0,nmpc):
    i1 = mpc[i, 0]
    i2 = mpc[i, 1]
    s[i1,0] = s[i1,0] + cnst * bt[i,0] * bt[i,0]
    s[i2,0] = s[i2,0] + cnst * bt[i,1] * bt[i,1]
    ir = i1
    if ir > i2: 
        ir = i2
    ic = abs(i2 - i1)
    s[ir,ic] = s[ir,ic] + cnst * bt[i,0] * bt[i,1]
    f[i1] = f[i1] + cnst * bt[i,0] * bt[i,2]
    f[i2] = f[i2] + cnst * bt[i,1] * bt[i,2]
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
#----- stress calculation -----
for i in range(0,ne):
    i1 = noc[i,0]-1
    i2 = noc[i,1]-1
    i3 = mat[i]-1
    x21 = x[i2,0] - x[i1,0]
    y21 = x[i2,1] - x[i1,1]
    el = math.sqrt(x21 * x21 + y21 * y21)
    cx = x21 / el
    cy = y21 / el
    j1 = 2*i1
    j2 = j1+1
    k1 = 2*i2
    k2 = k1+1
    dlt = (f[k1] - f[j1]) * cx + (f[k2] - f[j2]) * cy
    stress[i] = pm[i3,0] * (dlt / el - pm[i3,1] * dt[i])
#----- reaction calculation -----
for i in range(0,nd):
    n = int(nu[i]-1)
    u[i] = cnst * (u[i] - f[n])
print("Results")
print("for data in file",file1)
print("node#   x-displ    y-displ")
for i in range(0,nn):
    print('{:5d} {:12.4e} {:12.4e}'.format(i+1,f[2*i],f[2*i+1]))
print("elem#   stress")
for i in range(0,ne):
    print('{:5d} {:12.4e}'.format(i+1,stress[i]))
print("node#   reaction")
for i in range(0,nd):
    print('{:5d} {:12.4e}'.format(nu[i],u[i]))
