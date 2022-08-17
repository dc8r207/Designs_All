#for solving Ax = b, A symmetric
import numpy as np
#Enter symmetric matrix A()
A = np.array([[6.,0,1,2,0,0,2,1],
[0,5,1,1,0,0,3,0],
[1,1,6,1,2,0,1,2],
[2,1,1,7,1,2,1,1],
[0,0,2,1,6,0,2,1],
[0,0,0,2,0,4,1,0],
[2,3,1,1,2,1,5,1],
[1,0,2,1,1,0,1,3]])
#Enter right hand side b()
b = np.array([1.,1,1,1,1,1,1,1])
x = np.zeros(8)
itr = 0
def cgsolve(a,b,x,itr):
    n = len(b)
    ad = np.zeros((n),dtype = float)
    g = np.zeros((n),dtype = float)
    g = -b
    d = b
    ad = np.zeros((n),dtype = float)
    gg1 = np.dot(g,g)
    while gg1 > .000001:
        itr = itr + 1
        dad = 0
        for i in range(0,n):
           c = 0
           for j in range(0,n):
              c = c + a[i, j] * d[j]
           ad[i] = c
           dad = dad + c * d[i]
        al = gg1 / dad
        gg2 = 0
        for i in range(0,n):
           x[i] = x[i] + al * d[i]
           g[i] = g[i] + al * ad[i]
           gg2 = gg2 + g[i] * g[i]
        bt = gg2 / gg1
        for i in range(0,n):
           d[i] = -g[i] + bt * d[i]
        gg1 = gg2
    return itr
itr = cgsolve(A, b, x, itr)
print ("Solution")
print ("iterations = ", itr)
print(x)

