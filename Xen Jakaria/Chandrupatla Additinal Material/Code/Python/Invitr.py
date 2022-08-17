#=====         Program INVITR        =====
#Inverse Iteration method for eigenvalues
#   T.R. Chandrupatl & A.D. Belegundu
#=========================================
import numpy as np
import math
file1 = "eigen.inp"
f = open(file1, "r")
li=f.read().splitlines()
tmp=li[2].split()
nq = int(tmp[0])
nbw = int(tmp[1])
s = np.zeros(shape = (nq, nbw), dtype = float)
gm = np.zeros(shape = (nq, nbw), dtype = float)
ev1 = np.zeros(shape = (nq), dtype = float)
ev2 = np.zeros(shape = (nq), dtype = float)
evt = np.zeros(shape = (nq), dtype = float)
evs = np.zeros(shape = (nq), dtype = float)
st = np.zeros(shape = (nq), dtype = float)
dummy = "Program INVITR for eigen solution\n"
#---nev is number of eigenvalues desired
nev = 4
evc = np.zeros(shape = (nev,nq), dtype = float)
evl = np.zeros(shape = (nev), dtype = float)
niter = np.zeros((nev), dtype = int)
tol = .000001
itmax = 50
#---change shift value as needed
sh = 0
#---read s and gm from file
ptr = 3
for i in range(0,nq):
    ptr = ptr + 1
    for j in range(0,nbw):
        tmp = li[ptr].split()
        s[i,j] = float(tmp[j])
ptr = ptr + 1
for i in range(0,nq):
    ptr = ptr + 1
    for j in range(0,nbw):
        tmp = li[ptr].split()
        gm[i,j] = float(tmp[j])
ptr = ptr + 2
tmp = li[ptr].split()
for i in range(0,nq):
    st[i] =tmp[i]
#bansolveone turns a sym banded nXnbw to upper triangular matrix
def bansolveone(a,n,nbw):
#-----  gauss elimination ldu approach (for symmetric banded matrices)
#----- stiffness reduction to upper triangular form
    for k in range (0,n):
        nk = n - k + 1
        if nk > nbw:
            nk = nbw
        for i in range(2,nk+1):
            c1 = a[k-1][i-1] / a[k-1][0]
            i1 = k + i - 2
            for j in range (i,nk + 1):
                j1 = j - i
                a[i1][j1] = a[i1][j1] - c1 * a[k-1][j-1]
    return a
#---end of BanSolveOne()
def bansolvetwo(a,b,n,nbw):
#bansolvetwo for reduction of right hand side b
#with reduced n x nbw upper triangular matrix a
#for multiple righthand sides
#----- reduction of the right hand side
    for k in range(1,n):
        nk = n - k + 1
        if nk > nbw:
            nk = nbw
        for i in range(2, nk + 1):
            i1 = k + i - 1
            c1 = 1 / a[k-1][0]
            b[i1-1] = b[i1-1] - c1 * a[k-1][i-1] * b[k-1]
#----- backsubstitution
    b[n-1] = b[n-1] / a[nq-1][0]
    for ii in range(1,n):
        i = n - ii
        c1 = 1 / a[i-1][0]
        ni = n - i + 1
        if ni > nbw:
            ni = nbw
        b[i-1] = c1 * b[i-1]
        for k in range(2, ni + 1):
           b[i-1] = b[i-1] - c1 * a[i-1][k-1] * b[i + k - 2]
    return b
s = bansolveone(s,nq,nbw)
#Inverse iteration routine starts here
#--- bansolvetwo ends here
#ev1 is the starting vector st
#nv is number of eigenvalues desired
itmax = 50
nev1 = nev
for nv in range(1,nev+1):
    ifl = 1
    el2 = 0
    iter = 0
    for i in range(0,nq):
        ev1[i] = st[i]
    while ifl < 2:
        el1 = el2
        iter = iter + 1
        if iter > itmax:
            dummy = "no convergence for eigenvalue# " + str(nv) + "\n"
            nev1 = nv - 1
            break
        if nv > 1:
#----  starting vector orthogonal to
#----       evaluated vectors
            for i in range(1,nv):  
                cv = 0
                for k in range(1, nq+1):  
                    ka = k - nbw + 1
                    kz = k + nbw - 1
                    if ka < 1: 
                        ka = 1
                    if kz > nq:
                        kz = nq
                    for l in range(ka,kz+1):  
                        if l < k:
                            k1 = l - 1
                            l1 = k - l
                        else:
                            k1 = k - 1
                            l1 = l - k 
                        cv = cv + evs[k-1] * gm[k1][l1] * evc[i-1][l-1]
                for k in range(0, nq):  
                    ev1[k] = ev1[k] - cv * evc[i-1][k]
        for i in range(1,nq+1):   
            ia = i - nbw + 1
            iz = i + nbw - 1
            evt[i-1] = 0
            if ia < 1:
                ia = 1
            if iz > nq:
                iz = nq 
            for k in range(ia,iz+1):
                if k < i:
                    i1 = k - 1
                    k1 = i - k 
                else:
                    i1 = i - 1
                    k1 = k - i
                evt[i-1] = evt[i-1] + gm[i1][k1] * ev1[k-1]
            ev2[i-1] = evt[i-1]
        ev2 = bansolvetwo(s,ev2,nq,nbw)
        c1 = 0
        c2 = 0
        for i in range(0,nq):
            c1 = c1 + ev2[i] * evt[i]
        for i in range(1,nq+1):
            ia = i - nbw + 1
            iz = i + nbw - 1
            evt[i-1] = 0
            if ia < 1:
                ia = 1
            if iz > nq:
                iz = nq 
            for k in range(ia,iz + 1):
                if k < i:
                    i1 = k - 1
                    k1 = i - k
                else:
                    i1 = i - 1
                    k1 = k - i
                evt[i-1] = evt[i-1] + gm[i1][k1] * ev2[k-1]
        for i in range(0,nq):
            c2 = c2 + ev2[i] * evt[i]
        el2 = c1 / c2
        c2 = math.sqrt(c2)
        for i in range(0,nq):
            ev1[i] = ev2[i] / c2
            evs[i] = ev1[i]
        if abs(el2 - el1) / abs(el2) < tol:
            ifl = 3
    for i in range(0,nq):
        evc[nv-1][i] = ev1[i]
    niter[nv-1] = iter
    el2 = el2 + sh
    evl[nv-1] = el2
#invitersiter ends here
dummy = dummy + "Results for data in file  " + file1 + "\n"
if nev1 < nev:
    dummy = dummy + "Convergence of " + str(nev1) + "  eigenvalues only\n"
for nv in range(0,nev):
     nv1 = nv + 1
     dummy = dummy + "eigenval# = " + str("%2d"% nv1) + " value = "
     dummy = dummy + str("%12.4e"% evl[nv]) + "  iter# = " + str(niter[nv]) + "\n"
     omega = math.sqrt(evl[nv])
     freq = 0.5 * omega / math.pi
     dummy = dummy + "omega = " + str("%12.4e"% omega) + "\n"
     dummy = dummy + "freq Hz = " + str("%12.4e"% freq) + "\n"
     dummy = dummy + "eigenvector\n"
     for i in range (0,nq):
        dummy = dummy + str("%12.4e"% evc[nv][i]) + " "
     dummy = dummy + "\n"
print(dummy)