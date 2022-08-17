#=====       Program GENEIGEN          =====
#      Geneeralized Egigenvalue Method
#     T.R. Chandrupatl & A.D. Belegundu
#===========================================
import numpy as np
import math
file1 = "eigen.inp"
f = open(file1, "r")
li=f.read().splitlines()
tmp=li[2].split()
nq = int(tmp[0])
nbw = int(tmp[1])
s = np.zeros(shape = (nq, nq), dtype = float)
gm = np.zeros(shape = (nq, nq), dtype = float)
d = np.zeros(shape = (nq), dtype = float)
b = np.zeros(shape = (nq-1), dtype = float)
evc = np.zeros(shape = (nq,nq), dtype = float)
evl = np.zeros(shape = (nq), dtype = float)
nord = np.zeros(shape = (nq), dtype = int)

dummy = "Program DENEIGEN for eigen solution\n"
tol = .000001
#---read s and gm into nqxnq matricesfrom file
ptr = 3
for i in range(0,nq):
    ptr = ptr + 1
    for jn in range(0,nbw):
        tmp = li[ptr].split()
        c = float(tmp[jn])
        j = i + jn
        if j < nq:
            s[i][j] = c
            s[j][i] = c
ptr = ptr + 1
for i in range(0,nq):
    ptr = ptr + 1
    for jn in range(0,nbw):
        tmp = li[ptr].split()
        c = float(tmp[jn])
        j = i + jn
        if j < nq:
            gm[i][j] = c
            gm[j][i] = c

def chol(a,n):
#Cholesky Factorization of matrix a
#----- L into lower left triangle of a
    for k in range(0,n):
        a[k][k] = math.sqrt(a[k][k])
        for i in range(k+1, n):
            a[i][k] = a[i][k] / a[k][k]
        for j in range(k+1, n):
            for i in range(j, n):
                a[i][j] = a[i][j] - a[i][k] * a[j][k]
    print(a)
    return a
#--- end of Cholesky()
gm = chol(gm,nq)
def updatestiff(s,gm,n):
#----- update of stiffness matrix - standard form ax=(lambda)x
#--- forward substitution I  (invL)*s
    for j in range(0,n):
        s[0][j] = s[0][j] / gm[0][0]
        for i in range(1, n):
            for k in range(0, i):
                s[i][j] = s[i][j] - gm[i][k] * s[k][j]
            s[i][j] = s[i][j] / gm[i][i]
#--- forward substitution II   (invL)*s*(invL)'
    for j in range(0, n):
        s[j][0] = s[j][0] / gm[0][0]
        for i in range(1,n):
            for k in range(0, i):
                s[j][i] = s[j][i] - gm[i][k] * s[j][k]
            s[j][i] = s[j][i] / gm[i][i]
    return s
#--- end of updatestiff()
s = updatestiff(s,gm,nq)
def tridiag(s,d,b,n):
    #----- tri-diagonalize d() diagonal, b() sub-diagonal
    #----- s() has the rotation matrix
    for i in range(0, n-2):
        aa = 0
        for j in range (i + 1, n):
            aa = aa + s[j][i] * s[j][i]
        aa = math.sqrt(aa)
        ww = 2 * aa * (aa + abs(s[i + 1][i]))
        ww = math.sqrt(ww)
        ia = 1
        if s[i + 1][i] < 1:
            ia = -1
        #----- diagonal and next to diagonal term
        d[i] = s[i][i]
        b[i] = -ia * aa
        #----- unit vector w() in column i from row i+1 to n
        for j in range (i + 1, n):
            s[j][i] = s[j][i] / ww
        s[i + 1][i] = s[i + 1][i] + ia * aa / ww
        #----- w'a in row i from col i+1 to n
        bet = 0
        for j in range (i+1, n):
            s[i][j] = 0
            for k in range(i + 1, n):
                s[i][j] = s[i][j] + s[k][i] * s[k][j]
            bet = bet + s[i][j] * s[j][i]
        #----- modified s()
        for j in range(i + 1, n):
            for k in range(i + 1, n):
                c1 = - 2 * s[j][i] * s[i][k] - 2 * s[i][j] * s[k][i]
                c1 = c1 + 4 * bet * s[k][i] * s[j][i]
                s[j][k] = s[j][k] + c1
    d[n - 2] = s[n - 2][n - 2]
    b[n - 2] = s[n - 2][n - 1]
    d[n - 1] = s[n - 1][n - 1]
    s[n - 2][n - 2] = 1
    s[n - 1][n - 1] = 1
    s[n - 2][n - 1] = 0
    s[n - 1][n - 2] = 0
    #----- now create the q matrix in s()
    for i in range(0, n - 2):
        ii = n - i - 3
        s[ii][ii] = 1
        for j in range(1, i + 3):
            ij = ii + j
            c1 = 0
            for k in range(1, i + 3):
                ik = ii + k
                c1 = c1 + s[ik][ij] * s[ik][ii]
            for k in range(1, i + 3):
                ik = ii + k
                s[ik][ij] = s[ik][ij] - 2 * c1 * s[ik][ii]
        for j in range(1, i + 3):
            ij = ii + j
            s[ii][ij] = 0
            s[ij][ii] = 0
    return s
