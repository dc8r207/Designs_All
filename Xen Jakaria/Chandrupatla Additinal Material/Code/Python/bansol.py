#=====   Program BANDSOLVER        =====
#   T.R. Chandrupatl & A.D. Belegundu
#=======================================
import numpy as np
f = open("bansol.inp", "r")
li=f.read().splitlines()
x = li[2].split()
n = int(x[0])
nbw = int(x[1])
a = np.zeros(shape = (n, nbw))
b = np.zeros(n)
for i in range(0,n):
  for j in range(0,nbw):
   x = li[i+4].split()
   a[i,j] = float(x[j])
print(a)
x = li[n+5].split()
for j in range(0,n):
    b[j] = float(x[j])
print(b)
#---Band Solver
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
c = bansol(a,b,nbw)
print (c)
#print (c)