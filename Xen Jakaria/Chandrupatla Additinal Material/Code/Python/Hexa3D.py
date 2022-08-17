#Program QUAD (Quadrilateral Element)
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "hexa.inp"
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
x = np.zeros((nn,ndim), dtype = float)
noc = np.zeros((ne,nen),dtype = int)
f = np.zeros((nq), dtype = float)
mat = np.zeros((ne),dtype = int)
dt = np.zeros((ne), dtype = float)
pm = np.zeros((nm,npr), dtype = float)
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd), dtype = float)
mpc = np.zeros((nmpc,2),dtype = int)
bt = np.zeros((nmpc,3), dtype = float)
qe = np.zeros((24), dtype = float)
qt = np.zeros((24), dtype = float)
se = np.zeros((24,24), dtype = float)
d = np.zeros((6,6), dtype = float)
b = np.zeros((6,24), dtype = float)
db = np.zeros((6,24), dtype = float)
qt = np.zeros((24), dtype = float)
st = np.zeros((6), dtype = float)
g =np.zeros((6,9), dtype =float)
gn =np.zeros((3,8), dtype =float)
h =np.zeros((9,24), dtype =float)
tj =np.zeros((3,3), dtype =float)
aj =np.zeros((3,3), dtype =float)
xi = np.zeros((8,3), dtype = float)
xni = np.zeros((8,3), dtype = float)
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
def integ(xi):
#------- integration points xni() --------
    c = 0.57735026919
    xi[0][0] = -1
    xi[0][1] = -1
    xi[0][2] = -1
    xi[1][0] = 1
    xi[1][1] = -1
    xi[1][2] = -1
    xi[2][0] = 1
    xi[2][1] = 1
    xi[2][2] = -1
    xi[3][0] = -1
    xi[3][1] = 1
    xi[3][2] = -1
    xi[4][0] = -1
    xi[4][1] = -1
    xi[4][2] = 1
    xi[5][0] = 1
    xi[5][1] = -1
    xi[5][2] = 1
    xi[6][0] = 1
    xi[6][1] = 1
    xi[6][2] = 1
    xi[7][0] = -1
    xi[7][1] = 1
    xi[7][2] = 1
    for i in range (0,8):
        for  j in range (0,3):
            xni[i][j] = c*xi[i][j]
    return xni
def dmat(n,mat,pm):
#--- d() matrix relating stresses to strains
    m = mat[n] - 1
    e = pm[m][0]
    pnu = pm[m][1]
    c1 = e / ((1 + pnu) * (1 - 2 * pnu))
    c2 = 0.5 * e / (1 + pnu)
    d = np.zeros((6,6), dtype = float)
    d[0][0] = c1 * (1 - pnu)
    d[0][1] = c1 * pnu
    d[0][2] = d[0][1]
    d[1][0] = d[0][1]
    d[1][1] = d[0][0]
    d[1][2] = d[0][1]
    d[2][0] = d[0][2]
    d[2][1] = d[1][2]
    d[2][2] = d[0][0]
    d[3][3] = c2
    d[4][4] = c2
    d[5][5] = c2
    return d
def dbse(n,ip,x,noc,d,mat,pm,dt,qt,xi,xni,ifl):
#-------  db()  matrix  ------
    gn =np.zeros((3,8), dtype =float)
    aj =np.zeros((3,3), dtype =float)
    tj =np.zeros((3,3), dtype =float)
    aj =np.zeros((3,3), dtype =float)
    gn =np.zeros((3,8), dtype =float)    
#--- gradient of shape functions - the gn() matrix
    for i in range(0,3):
        for j in range(0,8):
            c = 1
            for k in range(0,3):
                if k!= i:
                    c = c * (1 + xi[j][k] * xni[ip][k])
                gn[i][j] = 0.125 * xi[j][i] * c
#--- formation of jacobian  tj
    for i in range(0,3):
        for j in range(0,3):
            tj[i][j] = 0
            for k in range(0,8):
                kn = noc[n][k] - 1
                tj[i][j] = tj[i][j] + gn[i][k] * x[kn][j]
#--- determinant of the jacobian
    dj1 = tj[0][0] * (tj[1][1] * tj[2][2] - tj[2][1] * tj[1][2])
    dj2 = tj[0][1] * (tj[1][2] * tj[2][0] - tj[2][2] * tj[1][0])
    dj3 = tj[0][2] * (tj[1][0] * tj[2][1] - tj[2][0] * tj[1][1])
    dj = dj1 + dj2 + dj3


#--- inverse of the jacobian aj()
    aj[0][0] = (tj[1][1] * tj[2][2] - tj[1][2] * tj[2][1]) / dj
    aj[0][1] = (tj[2][1] * tj[0][2] - tj[2][2] * tj[0][1]) / dj
    aj[0][2] = (tj[0][1] * tj[1][2] - tj[0][2] * tj[1][1]) / dj
    aj[1][0] = (tj[1][2] * tj[2][0] - tj[1][0] * tj[2][2]) / dj
    aj[1][1] = (tj[0][0] * tj[2][2] - tj[0][2] * tj[2][0]) / dj
    aj[1][2] = (tj[0][2] * tj[1][0] - tj[0][0] * tj[1][2]) / dj
    aj[2][0] = (tj[1][0] * tj[2][1] - tj[1][1] * tj[2][0]) / dj
    aj[2][1] = (tj[0][1] * tj[2][0] - tj[0][0] * tj[2][1]) / dj
    aj[2][2] = (tj[0][0] * tj[1][1] - tj[0][1] * tj[1][0]) / dj
    h = np.zeros((9,24), dtype =float)
    for i in range(0,3):
        for j in range(0,3):
            ir = 3 * i + j
            for k in range(0,8):
              ic = 3 * k + i
              h[ir][ic] = gn[j][k]
