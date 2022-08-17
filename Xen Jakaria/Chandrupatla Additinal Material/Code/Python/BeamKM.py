#Program BEAM
#T.R.Chandrupatla and A.D.Belegundu
import numpy as np
file1 = "beamkm.inp"
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
x = np.zeros((nn))
noc = np.zeros((ne,nen),dtype = int)
f = np.zeros((nq))
smi = np.zeros((ne))
area = np.zeros((ne))
mat = np.zeros((ne),dtype = int)
pm = np.zeros((nm,npr))
nu = np.zeros((nd), dtype = int)
u = np.zeros((nd))
mpc = np.zeros((nmpc,2),dtype = int)
bt = np.zeros((nmpc,3))
se = np.zeros((4,4),dtype = float)
em = np.zeros((4,4),dtype = float)
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
    smi[n-1] = float(tmp[4])
    area[n-1] = float(tmp[5])
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
gm = np.zeros((nq,nbw))
#-----  stiffness matrix -----
for n in range(0,ne):
    n1 = noc[n,0]-1
    n2 = noc[n,1]-1
    m = mat[n]-1
    el = abs(x[n1] - x[n2])
    eil = pm[m, 0] * smi[n] / el**3
    se[0,0] = 12 * eil
    se[0,1] = eil * 6 * el
    se[0,2] = -12 * eil
    se[0,3] = eil * 6 * el
    se[1,0] = se[0,1]
    se[1,1] = eil * 4 * el * el
    se[1,2] = -eil * 6 * el
    se[1,3] = eil * 2 * el * el
    se[2,0] = se[0,2]
    se[2,1] = se[1,2]
    se[2,2] = eil * 12
    se[2,3] = -eil * 6 * el
    se[3,0] = se[0,3]
    se[3,1] = se[1,3]
    se[3,2] = se[2,3]
    se[3,3] = eil * 4 * el * el
    #--- Element Mass
    rho = pm[m][1]
    c1 = rho * area[n] * el / 420
    em[0][0] = 156 * c1
    em[0][1] = 22 * el * c1
    em[0][2] = 54 * c1
    em[0][3] = -13 * el * c1
    em[1][0] = em[0][1]
    em[1][1] = 4 * el * el * c1
    em[1][2] = 13 * el * c1
    em[1][3] = -3 * el * el * c1
    em[2][0] = em[0][2]
    em[2][1] = em[1][2]
    em[2][2] = 156 * c1
    em[2][3] = -22 * el * c1
    em[3][0] = em[0][3]
    em[3][1] = em[1][3]
    em[3][2] = em[2][3]
    em[3][3] = 4 * el * el * c1
    #global stiffness and mass matrices       
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
    f[i1] = f[i1] + cnst * bt[i,0] * bt[i,2]
    f[i2] = f[i2] + cnst * bt[i,1] * bt[i,2]
dummy = "STIFFNESS AND MASS FROM BEAMKM\n"
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