#---end of tridiag()
s = tridiag(s,d,b,nq)
def eigentd(s,d,b,n):
    iter = 0
    m = n
    while m > 1:
        iter = iter + 1
        dd = 0.5 * (d[m - 2] - d[m - 1])
        bb = b[m - 2] * b[m - 2]
        p = 1
        if dd < 1:
            p = -1
        bot = dd + p * math.sqrt(dd * dd + bb)
        p = d[0] - d[m - 1] + bb / bot
        x = b[0]
        for i in range(0, m-1):
            pp = math.sqrt(p * p + x * x)
            cs = -p / pp
            sn = x / pp
            if i > 0:
                b[i - 1] = cs * b[i - 1] - sn * x
            a1 = d[i]
            a2 = d[i + 1]
            b1 = b[i]
            d[i] = a1 * cs * cs - 2 * b1 * cs * sn + a2 * sn * sn
            b[i] = (a1 - a2) * cs * sn + b1 * (cs * cs - sn * sn)
            d[i + 1] = a1 * sn * sn + 2 * b1 * cs * sn + a2 * cs * cs
            # ----- update q()
            for k in range(0, n):
                a1 = s[k][i]
                a2 = s[k][i + 1]
                s[k][i] = cs * a1 - sn * a2
                s[k][i + 1] = sn * a1 + cs * a2
            if i == m - 2:
                break
            x = -b[i + 1] * sn
            b[i + 1] = b[i + 1] * cs
            p = b[i]
        while m > 1 and abs(b[m - 2]) < 0.000001:
            m = m - 1
    m = m - 1
    return d
#--- end of eigentd()
d = eigentd(s,d,b,nq)
def eigenvec(s,gm,n):
    # --- backsubstitution --- */
    for j in range(0, n):
        s[n - 1][j] = s[n - 1][j] / gm[n - 1][n - 1]
        for i in range(n-2,-1,-1):
            for k in range(n-1, i, -1):
                s[i][j] = s[i][j] - gm[k][i] * s[k][j]
            s[i][j] = s[i][j] / gm[i][i]
    return s
#--- end eigenvec()
s = eigenvec(s,gm,nq)
for i in range(0,nq):
    nord[i] = i
#--- arrange in ascending order of eigenvalues
for i in range(0, nq):
    ii = nord[i]
    i1 = ii
    c1 = d[ii]
    j1 = i
    for j in range(i, nq):
        ij = nord[j]
        if c1 > d[ij]:
            c1 = d[ij]
            i1 = ij
            j1 = j
    if i1 != ii:
        nord[i] = i1
        nord[j1] = ii
dummy = dummy + "Results for data in file  " + file1 + "\n"
if nsw > nswmax:
    dummy = dummy + "No convergence in " + str(nswmax) + "  sweeps\n"
else:
    for i in range(0,nq):
        ii = nord[i]
        iii = i + 1
        dummy = dummy + "eigenval# = " + str("%2d"% iii) + "\n"
        " value = "
        dummy = dummy + " value = "+ str("%12.4e"% d[ii]) + "\n"
        omega = math.sqrt(d[ii])
        freq = 0.5 * omega / math.pi
        dummy = dummy + "omega = " + str("%12.4e"% omega) + "\n"
        dummy = dummy + "freq Hz = " + str("%12.4e"% freq) + "\n"
        dummy = dummy + "eigenvector\n"
        for j in range (0,nq):
            dummy = dummy + str("%12.4e"% s[j][ii]) + " "
        dummy = dummy + "\n"
print(dummy)

