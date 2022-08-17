#Program CST for constant strain triangle element
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
file1 = "cstkm.inp"
#Set lc = 1 for plane stess; 2 for plane strain
lc = 1
#Set ipl = 1 for for vonMises stress; 2 for max shear stress
ipl = 1
f = open(file1, "r")
li=f.read().splitlines()
f.close
dummy = ""
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
th = np.zeros((ne))
mat = np.zeros((ne),dtype = int)
dt = np.zeros((ne))
pm = np.zeros((nm,npr))
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd))
mpc = np.zeros((nmpc,2),dtype = int)
bt = np.zeros((nmpc,3))
se = np.zeros((6,6))
em = np.zeros((6,6))
tml = np.zeros(6)
d = np.zeros((3,3))
b = np.zeros((3,6))
db = np.zeros((3,6))
q = np.zeros(6)
st = np.zeros(3)
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
    th[n-1] = float(tmp[nen+2])
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
gm = np.zeros((nq,nbw))
#--- d-matrix
def dmat(n,lc,mat,pm):
#--- d-matrix
    m = mat[n]-1
    e = pm[m,0]
    pnu = pm[m,1]
    if lc == 1:
        #--- plane stess
        c1 = e / (1 - pnu**2)
        c2 = c1 * pnu
    else:
        #--- plane strain
        c = e / ((1 + pnu) * (1 - 2 * pnu))
        c1 = c * (1 - pnu)
        c2 = c * pnu
    c3 = .5 * e / (1 + pnu)
    d[0,0] = c1
    d[0,1] = c2
    d[1,0] = c2
    d[1,1] = c1
    d[2,2] = c3
    return d
#function dbse gives db with ifl = 1, se  with ifl = 2
def dbse(n,x,noc,d,th,mat,pm,dt,tml,lc,ifl):
#--- stain-displacement matrix b()
    i1 = noc[n, 0]-1
    i2 = noc[n, 1]-1
    i3 = noc[n, 2]-1
    x1 = x[i1, 0]
    y1 = x[i1, 1]
    x2 = x[i2, 0]
    y2 = x[i2, 1]
    x3 = x[i3, 0]
    y3 = x[i3, 1]
    x21 = x2 - x1
    x32 = x3 - x2
    x13 = x1 - x3
    y12 = y1 - y2
    y23 = y2 - y3
    y31 = y3 - y1
    dj = x13 * y23 - x32 * y31   #dj is determinant of jacobian
#--- definition of b() matrix
    b[0, 0] = y23 / dj
    b[0, 1] = 0
    b[0, 2] = y31 / dj
    b[0, 3] = 0
    b[0, 4] = y12 / dj
    b[0, 5] = 0
    b[1, 0] = 0
    b[1, 1] = x32 / dj
    b[1, 2] = 0
    b[1, 3] = x13 / dj
    b[1, 4] = 0
    b[1, 5] = x21 / dj
    b[2, 0] = x32 / dj
    b[2, 1] = y23 / dj
    b[2, 2] = x13 / dj
    b[2, 3] = y31 / dj
    b[2, 4] = x21 / dj
    b[2, 5] = y12 / dj
#--- db matrix db = d*b
    db = np.dot(d,b)
    if ifl < 2:
        return db 
#--- temperature load vector
    m = mat[n]-1
    pnu = pm[m,1]
    al = pm[m,2]
    c = al * dt[n]
    if lc == 2 :
        c = c * (1 + pnu)
        for i in range(0,6):
           tml[i] = .5 * c * th[n] * abs(dj) * (db[0, i] + db[1, i])
#--- element stiffness
    se = 0.5*th[n]*abs(dj)*np.dot(np.transpose(b),db)
    return se
#-----  stiffness matrix -----
for n in range(0,ne):
    d = dmat(n,lc,mat,pm)
    ifl = 2
    se = dbse(n,x,noc,d,th,mat,pm,dt,tml,lc,ifl)
#--- Element Mass  EM()
    i1 = noc[n, 0]-1
    i2 = noc[n, 1]-1
    i3 = noc[n, 2]-1
    x1 = x[i1, 0]
    y1 = x[i1, 1]
    x2 = x[i2, 0]
    y2 = x[i2, 1]
    x3 = x[i3, 0]
    y3 = x[i3, 1]
    x32 = x3 - x2
    x13 = x1 - x3
    y23 = y2 - y3
    y31 = y3 - y1
    dj = x13 * y23 - x32 * y31
    m = mat[n] - 1
    rho = pm[m][3]
    cm = rho * th[n] * 0.5 * abs(dj) / 12
    for i in range(0, 6):
        for j in range(0, 6):
            em[i][j] = 0
    #--- Non-zero elements of mass matrix are defined
    em[0][0] = 2 * cm
    em[0][2] = cm
    em[0][4] = cm
    em[1][1] = 2 * cm
    em[1][3] = cm
    em[1][5] = cm
    em[2][0] = cm
    em[2][2] = 2 * cm
    em[2][4] = cm
    em[3][1] = cm
    em[3][3] = 2 * cm
    em[3][5] = cm
    em[4][0] = cm
    em[4][2] = cm
    em[4][4] = 2 * cm
    em[5][1] = cm
    em[5][3] = cm
    em[5][5] = 2 * cm    
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
                       gm[nr,nc] = gm[nr,nc] + em[i,j]
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
dummy = "STIFFNESS AND MASS USING CSTKM\n"
dummy = dummy + "Example" + "\n"
dummy=dummy +"numdof  bandwidth" +"\n"
dummy = dummy + str(nq) + "   " + str(nbw) +"\n"
dummy=dummy +"banded stiffness matrix" +"\n"
for i in range(0, nq):
   for j in range(0, nbw):
       c = round(s[i,j]*100000)/100000
       dummy = dummy + str(c)+ "  "
   dummy = dummy + "\n"
dummy = dummy + "banded mass matrix\n"
for i in range(0, nq):
    for j in range(0, nbw):
        c = round(gm[i,j]*100000)/100000
        dummy = dummy + str(c) + "  "
    dummy = dummy + "\n"
dummy = dummy + "starting vector for inverse iteration\n"
for i in range(0, nq):
   dummy = dummy + "1 "
print(dummy)