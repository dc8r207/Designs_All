#Program FRAME3D
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "frame3d.inp"
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
tmp = li[5].split()
ndim = int(tmp[0])
nen = int(tmp[1])
ndn = int(tmp[2])
nnref = int(tmp[3])
nnt = nn + nnref
nq = ndn*nn
#Allocate arrays
x = np.zeros((nnt,ndim))
noc = np.zeros((ne,nen+1),dtype = int)
f = np.zeros((nq))
arin = np.zeros((ne,4),dtype = float)
udl = np.zeros((ne,2))
mat = np.zeros((ne),dtype = int)
pm = np.zeros((nm,npr))
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd))
mpc = np.zeros((nmpc,2),dtype = int)
bt = np.zeros((nmpc,3))
alambda = np.zeros((12,12),dtype = float)
se = np.zeros((12,12),dtype = float)
sep = np.zeros((12,12),dtype = float)
ed = np.zeros(12,dtype = float)
edp = np.zeros(12,dtype = float)
edf = np.zeros(12,dtype = float)
results1 = "Results\n" + "for data in file " + file1 +"\n"
results2 = ""
ptr = 7
#----- coordinates -----
for i in range(0,nnt):
    tmp=li[ptr+i].split()
    n = int(tmp[0])
    for j in range(0,ndim):
        x[n-1,j] = float(tmp[1+j])
ptr = ptr+nnt+1
#----- connectivity -----
for i in range(0,ne):
    tmp=li[ptr+i].split()
    n = int(tmp[0])
    for j in range(0,nen+1):
        noc[n-1,j] = int(tmp[1+j])
        mat[n-1] = int(tmp[nen+2])
        mat[n-1] = int(tmp[nen+2])
        arin[n-1,0] = float(tmp[nen+3])
        arin[n-1,1] = float(tmp[nen+4])
        arin[n-1,2] = float(tmp[nen+5])
        arin[n-1,3] = float(tmp[nen+6])    
        udl[n-1,0] = float(tmp[nen+7]) 
        udl[n-1,1] = float(tmp[nen+8])
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
    i3 = noc[n, 2]-1
    m = mat[n]-1
    x21 = x[i2, 0] - x[i1, 0]
    y21 = x[i2, 1] - x[i1, 1]
    z21 = x[i2, 2] - x[i1, 2]
    el = math.sqrt(x21 * x21 + y21 * y21 + z21 * z21)
    eal = pm[m, 0] * arin[n, 0] / el
    eiyl = pm[m, 0] * arin[n, 1] / el
    eizl = pm[m, 0] * arin[n, 2] / el
    gjl = pm[m, 1] * arin[n, 3] / el
    sep = np.zeros((12,12),dtype = float)
    sep[0,0] = eal
    sep[0,6] = -eal
    sep[6,6] = eal
    sep[3,3] = gjl
    sep[3,9] = -gjl
    sep[9,9] = gjl
    sep[1,1] = 12 * eizl / el**2
    sep[1,5] = 6 * eizl / el
    sep[1,7] = -sep[1,1]
    sep[1,11] = sep[1,5]
    sep[2,2] = 12 * eiyl / el**2
    sep[2,4] = -6 * eiyl / el
    sep[2,8] = -sep[2,2]
    sep[2,10] = sep[2,4]
    sep[4,4] = 4 * eiyl
    sep[4,8] = 6 * eiyl / el
    sep[4,10] = 2 * eiyl
    sep[5,5] = 4 * eizl
    sep[5,7] = -6 * eizl / el
    sep[5,11] = 2 * eizl
    sep[7,7] = 12 * eizl / el**2
    sep[7,11] = -6 * eizl / el
    sep[8,8] = 12 * eiyl / el**2
    sep[8,10] = 6 * eiyl / el
    sep[10,10] = 4 * eiyl
    sep[11,11] = 4 * eizl
    for i in range (0,12):
        for j in range (0,12):
            sep[j, i] = sep[i, j]
