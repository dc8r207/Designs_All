#Program Tetra3D (Tetrahedral Element for 3D)
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "tetra3d.inp"
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
mat = np.zeros((ne),dtype = int)
dt = np.zeros((ne))
pm = np.zeros((nm,npr))
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd))
mpc = np.zeros((nmpc,2),dtype = int)
bt = np.zeros((nmpc,3))
se = np.zeros((12,12))
d = np.zeros((6,6))
b = np.zeros((6,12))
db = np.zeros((6,12))
qt = np.zeros(12)
st = np.zeros(6)
results1 = "Results\n" + "for data in file " + file1 +"\n"
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
    dt[n-1] = float(tmp[nen+2])
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
#----- bandwidth nbw from connectivity noc() and mpc
nbw = 0
for i in range(0,ne):
    nmin = noc[i,0]
    nmax = noc[i,0]
    for j in range(0,nen):
        if nmin > noc[i,j]:
            nmin = noc[i,j]
        if nmax < noc[i,j]:
            nmax = noc[i,j]
    ntmp = ndn * (nmax - nmin + 1)
    if nbw < ntmp:
        nbw = ntmp
for i in range(0,nmpc):
    nabs = abs(mpc[i,0] - mpc[i,1]) + 1
    if nbw < nabs:
        nbw = nabs
s = np.zeros((nq,nbw))
#--- d-matrix
def dmat(n, mat,pm):
#--- d-matrix
    m = mat[n]-1
    e = pm[m,0]
    pnu = pm[m,1]
#----- d(), b() and db() matrices
#--- first the d-matrix
    d = np.zeros((6,6))
#--- d-matrix
    m = mat[n]-1
    e = pm[m,0]
    pnu = pm[m,1]
    c4 = e / ((1 + pnu) * (1 - 2 * pnu))
    c1 = c4 * (1 - pnu)
    c2 = c4 * pnu
    c3 = .5 * e / (1 + pnu)
    d[0, 0] = c1
    d[0, 1] = c2
    d[0, 2] = c2
    d[1, 0] = c2
    d[1, 1] = c1
    d[1, 2] = c2
    d[2, 0] = c2
    d[2, 1] = c2
    d[2, 2] = c1
    d[3, 3] = c3
    d[4, 4] = c3
    d[5, 5] = c3
    return d
#---db/ se function ifl = 2 for se, ifl = 1 for db
def dbse(n,x,noc,d,mat,pm,dt,qt,ifl):
#--- strain-displacement matrix b()
    i1 = noc[n, 0] - 1
    i2 = noc[n, 1] - 1
    i3 = noc[n, 2] - 1
    i4 = noc[n, 3] - 1
    x14 = x[i1, 0] - x[i4, 0]
    x24 = x[i2, 0] - x[i4, 0]
    x34 = x[i3, 0] - x[i4, 0]
    y14 = x[i1, 1] - x[i4, 1]
    y24 = x[i2, 1] - x[i4, 1]
    y34 = x[i3, 1] - x[i4, 1]
    z14 = x[i1, 2] - x[i4, 2]
    z24 = x[i2, 2] - x[i4, 2]
    z34 = x[i3, 2] - x[i4, 2]
    dj1 = x14 * (y24 * z34 - z24 * y34)
    dj2 = y14 * (z24 * x34 - x24 * z34)
    dj3 = z14 * (x24 * y34 - y24 * x34)
    dj = dj1 + dj2 + dj3
    a11 = (y24 * z34 - z24 * y34) / dj
    a21 = (z24 * x34 - x24 * z34) / dj
    a31 = (x24 * y34 - y24 * x34) / dj
    a12 = (y34 * z14 - z34 * y14) / dj
    a22 = (z34 * x14 - x34 * z14) / dj
    a32 = (x34 * y14 - y34 * x14) / dj
    a13 = (y14 * z24 - z14 * y24) / dj
    a23 = (z14 * x24 - x14 * z24) / dj
    a33 = (x14 * y24 - y14 * x24) / dj
