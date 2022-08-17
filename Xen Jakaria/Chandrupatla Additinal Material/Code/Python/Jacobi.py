#=====              Program JACOBI             =====
# Jacobi Method for All Eigenvalues and Eigenvectors
#         T.R. Chandrupatl & A.D. Belegundu
#===================================================
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
evc = np.zeros(shape = (nq,nq), dtype = float)
evl = np.zeros(shape = (nq), dtype = float)
nord = np.zeros(shape = (nq), dtype = int)

dummy = "Program JACOBI for eigen solution\n"
tol = .000001
nswmax = 50
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
#--- jacobieigen():
#----- initialize nord() and evc() as identity matrix
for i in range(0, nq):
    nord[i] = i
    evc[i][i] = 1.
c1 = s[0][0]
c2 = gm[0][0]
for i in range(0, nq):
    if c1 > s[i][i]:
        c1 = s[i][i]
    if c2 < gm[i][i]:
        c2 = gm[i][i]
tols = tol * c1
tolm = tol * c2
k1 = 1
i1 = 1
ifl = 1
nsw = 0
while ifl == 1:
    nsw = nsw + 1
    if nsw > nswmax:
        #--- no convergence
        break
    for k in range(k1, nq):
        for i in range (i1, k+1):
            ii = i - 1
            j = nq - k + i
            jj = j - 1
            if abs(s[ii][jj]) > tols or abs(gm[ii][jj]) > tolm:
                aa = s[ii][ii] * gm[ii][jj] - gm[ii][ii] * s[ii][jj]
                bb = s[jj][jj] * gm[ii][jj] - gm[jj][jj] * s[ii][jj]
                cc = s[ii][ii] * gm[jj][jj] - gm[ii][ii] * s[jj][jj]
                cab = 0.25 * cc * cc + aa * bb
                if cab < 0:
                    #square root of negative term -- check matrices
                    break
                if aa == 0:
                    bet = 0
                    alp = -s[ii][jj] / s[ii][ii]
                elif bb == 0:
                    alp = 0
                    bet = -s[ii][jj] / s[jj][jj]
                else:
                    sqc = math.sqrt(cab)
                    if cc < 0:
                        sqc = -sqc
                    alp = (-0.5 * cc + sqc) / aa
                    bet = -aa * alp / bb
#----- only upper triangular part is used in diagonalization
                if i > 1:
                    for n in range(1,i):
                        si = s[n-1][ii]
                        sj = s[n-1][jj]
                        emi = gm[n-1][ii]
                        emj = gm[n-1][jj]
                        s[n-1][ii] = si + bet * sj
                        s[n-1][jj] = sj + alp * si
                        gm[n-1][ii] = emi + bet * emj
                        gm[n-1][jj] = emj + alp * emi
                if j < nq:
                    for n in range(j+1, nq+1):
                        si = s[ii][n-1]
                        sj = s[jj][n-1]
                        emi = gm[ii][n-1]
                        emj = gm[jj][n-1]
                        s[ii][n-1] = si + bet * sj
                        s[jj][n-1] = sj + alp * si
                        gm[ii][n-1] = emi + bet * emj
                        gm[jj][n-1] = emj + alp * emi
                if i < j:
                    for n in range (i+1, j):
                        si = s[ii][n-1]
                        sj = s[n-1][jj]
                        emi = gm[ii][n-1]
                        emj = gm[n-1][jj]
                        s[ii][n-1] = si + bet * sj
                        s[n-1][jj] = sj + alp * si
                        gm[ii][n-1] = emi + bet * emj
                        gm[n-1][jj] = emj + alp * emi
                sii = s[ii][ii]
                sij = s[ii][jj]
                sjj = s[jj][jj]
                s[ii][jj] = 0
                s[ii][ii] = sii + 2 * bet * sij + bet * bet * sjj
                s[jj][jj] = sjj + 2 * alp * sij + alp * alp * sii
                eii = gm[ii][ii]
                eij = gm[ii][jj]
                ejj = gm[jj][jj]
                gm[ii][jj] = 0
                gm[ii][ii] = eii + 2 * bet * eij + bet * bet * ejj
                gm[jj][jj] = ejj + 2 * alp * eij + alp * alp * eii
#---- eigenvectors -----
                for n in range(0, nq):
                    evi = evc[ii][n]
                    evj = evc[jj][n]
                    evc[ii][n] = evi + bet * evj
                    evc[jj][n] = evj + alp * evi
    for k in range(1,nq):
        for i in range(1,k+1):
            ii = i - 1
            j = nq - k + i - 1
            ifl = 0
            if abs(s[ii][j]) > tols or abs(gm[ii][j]) > tolm:
                k1 = k
                i1 = i
                ifl = 1
            if ifl == 1:
                break
        if ifl == 1:
            break
    if nsw > nswmax or cab < 0:
        break
#-----  calculation of eigenvalues -----
for i in range(0, nq):
    if abs(gm[i][i]) < tolm:
        gm[i][i] = tolm
    evl[i] = s[i][i] / gm[i][i]
#----- scaling of eigenvectors
for i in range(0, nq):
    gm2 = math.sqrt(abs(gm[i][i]))
    for j in range(0, nq):
        evc[i][j] = evc[i][j] / gm2
#-----   results   -----
#--- ascending order of eigenvalues
for i in range(0, nq):
    ii = nord[i]
    i1 = ii
    c1 = evl[ii]
    j1 = i
    for j in range(i, nq):
        ij = nord[j]
        if c1 > evl[ij]:
            c1 = evl[ij]
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
        dummy = dummy + " value = "+ str("%12.4e"% evl[ii]) + "\n"
        omega = math.sqrt(evl[ii])
        freq = 0.5 * omega / math.pi
        dummy = dummy + "omega = " + str("%12.4e"% omega) + "\n"
        dummy = dummy + "freq Hz = " + str("%12.4e"% freq) + "\n"
        dummy = dummy + "eigenvector\n"
        for j in range (0,nq):
            dummy = dummy + str("%12.4e"% evc[ii][j]) + " "
        dummy = dummy + "\n"
print(dummy)