#convert element stiffness matrix to global system
    dcos = np.zeros((3,3),dtype = float)
    dcos[0,0] = x21 / el
    dcos[0,1] = y21 / el
    dcos[0,2] = z21 / el
    eip1 = x[i3, 0] - x[i1, 0]
    eip2 = x[i3, 1] - x[i1, 1]
    eip3 = x[i3, 2] - x[i1, 2]
    c1 = dcos[0,1] * eip3 - dcos[0,2] * eip2
    c2 = dcos[0,2] * eip1 - dcos[0,0] * eip3
    c3 = dcos[0,0] * eip2 - dcos[0,1] * eip1
    cc = math.sqrt(c1 * c1 + c2 * c2 + c3 * c3)
    dcos[2,0] = c1 / cc
    dcos[2,1] = c2 / cc
    dcos[2,2] = c3 / cc
    dcos[1,0] = dcos[2,1] * dcos[0,2] - dcos[0,1] * dcos[2,2]
    dcos[1,1] = dcos[0,0] * dcos[2,2] - dcos[2,0] * dcos[0,2]
    dcos[1,2] = dcos[2,0] * dcos[0,1] - dcos[0,0] * dcos[2,1]
    for k in range (0,4):
        ik = 3 * k
        for i in range (0,3):
            for j  in range (0,3):
                alambda[i + ik, j + ik] = dcos[i, j]
    if istf < 2:
         return sep
    se = np.zeros((12,12),dtype = float)
    se = np.mat(sep)*np.mat(alambda)
    for i in range (0,12):
        for j in range (0,12):
            sep[i, j] = se[i, j]
    se = np.zeros((12,12),dtype = float)
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
#----- loads due to uniformly distributed load on element
    if abs(udl[n, 0]) > 0 or abs(udl[n, 1]) > 0:
        i1 = noc[n, 0] - 1
        i2 = noc[n, 1] - 1
        x21 = x[i2, 0] - x[i1, 0]
        y21 = x[i2, 1] - x[i1, 1]
        el = math.sqrt(x21 * x21 + y21 * y21)        
        ed[0] = 0
        ed[3] = 0
        ed[6] = 0
        ed[9] = 0
        ed[1] = udl[n, 0] * el / 2
        ed[7] = ed[1]
        ed[5] = udl[n, 0] * el ** 2 / 12
        ed[11] = -ed[5]
        ed[2] = udl[n, 1] * el / 2
        ed[8] = ed[2]
        ed[4] = -udl[n, 1] * el ** 2 / 12
        ed[10] = -ed[4]
        for i in range(0,12):
            edp[i] = 0
            for k in range(0,12):
                edp[i] = edp[i] + alambda[k, i] * ed[k]
        for i  in range(0,6):
            f[6 * i1 + i] = f[6 * i1 + i] + edp[i]
            f[6 * i2 + i] = f[6 * i2 + i] + edp[i + 6]


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
#----- reaction calculation -----
for i in range(0,nd):
    n = int(nu[i]-1)
    u[i] = cnst * (u[i] - f[n])
#---- member end-actions
results2 = results2 + "member end forces\n"
for n in range(0,ne):
    istf = 1
    sep = elstiff(n,x,noc,mat,pm,arin,alambda,istf)
    i1 = noc[n,0] - 1
    i2 = noc[n,1] - 1
    for i in range(0,6):
        ed[i] = f[6 * i1 + i]
        ed[i + 6] = f[6 * i2 + i]
    for i in range(0,12):
        edp[i] = 0
        for k in range(0,12):
            edp[i] = edp[i] + alambda[i, k] * ed[k]
# end forces due to distributed loads
    if abs(udl[n, 0]) > 0 or abs(udl[n, 1]) > 0:
        x21 = x[i2, 0] - x[i1, 0]       
        y21 = x[i2, 1] - x[i1, 1]
        z21 = x[i2, 2] - x[i1, 2]
        el = math.sqrt(x21 * x21 + y21 * y21 + z21 * z21)
        ed[0] = 0
        ed[3] = 0
        ed[6] = 0
        ed[9] = 0
        ed[1] = -udl[n, 0] * el / 2
        ed[7] = ed[1]
        ed[5] = -udl[n, 0] * el ** 2 / 12
        ed[11] = -ed[5]
        ed[2] = -udl[n, 1] * el / 2
        ed[8] = ed[2]
        ed[4] = udl[n, 1] * el ** 2 / 12
        ed[10] = -ed[4]
    else:
        for k in range(0,12):
            ed[k] = 0
    for i in range(0,12):
        for k in range(0,12):
            ed[i] = ed[i] + sep[i, k] * edp[k]
    results2 = results2 + "element# " + str(n+1) +"  end forces\n" 
    for i in range(0,2):
        ii = i * 6
        for j in range(0,6):
            results2 = results2 + str("%12.4e" % ed[ii+i]) +" "
        results2 = results2 + "\n"
results1 = results1 + "node# x-displ y-displ z-displ  x-rot  y-rot  z-rot\n"
for i in range(0,nn):
    ii = 6*i
    results1 = results1 + str(i+1) + " "
    for j in range(0,6):
        results1 = results1 + str("%12.4e" % f[ii+i]) +" "
    results1 = results1 + "\n"
results1 = results1 + results2 + "node#   reaction\n"
for i in range(0,nd):
    results1 = results1 + str("%5d"% nu[i]) +" "+ str("%12.4e"% u[i]) + "\n" 
print(results1)