#---  b matrix
    b = np.zeros((6, 12), dtype = float)
    b[0, 0] = a11
    b[0, 3] = a12
    b[0, 6] = a13
    b[0, 9] = -a11 - a12 - a13
    b[1, 1] = a21
    b[1, 4] = a22
    b[1, 7] = a23
    b[1, 10] = -a21 - a22 - a23
    b[2, 2] = a31
    b[2, 5] = a32
    b[2, 8] = a33
    b[2, 11] = -a31 - a32 - a33
    b[3, 1] = a31
    b[3, 2] = a21
    b[3, 4] = a32
    b[3, 5] = a22
    b[3, 7] = a33
    b[3, 8] = a23
    b[3, 10] = b[2, 11]
    b[3, 11] = b[1, 10]
    b[4, 0] = a31
    b[4, 2] = a11
    b[4, 3] = a32
    b[4, 5] = a12
    b[4, 6] = a33
    b[4, 8] = a13
    b[4, 9] = b[2, 11]
    b[4, 11] = b[0, 9]
    b[5, 0] = a21
    b[5, 1] = a11
    b[5, 3] = a22
    b[5, 4] = a12
    b[5, 6] = a23
    b[5, 7] = a13
    b[5, 9] = b[1, 10]
    b[5, 10] = b[0, 9]
#--- db matrix db = d*b
    db = np.matmul(d,b)
    if ifl < 2:
        return db
#--- Temperature Load Vector QT()
    c = pm[mat[n]-1,2] * dt[n]
    for i in range(0,12):
        dsum = db[0, i] + db[1, i] + db[2, i]
        qt[i] = c * abs(dj) * dsum / 6
#--- element stiffness se
    se = abs(dj)*np.matmul(np.transpose(b),db)/6
    return se
#-----  stiffness matrix -----
for n in range(0,ne):
    d = dmat(n,mat,pm)
    ifl = 2
    se = dbse(n,x,noc,d,mat,pm,dt,qt,ifl)
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
            f[nr] = f[nr] + qt[i]
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
results1 = results1 + "node# x-displ   y-displ   z-displ\n"
for i in range(0,nn):
    ii = ndn*i
    results1 = results1 + str(i+1) + " "
    for j in range(0,ndn):
        results1 = results1 + str("%12.4e" % f[ii+j]) +" "
    results1 = results1 + "\n"
#----- reaction calculation -----
for i in range(0,nd):
    n = int(nu[i]-1)
    u[i] = cnst * (u[i] - f[n])
#----- stess Evaluation
results2 = "el#  sx  sy  sz  tyz  txz  txy / s1  s2  s3\n"
for n in range(0,ne):
    results2 = results2 + str(n+1) + " "
    d = dmat(n,mat,pm)
    ifl = 1
    db = dbse(n,x,noc,d,mat,pm,dt,qt,ifl)
    for i in range(0,nen):
        i1 = 3*i
        i2 = 3*(noc[n,i]-1)
        for j in range(0,3):
            qt[i1+j] = f[i2+j]
    m = mat[n]-1
    c1 = pm[m,2] * dt[n]
    for i in range(0,6):
        st[i] = np.dot(db[i,0:12],qt[0:12])-c1*(d[i,0]+d[i,1]+d[i,2])
        results2 = results2 + str("%8.3f" %st[i]) + " "
#--- Principal Stress Calculations
    ai1 = st[0] + st[1] + st[2]
    ai21 = st[0] * st[1] + st[1] * st[2] + st[2] * st[0]
    ai22 = st[3] * st[3] + st[4] * st[4] + st[5] * st[5]
    ai2 = ai21 - ai22
    ai31 = st[0] * st[1] * st[2] + 2 * st[3] * st[4] * st[5]
    ai32 = st[0] * st[3]**2 + st[1] * st[4]**2 + st[2] * st[5]**2
    ai3 = ai31 - ai32
    c1 = ai2 - ai1**2 / 3
    c2 = -2 * (ai1 / 3)**3 + ai1 * ai2 / 3 - ai3
    c3 = 2 * math.sqrt(-c1 / 3)
    th = -3 * c2 / (c1 * c3)
    th2 = abs(1 - th * th)
    if th == 0:
        th = math.pi / 2
    if th > 0:
        th = math.atan(math.sqrt(th2) / th)
    if th < 0:
        th = math.pi - math.atan(math.sqrt(th2) / th)
    th = th / 3
#--- principal stresses
    p1 = ai1 / 3 + c3 * math.cos(th)
    p2 = ai1 / 3 + c3 * math.cos(th + 2 * math.pi / 3)
    p3 = ai1 / 3 + c3 * math.cos(th + 4 * math.pi / 3)
    results2 = results2 + "\n  "
    results2 = results2 + str("%9.3f" %p1) + " "
    results2 = results2 + str("%9.3f" %p2) + " "
    results2 = results2 + str("%9.3f" %p3) + "\n"
results1 = results1 + results2 + "dof#   Reactions\n"
for i in range(0,nd):
    results1 = results1 + str("%4d"% nu[i]) +" "+ str("%12.4e"% u[i]) + "\n"
print(results1)