#--- g(6,9) matrix relates local derivatives of u
#--- to local nodal displacements q(24)
    g = np.zeros((6,9), dtype = float)
    g[0][0] = aj[0][0]
    g[0][1] = aj[0][1]
    g[0][2] = aj[0][2]
    g[1][3] = aj[1][0]
    g[1][4] = aj[1][1]
    g[1][5] = aj[1][2]
    g[2][6] = aj[2][0]
    g[2][7] = aj[2][1]
    g[2][8] = aj[2][2]
    g[3][3] = aj[2][0]
    g[3][4] = aj[2][1]
    g[3][5] = aj[2][2]
    g[3][6] = aj[1][0]
    g[3][7] = aj[1][1]
    g[3][8] = aj[1][2]
    g[4][0] = aj[2][0]
    g[4][1] = aj[2][1]
    g[4][2] = aj[2][2]
    g[4][6] = aj[0][0]
    g[4][7] = aj[0][1]
    g[4][8] = aj[0][2]
    g[5][0] = aj[1][0]
    g[5][1] = aj[1][1]
    g[5][2] = aj[1][2]
    g[5][3] = aj[0][0]
    g[5][4] = aj[0][1]
    g[5][5] = aj[0][2]
    b = np.zeros((6,24), dtype = float)
    db = np.zeros((6,24), dtype = float)
#--- b(6,24) matrix relates strains to q
    b = np.matmul(g,h)
    db = np.zeros((6,24), dtype = float)
#--- db(3,8) is stress-displ matrix at integration point
    db = np.matmul(d,b)
    if ifl < 2:
        return db
#sip is stiffness evaluated integration point
    sip = np.zeros((24,24), dtype = float)
    sip = dj*np.matmul(np.transpose(b),db)
#--- determine temperature load tl
    m = mat[n] - 1
    c = pm[m, 2] * dt[n]/6
    for i in range(0,24):
        qt[i] = qt[i] + c * abs(dj)*(db[0, i] + db[1, i] + db[2, i])
    return sip
#--- end of dbse
def elstiff(n,x,noc,d,mat,pm,dt,qt,xi,xni):
#--------  Element Stiffness and Temperature Load  -----
    se = np.zeros((24,24), dtype = float)
    for i in range(0,8):
        qt[i] = 0
        d = dmat(n,mat,pm)
#--- weight factor is one
#--- loop on integration points
        for ip in range(0,8):
            ifl = 2
            sip = dbse(n,ip,x,noc,d,mat,pm,dt,qt,xi,xni,ifl)
#--- element stiffness matrix  se
            se = se + sip
        return se
#--- end of elstiff
#-----  stiffness matrix -----
xni = integ(xi)
for n in range(0,ne):
    d = dmat(n,mat,pm)
    ifl = 2
    se = elstiff(n,x,noc,d,mat,pm,dt,qt,xi,xni)
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
#----- reaction calculation -----
for i in range(0,nd):
    n = int(nu[i]-1)
    u[i] = cnst * (u[i] - f[n])
results1 = results1 + "node# x-displ   y-displ   z-displ\n"
for i in range(0,nn):
    ii = ndn*i
    results1 = results1 + str(i+1) + " "
    for j in range(0,ndn):
        results1 = results1 + str("%12.4e" % f[ii+j]) +" "
    results1 = results1 + "\n"
d = dmat(0,mat,pm)
#----- stess Evaluation
results2 = results2 + "vonMises stresses at integration points\n"
results2 = "Elem#   Int1   Int2   Int3   Int4   Int5   Int6   Int7   Int8\n"
for n in range(0,ne):
    for i in range(0,nen):
        iin = 3 * (noc[n,i]-1)
        ii = 3 * i
        for j in range(0,3):
            qt[ii + j] = f[iin + j]
            d = dmat(n,mat,pm)
    results2 = results2 + str(n + 1)
    for ip in range(0,8):
        ifl = 1
        db = dbse(n,ip,x,noc,d,mat,pm,dt,qt,xi,xni,ifl)
#--- stress calculation str = db * qt
        st = np.matmul(db,qt)
        m = mat[n] - 1
        cal = dt[n] * pm[m][2]
        for i in range(0,6):
            st[i] = st[i] - cal * (d[i][0] + d[i][1] + d[i][2])
        siv1 = st[0] + st[1] + st[2]
        siv2 = st[0] * st[1] + st[1] * st[2] + st[2] * st[0]
        siv2 = siv2 - st[3]*st[3] - st[4]*st[4] - st[5]*st[5]
        sv = math.sqrt(siv1 * siv1 - 3 * siv2)
        results2 = results2 + str("%10.4f" %sv)
    results2 = results2 + "\n"
results1 = results1 + results2 + "dof#   Reactions\n"
for i in range(0,nd):
    results1 = results1 + str("%4d"% nu[i]) +" "+ str("%12.4e"% u[i]) + "\n"
print(results1)
