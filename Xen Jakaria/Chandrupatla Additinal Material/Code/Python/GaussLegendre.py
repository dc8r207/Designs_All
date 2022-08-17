#Gauss-Legendre Integration Points and Weights
#---  T. R. Chandrupatla & A.D.Belegundu ---
#Give number of intgration points "n" needed
import math
n = 7

def glinteg(n):
    p3 = 0
    dmy = "IntegrationPoint        WeightFactor\n"
    n1 = math.floor((n + 1) / 2)
    for j in range(1,n1 + 1):
        x = math.cos(math.pi * (j - 1 / 4) / (n + 1 / 2))
        ifl = 0
        while ifl < 1:
            p1 = 0
            p2 = 1
            for i in range(1, n+1):
                p3 = (2 - 1 / i) * x * p2 - (1 - 1 / i) * p1
                p1 = p2
                p2 = p3
            dp = n / (x*x - 1) * (x * p2 - p1)
            x = x - p2 / dp
            w = 2 / (1 - x*x) / (dp*dp)
            if abs(p3) < 0.000000000001:
                s1 = "+- " + str(x) + "  " + str(w) + "\n"
                if abs(x) < 1e-10:
                    s1 = "   0                   " + str(w) + "\n"
                dmy = dmy + s1
                break
    return dmy
t = glinteg(n)
print(t)