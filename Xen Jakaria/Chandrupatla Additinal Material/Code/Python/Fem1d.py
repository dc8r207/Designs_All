#Program FEM1D
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
file1 = "fem1d.inp"
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
ndim = int(tmp[3])
nen = int(tmp[4])
ndn = int(tmp[5])
tmp=li[5].split()
ndim = int(tmp[0])
nen = int(tmp[1])
ndn = int(tmp[2])
#Allocate arrays
x = np.zeros((nn))
noc = np.zeros((ne,nen),dtype = int)
f = np.zeros((nn))
area = np.zeros((ne))
mat = np.zeros((ne),dtype = int)
dt = np.zeros((ne))
pm = np.zeros((nm,npr))
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd))
mpc = np.zeros((nmpc,2),dtype = int)
bt = np.zeros((nmpc,3))
stress = np.zeros(ne)
ptr = 7
#----- coordinates -----
for i in range(0,nn):
    tmp=li[ptr+i].split()
    n = int(tmp[0])
    x[n-1] = float(tmp[1])
ptr = ptr+nn+1
#----- connectivity -----
for i in range(0,ne):
    tmp=li[ptr+i].split()
    n = int(tmp[0])
    noc[n-1,0] = int(tmp[1])
    noc[n-1,1] = int(tmp[2])
    mat[n-1] = int(tmp[3]) 
    area[n-1] = float(tmp[4])
    dt[n-1] = float(tmp[5])
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
        nabs = abs(noc[n,0]-noc[n,1])+1
        if nbw < nabs:
            nbw = nabs
    for i in range (0,nmpc):
        nabs = abs(mpc[i,0]-mpc[i,1])+1
        if nbw < nabs:
           nbw = nabs       
    return nbw

nbw =bandwidth(noc,ne,mpc,nmpc,nen) 
s = np.zeros((nn,nbw),dtype = float)
#----- stiffness matrix -----
for n in range(0,ne):
    n1 = noc[n,0]-1
    n2 = noc[n,1]-1
    n3 = mat[n]-1
    x21 = x[n2] - x[n1]
    el = abs(x21)
    eal = pm[n3,0]*area[n]/el
    if npr > 0:
        c = pm[n3,1]
    tl = pm[n3,0]*c*dt[n]*area[n]*el/x21
    #----- temperature loads -----
    f[n1] = f[n1] - tl
    f[n2] = f[n2] + tl
    #----- element stiffness in global locations -----
    s[n1,0] = s[n1,0] + eal
    s[n2,0] = s[n2,0] + eal
    ir = n1
    if ir > n2:
        ir = n2
    ic = n2-n1
    s[ir,ic] = s[ir,ic] - eal  
#----- decide penalty parameter cnst -----
cnst = 0
for i in range(0,nn):
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
for n in range(0,ne):
    n1 = noc[n,0]-1
    n2 = noc[n,1]-1
    n3 = int(mat[n]-1)
    eps = (f[n2] - f[n1]) / (x[n2] - x[n1])
    c = 0
    if npr > 0:
        c = pm[n3,1]
    stress[n] = pm[n3,0] * (eps - c * dt[n])
#----- reaction calculation -----
for i in range(0,nd):
    n = int(nu[i]-1)
    u[i] = cnst * (u[i] - f[n])
print("Results")
print("for data in file",file1)
print("node#   displacement")
for i in range(0,nn):
    print('{:5d} {:12.4e}'.format(i+1,f[i]))
print("elem#   stress")
for i in range(0,ne):
    print('{:5d} {:12.4e}'.format(i+1,stress[i]))
print("node#   reaction")
for i in range(0,nd):
    print('{:5d} {:12.4e}'.format(nu[i],u[i]))
    

