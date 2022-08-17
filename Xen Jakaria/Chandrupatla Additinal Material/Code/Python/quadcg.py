#Program QUADCG (Conjugate Gradient Method)
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
import math
file1 = "quad.inp"
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
x = np.zeros((nn,ndim),dtype = float)
noc = np.zeros((ne,nen),dtype = int)
f = np.zeros((nq),dtype = float)
th = np.zeros((ne),dtype = float)
mat = np.zeros((ne),dtype = int)
dt = np.zeros((ne),dtype = float)
pm = np.zeros((nm,npr),dtype = float)
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd),dtype = float)
mpc = np.zeros((nmpc,2),dtype = int)
bt = np.zeros((nmpc,3),dtype = float)
se = np.zeros((8,8),dtype = float)
s = np.zeros((ne,8,8), dtype = float)
tml = np.zeros((8),dtype = float)
d = np.zeros((3,3),dtype = float)
b = np.zeros((3,8),dtype = float)
db = np.zeros((3,8),dtype = float)
qe = np.zeros((8),dtype = float)
st = np.zeros((3),dtype = float)
q = np.zeros((nq),dtype = float)
dd = np.zeros((nq),dtype = float)
ad = np.zeros((nq),dtype = float)
gg = np.zeros((nq),dtype = float)
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
    th[n-1] = float(tmp[nen+2])
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
    d = np.zeros((3,3))
    d[0,0] = c1
    d[0,1] = c2
    d[1,0] = c2
    d[1,1] = c1
    d[2,2] = c3
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
def dbse(n,x,noc,d,th,mat,pm,dt,tml,xi,eta,lc,ifl):
#-------  db()  matrix  ------
#--- nodal coordinates
    thick = th[n]
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
#--- b(3,8) matrix relates strains to q
    b = np.matmul(a,g)
    db = np.zeros((3,8), dtype = float)
#--- db(3,8) is stress-displ matrix at integration point
    db = np.matmul(d,b)
    if ifl < 2:
        return db
        print(db)
#sip is stiffness evaluated integration point
    sip = np.zeros((8,8), dtype = float)
    sip = dj*thick*np.matmul(np.transpose(b),db)
#--- determine temperature load tl
    m = mat[n] - 1
    c = pm[m, 2] * dt[n]
    if lc == 2:
        c = (1 + pm[m, 1]) * c
    for i in range(0,8):
        tml[i] = tml[i] + thick * dj * c * (db[0, i] + db[1, i])
    return sip
def elstiff(n,x,noc,d,th,mat,pm,dt,tml,xni,lc):
#--------  Element Stiffness and Temperature Load  -----
    se = np.zeros((8,8), dtype = float)
    for i in range(0,8):
        tml[i] = 0
        d = dmat(n,lc,mat,pm)
#--- weight factor is one
#--- loop on integration points
        for ip in range(0,4):
            xi = xni[ip, 0]
            eta = xni[ip, 1]
            ifl = 2
            sip = dbse(n,x,noc,d,th,mat,pm,dt,tml,xi,eta,lc,ifl)
#--- element stiffness matrix  se
            se = se + sip
        return se
#--End of  Element Stiffness 


#-----  stiffness matrix -----
for n in range(0,ne):
    d = dmat(n,lc,mat,pm)
    ifl = 2
    se = elstiff(n,x,noc,d,th,mat,pm,dt,tml,xni,lc)
    for i in range (0,8):
        for j in range (0,8):
            s[n,i,j] = se[i,j]
    for ii in range(0,nen):
        nrt = ndn * (noc[n, ii] - 1)
        for it in range (0,ndn):
            nr = nrt + it
            i = ndn * ii + it
            f[nr] = f[nr] + tml[i]
            gg[nr] = gg[nr] + se[i,i]
#---End of stiffness
#----- decide penalty parameter cnst -----
cnst = 0
for i in range(0,nq):
    if cnst < gg[i]:
        cnst = gg[i]
cnst = cnst * 10000
#----- Modify right hand side F() for Boundary Conditions -----
#--- displacement bc ---
for i in range(0,nd):
    n = int(nu[i]-1)
    f[n] = f[n] + cnst * u[i]
#--- multi-point constraints ---
for i in range(0,nmpc):
    i1 = mpc[i, 0]
    i2 = mpc[i, 1]
    f[i1] = f[i1] + cnst * bt[i,0] * bt[i,2]
    f[i2] = f[i2] + cnst * bt[i,1] * bt[i,2]

