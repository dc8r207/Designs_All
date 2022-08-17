#Program FRAME2D
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "frame2d.inp"
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
tmp = li[5].split()
ndim = int(tmp[0])
nen = int(tmp[1])
ndn = int(tmp[2])
nq = ndn*nn
#Allocate arrays
x = np.zeros((nn,ndim))
noc = np.zeros((ne,nen),dtype = int)
f = np.zeros((nq))
arin = np.zeros((ne,2),dtype = float)
udl = np.zeros((ne))
mat = np.zeros((ne),dtype = int)
pm = np.zeros((nm,npr))
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd))
mpc = np.zeros((nmpc,2),dtype = int)
bt = np.zeros((nmpc,3))
se = np.zeros((6,6),dtype = float)
sep = np.zeros((6,6),dtype = float)
alambda = np.zeros((6,6),dtype = float)
ed = np.zeros(6,dtype = float)
edp = np.zeros(6,dtype = float)
edf = np.zeros(6,dtype = float)

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
    noc[n-1,0] = int(tmp[1])
    noc[n-1,1] = int(tmp[2])
    mat[n-1] = int(tmp[3])
    arin[n-1,0] = float(tmp[4])
    arin[n-1,1] = float(tmp[5])
    udl[n-1] = float(tmp[6])
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
nbw = bandwidth(noc,ne,mpc,nmpc,nen)
s = np.zeros((nq,nbw))

def elstiff(n,x,noc,mat,pm,arin,alambda,istf):
#----- element stiffness matrix -----
    i1 = noc[n, 0]-1
    i2 = noc[n, 1]-1
    m = mat[n]-1
    x21 = x[i2, 0] - x[i1, 0]
    y21 = x[i2, 1] - x[i1, 1]
    el = math.sqrt(x21 * x21 + y21 * y21)
    eal = pm[m, 0] * arin[n, 0] / el
    eizl = pm[m, 0] * arin[n, 1] / el
    sep = np.zeros((6,6),dtype = float)

    sep[0, 0] = eal
    sep[0, 3] = -eal
    sep[3, 3] = eal
    sep[1, 1] = 12 * eizl / el**2
    sep[1, 2] = 6 * eizl / el
    sep[1, 4] = -sep[1, 1]
    sep[1, 5] = sep[1, 2]
    sep[2, 2] = 4 * eizl
    sep[2, 4] = -6 * eizl / el
    sep[2, 5] = 2 * eizl
    sep[4, 4] = 12 * eizl / el**2
    sep[4, 5] = -6 * eizl / el
    sep[5, 5] = 4 * eizl

    for i in range (0,6):
        for j in range (i,6):
            sep[j, i] = sep[i, j]

#convert element stiffness matrix to global system
    dcos = np.zeros((3,3),dtype = float)
    
    dcos[0, 0] = x21 / el
    dcos[0, 1] = y21 / el
    dcos[1, 0] = -dcos[0, 1]
    dcos[1, 1] = dcos[0, 0]
    dcos[2, 2] = 1

    for k in range (0,2):
        ik = 3 * k
        for i in range (0,3):
            for j in range (0,3):
                alambda[i + ik, j + ik] = dcos[i, j]
    if istf < 2:
        return sep

    se = np.zeros((6,6),dtype = float)
    se = np.mat(sep)*np.mat(alambda)

    for i in range (0,6):
        for j in range (0,6):
            sep[i, j] = se[i, j]
    se = np.zeros((6,6),dtype = float)
    se = np.mat(alambda).T*np.mat(sep)
    return se

#-----  stiffness matrix -----
for n in range(0,ne):
    istf = 2
    se = elstiff(n,x,noc,mat,pm,arin,alambda,istf)
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
    #----- Loads due to uniformly distributed load on element
    if abs(udl[n]) > 0:
        i1 = noc[n, 0]-1
        i2 = noc[n, 1]-1
        x21 = x[i2, 0] - x[i1, 0]
        y21 = x[i2, 1] - x[i1, 1]
        el = math.sqrt(x21 * x21 + y21 * y21)
        ed[0] = 0
        ed[3] = 0
        ed[1] = udl[n] * el / 2
        ed[4] = ed[1]
        ed[2] = udl[n] * el**2 / 12
        ed[5] = -ed[2]
        edp = np.mat(alambda).T*np.mat(ed).T
        for i in range(0,3):
          f[3 * i1 + i] = f[3 * i1 + i] + edp[i]
          f[3 * i2 + i] = f[3 * i2 + i] + edp[i + 3]
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
print("Results")
print("for data in file",file1)
print("node#   x-displ    y-displ    z-rotation(rad)")
for i in range(0,nn):
    i1=3*i
    print('{:5d}{:12.4e}{:12.4e}{:12.4e}'.format(i+1,f[i1],f[i1+1],f[i1+2]))
#----- reaction calculation -----
for i in range(0,nd):
    n = int(nu[i]-1)
    u[i] = cnst * (u[i] - f[n])
#---- member end-actions
for n in range(0,ne):
    istf = 1
    sep = elstiff(n,x,noc,mat,pm,arin,alambda,istf)
    i1 = noc[n, 0]-1
    i2 = noc[n, 1]-1
    for i in range(0,3):
        ed[i] = f[3 * i1 + i]
        ed[i + 3] = f[3 * i2 + i]
    for i in range(0,6):
        edp[i] = 0
        for k in range(0,6):
            edp[i] = edp[i] + alambda[i,k]*ed[k]
# end forces due to distributed loads
    if abs(udl[n]) > 0:
        x21 = x[i2, 0] - x[i1, 0]
        y21 = x[i2, 1] - x[i1, 1]
        el = math.sqrt(x21 * x21 + y21 * y21)
        ed[0] = 0
        ed[3] = 0
        ed[1] = -udl[n] * el / 2
        ed[4] = ed[1]
        ed[2] = -udl[n] * el**2 / 12
        ed[5] = -ed[2]
    else:
        ed = np.zeros(6,dtype = float)
    for i in range(0,6):
        for k in range(0,6):
            ed[i] = ed[i] + sep[i, k] * edp[k]
    print("member",n+1)
    print('{:12.4e}{:12.4e}{:12.4e}'.format(ed[0],ed[1],ed[2]))
    print('{:12.4e}{:12.4e}{:12.4e}'.format(ed[3],ed[4],ed[5]))
print("node#   reaction")
for i in range(0,nd):
    print('{:5d} {:12.4e}'.format(nu[i],u[i]))


    