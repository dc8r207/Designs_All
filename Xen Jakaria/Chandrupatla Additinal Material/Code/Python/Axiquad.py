#Program AXIQUAD (Axisymmetric Quadrilateral Element)
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "axiquad.inp"
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
se = np.zeros((8,8))
tml = np.zeros(8)
d = np.zeros((4,4))
b = np.zeros((4,8))
db = np.zeros((4,8))
q = np.zeros(8)
st = np.zeros(4)
xni = np.zeros((4,2), dtype = float)
results1 = "Results\n" + "for data in file " + file1 +"\n"
results2 = ""
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
def dmat(n,mat,pm):
#--- d-matrix
    m = mat[n]-1
    e = pm[m,0]
    pnu = pm[m,1]
    d = np.zeros((4,4))
    c1 = e * (1 - pnu) / ((1 + pnu) * (1 - 2 * pnu))
    c2 = pnu / (1 - pnu)
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
def integ():
#------ Integration Points xni() --------
    c = .57735026919
    xni[0, 0] = -c
    xni[1, 0] = c
    xni[2, 0] = c
    xni[3, 0] = -c
    xni[0, 1] = -c
    xni[1, 1] = -c
    xni[2, 1] = c
    xni[3,1] = c
    return xni
xni = integ()
def dbse(n,x,noc,d,mat,pm,dt,tml,xi,eta,ifl):
#-------  db()  matrix  ------
#--- nodal coordinates
    n1 = noc[n, 0]-1
    n2 = noc[n, 1]-1
    n3 = noc[n, 2]-1
    n4 = noc[n, 3]-1
    x1 = x[n1, 0]
    y1 = x[n1, 1]
    x2 = x[n2, 0]
    y2 = x[n2, 1]
    x3 = x[n3, 0]
    y3 = x[n3, 1]
    x4 = x[n4, 0]
    y4 = x[n4, 1]
#---- formation of jacobian  tj
    tj11 = ((1 - eta) * (x2 - x1) + (1 + eta) * (x3 - x4)) / 4
    tj12 = ((1 - eta) * (y2 - y1) + (1 + eta) * (y3 - y4)) / 4
    tj21 = ((1 - xi) * (x4 - x1) + (1 + xi) * (x3 - x2)) / 4
    tj22 = ((1 - xi) * (y4 - y1) + (1 + xi) * (y3 - y2)) / 4
#--- determinant of the jacobian
    dj = tj11 * tj22 - tj12 * tj21
#--- a(3,4) matrix relates strains to
    a = np.zeros((3,4), dtype = float)
#--- local derivatives of u
    a[0, 0] = tj22 / dj
    a[1, 0] = 0
    a[2, 0] = -tj21 / dj
    a[0, 1] = -tj12 / dj
    a[1, 1] = 0
    a[2, 1] = tj11 / dj
    a[0, 2] = 0
    a[1, 2] = -tj21 / dj
    a[2, 2] = tj22 / dj
    a[0, 3] = 0
    a[1, 3] = tj11 / dj
    a[2, 3] = -tj12 / dj
#--- g(4,8) matrix relates local derivatives of u
#--- to local nodal displacements q(8)
    g = np.zeros((4,8), dtype = float)
    g[0, 0] = -(1 - eta) / 4
    g[1, 0] = -(1 - xi) / 4
    g[2, 1] = -(1 - eta) / 4
    g[3, 1] = -(1 - xi) / 4
    g[0, 2] = (1 - eta) / 4
    g[1, 2] = -(1 + xi) / 4
    g[2, 3] = (1 - eta) / 4
    g[3, 3] = -(1 + xi) / 4
    g[0, 4] = (1 + eta) / 4
    g[1, 4] = (1 + xi) / 4
    g[2, 5] = (1 + eta) / 4
    g[3, 5] = (1 + xi) / 4
    g[0, 6] = -(1 + eta) / 4
    g[1, 6] = (1 - xi) / 4
    g[2, 7] = -(1 + eta) / 4
    g[3, 7] = (1 - xi) / 4