#Function conjugate gradient solver
def cgsolve(nq,ne,nd,s,f,q,gg,dd,noc,ad,mpc,bt,nmpc):
#----- conjugate gradient method starts here
    gg1 = 0
    for i in range(0,nq):
        gg[i] = -f[i]
        dd[i] = f[i]
        q[i] = 0
        gg1 = gg1 + gg[i] * gg[i]
#-----  iteration loop
    iter = 0
    ifl = 2
    while ifl > 1:
        iter = iter + 1
#=====  element loop  =====
        for n in range(0, ne):
            for i in range(0,4):
                igt = 2 * (noc[n, i] - 1)
                ilt = 2 * i
                for ii in range(0,2):
                    ig = igt + ii
                    il = ilt + ii
                    for j in range(0,4):
                       jgt = 2 * (noc[n, j] - 1)
                       jlt = 2 * j
                       for jj in range(0,2):
                           jg = jgt + jj
                           jl = jlt + jj
                           ad[ig] = ad[ig] + s[n,il,jl] * dd[jg]
#--- displacement bc ---
        for i in range(0, nd):
            n = nu[i]-1
            ad[n] = ad[n] + cnst * dd[n]
#--- multi-point constraints ---
        for i in range(0, nmpc):
            i1 = mpc[i, 1]-1
            i2 = mpc[i, 2]-1
            c = bt[i, 0] * dd[i1] + bt[i, 1] * dd[i2]
            ad[i1] = ad[i1] + cnst * bt[i, 0] * c
            ad[i2] = ad[i2] + cnst * bt[i, 1] * c
        dad = 0
        for i in range(0, nq):
            dad = dad + dd[i] * ad[i]
        al = gg1 / dad
        gg2 = 0
        for i in range(0, nq):
            gg[i] = gg[i] + al * ad[i]
            q[i] = q[i] + al * dd[i]
            gg2 = gg2 + gg[i] * gg[i]
# condition for exit while
        if gg2 < .00000001:
            ifl = 0
            break
        bta = gg2 / gg1
        gg1 = gg2
        for i in range(0, nq):
            dd[i] = -gg[i] + bta * dd[i]
        for i in range(0, nq):
            ad[i] = 0
    return q

q = cgsolve(nq,ne,nd,s,f,q,gg,dd,noc,ad,mpc,bt,nmpc)
#----- reaction calculation -----
for i in range(0,nd):
    n = int(nu[i]-1)
    u[i] = cnst * (u[i] - q[n])
results1 = results1 + "node# x-displ   y-displ\n"
for i in range(0,nn):
    ii = ndn*i
    results1 = results1 + str(i+1) + " "
    for j in range(0,ndn):
        results1 = results1 + str("%12.4e" % q[ii+j]) +" "
    results1 = results1 + "\n"
#----- stess Evaluation
results2 = "Elem#  Integ1  Integ2  Integ3  Integ4  "
if ipl > 1:
    results2 = results2 + "max shear stresses\n"
else:
    results2 = results2 + "vonMises stresses\n"
for n in range(0,ne):
    for i in range(0,nen):
        ii = noc[n,i]-1
        qe[2*i] = q[2*ii]
        qe[2*i+1] = q[2*ii+1]
        d = dmat(n,lc,mat,pm)

    for ip in range(0,4):
        ifl = 1
        xi = xni[ip, 0]
        eta = xni[ip, 1]        
        db = dbse(n,x,noc,d,th,mat,pm,dt,tml,xi,eta,lc,ifl)
        st = np.matmul(db,qe)
        m = mat[n]-1
        c1 = pm[m,2] * dt[n]
        if lc == 2:
            c1 = c1 * (1 + pm[m,1]) 
        for j in range(0,3):
            st[j] = st[j] - c1 * (d[j,0] + d[j,1])
#--- von mises stress at integration point
        c = 0
        pnu = pm[mat[n]-1,1]
        if lc > 1:
            c = pnu * (st[0] + st[1])
        c1 = (st[0] - st[1])**2 + (st[1] - c)**2 + (c - st[0])**2
        sv = math.sqrt(.5 * c1 + 3 * st[2]**2)
#--- maximum shear stress r
        r = math.sqrt(.25*(st[0]-st[1])**2 + st[2]**2)
        if ifl > 1:
            results2 = results2 + str(n+1) + "  "+str("%10.4f" %r)
        else:
            results2 = results2 + str(n+1) + "  "+str("%10.4f" %sv)
    results2 = results2 + "\n"
results1 = results1 + results2 + "dof#   Reactions\n"
for i in range(0,nd):
    results1 = results1 + str("%4d"% nu[i]) +" "+ str("%12.4e"% u[i]) + "\n"
print(results1)



