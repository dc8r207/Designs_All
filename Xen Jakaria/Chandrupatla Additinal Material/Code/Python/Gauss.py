#=====       Program GAUSS         =====
#   T.R. Chandrupatl & A.D. Belegundu
#=======================================
import numpy as np
f = open("gauss.inp", "r")
li=f.read().splitlines()
print(li)
n = int(li[2])
a = np.zeros(shape = (n, n))
b = np.zeros(n)
for i in range(0,n):
  for j in range(0,n):
   x = li[i+4].split()
   a[i,j] = float(x[j])
print(a)
x = li[n+5].split()
for j in range(0,n):
    b[j] = float(x[j])
print(b)
#---Gauss Elimination Method
def gaussElim(a,b):
    n = len(b)
  # Elimination Phase
    for k in range(0,n-1):
        for i in range(k+1,n):
           if a[i,k] != 0.0:
               c = a [i,k]/a[k,k]
               a[i,k+1:n] = a[i,k+1:n] - c*a[k,k+1:n]
               b[i] = b[i] - c*b[k]
  # Backsubstitution
    for k in range(n-1,-1,-1):
        b[k] = (b[k] - np.dot(a[k,k+1:n],b[k+1:n]))/a[k,k]
    return b
c = gaussElim(a,b)
print (c)