#--- shape function values
    sh1 = .25 * (1 - xi) * (1 - eta)
    sh2 = .25 * (1 + xi) * (1 - eta)
    sh3 = .25 * (1 + xi) * (1 + eta)
    sh4 = .25 * (1 - xi) * (1 + eta)
    rad = sh1 * x1 + sh2 * x2 + sh3 * x3 + sh4 * x4
#'--- b(4,8) matrix relates strains to q
    for i in range(0,3):
        for j in range(0,8):
            c = 0
            for k in range(0,4):
                c = c + a[i, k] * g[k, j]
            b[i, j] = c
    b[3, 0] = sh1 / rad
    b[3, 1] = 0
    b[3, 2] = sh2 / rad
    b[3, 3] = 0
    b[3, 4] = sh3 / rad
    b[3, 5] = 0
    b[3, 6] = sh4 / rad
    b[3, 7] = 0
    db = np.matmul(d,b)
    if ifl < 2:
        return db
        print(db)
#sip is stiffness evaluated integration point
    sip = np.zeros((8,8), dtype = float)
    sip = 2*math.pi*rad*dj*np.matmul(np.transpose(b),db)
#--- determine temperature load tl
    m = mat[n] - 1
    c = pm[m, 2] * dt[n]
    for i in range(0,8):
        c1 = 2*math.pi*rad*dj*c*(db[0, i] + db[1, i] + db[3, i])
        tml[i] = tml[i] + c1
    return sip
def elstiff(n,x,noc,d,mat,pm,dt,tml,xni):
#--------  Element Stiffness and Temperature Load  -----
    se = np.zeros((8,8), dtype = float)
    for i in range(0,8):
        tml[i] = 0
        d = dmat(n,mat,pm)
#--- weight factor is one
#--- loop on integration points
        for ip in range(0,4):
            xi = xni[ip, 0]
            eta = xni[ip, 1]
            ifl = 2
            sip = dbse(n,x,noc,d,mat,pm,dt,tml,xi,eta,ifl)
#--- element stiffness matrix  se
            se = se + sip
        return se
#-----  stiffness matrix -----
for n in range(0,ne):
    d = dmat(n,mat,pm)
    ifl = 2
    se = elstiff(n,x,noc,d,mat,pm,dt,tml,xni)
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
results1 = results1 + "node# x-displ   y-displ\n"
for i in range(0,nn):
    ii = ndn*i
    results1 = results1 + str(i+1) + " "
    for j in range(0,ndn):
        results1 = results1 + str("%12.4e" % f[ii+j]) +" "
    results1 = results1 + "\n"
#----- stess Evaluation
results2 = "Elem#  Integ1  Integ2  Integ3  Integ4  "
results2 = results2 + "vonMises stresses\n"
for n in range(0,ne):
    for i in range(0,nen):
        ii = noc[n,i]-1
        q[2*i] = f[2*ii]
        q[2*i+1] = f[2*ii+1]
        d = dmat(n,mat,pm)
    results2 = results2 + str(n+1)
    for ip in range(0,4):
        
        ifl = 1
        xi = xni[ip, 0]
        eta = xni[ip, 1]        
        db = dbse(n,x,noc,d,mat,pm,dt,tml,xi,eta,ifl)
        st = np.matmul(db,q)
        m = mat[n]-1
        c1 = pm[m,2] * dt[n]
        for i in range(0,4):
            c = 0
            for k in range(0,8):
                c = c + db[i, k] * q[k]
            st[i] = c - c1 * (d[i, 0] + d[i, 1] + d[i, 3])
        c1 = st[0] + st[1] + st[3]
        c2 = st[0]*st[1]+st[1]*st[3]+st[3]*st[0]-st[2]*st[2]
        sv = math.sqrt(c1 * c1 - 3 * c2)
#--- vonMises stress at integration point
        r = math.sqrt(.25*(st[0]-st[1])**2 + st[2]**2)
        results2 = results2  + "  "+str("%10.4f" %sv)
    results2 = results2 + "\n"
#---stress function finished here
results1 = results1 + results2 + "dof#   Reactions\n"
for i in range(0,nd):
    results1 = results1 + str("%4d"% nu[i]) +" "+ str("%12.4e"% u[i]) + "\n"
print(results1)


