#Program Axisym (Axisymmetric Triangle element)
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "axisym.inp"
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
stress = np.zeros((ne,6))
se = np.zeros((6,6))
tml = np.zeros(6)
d = np.zeros((4,4))
b = np.zeros((4,6),dtype = float)
db = np.zeros((4,6))
q = np.zeros(6)
st = np.zeros(4)
results1 = "Results\n" + "for data in file " + file1 +"\n"
results2 = ""
vm = ""
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
def dmat(n,mat,pm):
#----- d(), b() and db() matrices
#--- first the d-matrix
    m = mat[n]-1
    e = pm[m, 0]
    pnu = pm[m, 1]
    c1 = e * (1 - pnu) / ((1 + pnu) * (1 - 2 * pnu))
    c2 = pnu / (1 - pnu)
    d = np.zeros((4,4))
    d[0, 0] = c1
    d[0, 1] = c1 * c2
    d[0, 3] = c1 * c2
    d[1, 0] = d[0, 1]
    d[1, 1] = c1
    d[1, 3] = c1 * c2
    d[2, 2] = .5 * e / (1 + pnu)
    d[3, 0] = d[0, 3]
    d[3, 1] = d[1, 3]
    d[3, 3] = c1
    return d
#function dbse gives db with ifl = 1, se  with ifl = 2
def dbse(n,x,noc,d,mat,pm,dt,tml,ifl):
#--- strain-displacement matrix b()
    i1 = noc[n, 0]-1
    i2 = noc[n, 1]-1
    i3 = noc[n, 2]-1
    r1 = x[i1, 0]
    r2 = x[i2, 0]
    r3 = x[i3, 0]    
    z1 = x[i1, 1]
    z2 = x[i2, 1]
    z3 = x[i3, 1]
    r21 = r2 - r1
    r32 = r3 - r2
    r13 = r1 - r3
    z12 = z1 - z2
    z23 = z2 - z3
    z31 = z3 - z1
#--- determinant of jacobian
    dj = r13 * z23 - r32 * z31
    rbar = (r1 + r2 + r3) / 3
    b = np.zeros((4,6),dtype = float)
#--- definition of b() matrix
    b[0, 0] = z23 / dj
    b[1, 0] = 0
    b[2, 0] = r32 / dj
    b[3, 0] = 1 / (3 * rbar)
    b[0, 1] = 0
    b[1, 1] = r32 / dj
    b[2, 1] = z23 / dj
    b[3, 1] = 0
    b[0, 2] = z31 / dj
    b[1, 2] = 0
    b[2, 2] = r13 / dj
    b[3, 2] = 1 / (3 * rbar)
    b[0, 3] = 0
    b[1, 3] = r13 / dj
    b[2, 3] = z31 / dj
    b[3, 3] = 0
    b[0, 4] = z12 / dj
    b[1, 4] = 0
    b[2, 4] = r21 / dj
    b[3, 4] = 1 / (3 * rbar)
    b[0, 5] = 0
    b[1, 5] = r21 / dj
    b[2, 5] = z12 / dj
    b[3, 5] = 0
#--- db matrix db = d*b
    db = np.matmul(d,b)
    if ifl < 2:
        return db 
#--- Temperature Load Vector
    m = mat[n]-1
    al = pm[m,2]
    c = al * dt[n] * math.pi * rbar * abs(dj)
    for i in range(0,6):
           tml[i] = c * (db[0, i] + db[1, i] + db[3, i])
#--- element stiffness
    se = abs(dj)*math.pi*rbar*np.matmul(np.transpose(b),db)
    return se
for n in range(0,ne):
    d = dmat(n,mat,pm)
    ifl = 2
    se = dbse(n,x,noc,d,mat,pm,dt,tml,ifl)
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
            f[nr] = f[nr] + tml[i]
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
#----- stess Evaluation
vm = "Element vonMises stress values\n"
results2 = results2 + "stresses in elements"
results2 = results2 + "elem# sig-r  sig-z  sig-r  hoop  s1  s2   ang \n"
for n in range(0,ne):
    d = dmat(n,mat,pm)
    ifl = 1
    db = dbse(n,x,noc,d,mat,pm,dt,tml,ifl)
    for i in range(0,nen):
        ii = noc[n,i]-1
        q[2*i] = f[2*ii]
        q[2*i+1] = f[2*ii+1]
    m = mat[n]-1
    c1 = pm[m,2] * dt[n]
    st = np.matmul(db,q)
    for i in range(0,4):
        st[i] = st[i] - c1 * (d[i, 0] + d[i, 1] + d[i, 3])
        results2 = results2 + str("%12.4e" % st[i]) + " "
#--- principal stress calculations
        if st[2] == 0:
            s1 = st[0]
            s2 = st[1]
            ang = 0
            if s2 > s1:
                s1 = st[1]
                s2 = st[0]
                ang = 90
        else:
           c = .5 * (st[0] + st[1])
           r = math.sqrt(.25 * (st[0] - st[1])**2 + (st[2])**2)
           s1 = c + r
           s2 = c - r
           if c > st[0]:
               ang = 57.2957795 * np.arctan(st[2] / (s1 - st[0]))
               if st[2] > 0:
                   ang = 90 - ang
               if st[2] < 0:
                   ang = -90 - ang
           else:
              ang = 57.29577951 * np.arctan(st[2] / (st[0] - s2))
    s3 = st[3]
    c = (s1 - s2)**2 + (s2 - s3)**2 + (s3 - s1)**2
    c= math.sqrt(.5 * c)
    vm = vm + str("%10.4f" % c) + "\n"
    results2 = results2 + str("%12.4e" % s1) + str("%12.4e" % s2)
    results2 = results2 + str("%12.4e" % ang) + "\n"
results1 = results1 + "node# r-displ z-displ\n"
for i in range(0,nn):
    ii = ndn*i
    results1 = results1 + str(i+1) + " "
    for j in range(0,ndn):
        results1 = results1 + str("%12.4e" % f[ii+j]) +" "
    results1 = results1 + "\n"
results1 = results1 + results2 + "node#   reaction\n"
for i in range(0,nd):
    results1 = results1 + str("%5d"% nu[i]) +" "+ str("%12.4e"% u[i]) + "\n"
results1 = results1 + vm
print(results1)