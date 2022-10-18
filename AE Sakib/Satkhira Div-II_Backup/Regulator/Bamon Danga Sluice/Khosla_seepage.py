#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import numpy as np
import pandas as pd


# In[2]:


"""Solution of Cubic Equation"""
def solve_cubic(a,b,c,d):
    eqn=np.poly1d([a,b,c,d])
    inv_a=1./a
    b_a=inv_a*b
    b_a2=b_a*b_a
    c_a=inv_a*c
    d_a=inv_a*d
    Q = (3 * c_a - b_a2) / 9
    R = (9 * b_a * c_a - 27 * d_a - 2 * b_a * b_a2) / 54
    Q3 = Q * Q * Q
    D = Q3 + R * R
    print("Q={} R={} D={}".format(Q,R,D))
    b_a_3 = (1. / 3.) * b_a
    CV_PI=4*math.atan(1)
    if D>0:
        sqrt_D=math.sqrt(D)
        S=np.cbrt(R+sqrt_D)
        T=np.cbrt(R-sqrt_D)
        S_plus_T=S+T
        S_minus_T=S-T
        sqrt_3=math.sqrt(3)
        img_part=(1./2.)*sqrt_3*(S_minus_T)
        real_part=-b_a_3-(1./2.)*S_plus_T
        x1=- b_a_3+S_plus_T
        x2=complex(real_part,img_part)
        x3=complex(real_part,-img_part)
        
    elif D==0:
        S=np.cbrt(R)
        x1=- b_a_3+2*S
        x2=- b_a_3-S
        x3=-- b_a_3-S
    else:
        theta = math.acos(R / math.sqrt(-Q3));
        sqrt_Q = math.sqrt(-Q);
        x1 = 2 * sqrt_Q * math.cos(theta/3.0) - b_a_3;
        x2 = 2 * sqrt_Q * math.cos((theta + 2 * CV_PI)/ 3.0) - b_a_3;
        x3 = 2 * sqrt_Q * math.cos((theta + 4 * CV_PI)/ 3.0) - b_a_3;
    myvalues={"x1":x1,"x2":x2,"x3":x3,'eqn':eqn}
    return  myvalues


# In[3]:


def criticalCutoffLength(GE,H,b):
    pi=4*math.atan(1)
    pi2=pi*pi
    GE2=GE*GE
    H2=H*H
    dc=(2*H2)/(GE2*pi2*b)
    print("for H={} b={} GE={} d={}".format(H,b,GE,dc))
    
def calcualteExitGradient(b,d,H):
    pi=4*math.atan(1)
    alpha=b/d
    lamda=0.5*(1+math.sqrt(1+alpha*alpha))
    T1=1.0/pi
    T2=H/(d*1.0)
    T3=1.0/math.sqrt(lamda)
    GE=T1*T2*T3
    print("Exit Gradient={}".format(GE))
    
def mutual_interfernce_cooection(b,d,bprime,D):
    """parameters
    bprime=distance between two pile
    b=total floor length
    d=depth of pile in which correction to be applied
    D=depth of pile which makes interferenc 
    """
    C=19.0*math.sqrt(D/bprime)*((D+d)/b)
    print("mutual correction factor={}".format(C))
    return C
    
def uncorrected_khosla_value(b,d):
    pi=4*math.atan(1)
    alpha=b/d
    lamda=0.5*(1+math.sqrt(1+alpha*alpha))
    T1=1.0/pi
    Phi_E=T1*math.acos((lamda-2)/lamda)
    Phi_D=T1*math.acos((lamda-1)/lamda)
    Phi_C1=1-Phi_E
    Phi_D1=1-Phi_D
    myvalues={"Phi_E":Phi_E,"Phi_D":Phi_D,"Phi_C1":Phi_C1,"Phi_D1":Phi_D1}
    print("pi={} alpha={} lamda={}".format(pi,alpha,lamda))
    print("Phi_D1={} Phi_C1={}  Phi_D={} Phi_E={}".format(Phi_D1,Phi_C1,Phi_D,Phi_E))
    return myvalues

def corrected_khosla_value(b,d,t):    
    """parameters
    bprime=distance between two pile
    b=total floor length
    d=depth of pile in which correction to be applied
    D=depth of pile which makes interferenc 
    t=approximate floor thickness
    """    
    myvalues=uncorrected_khosla_value(b,d)
    mc=mutual_interfernce_cooection(b,d-t,b,d-t)
    Phi_E=myvalues['Phi_E']
    Phi_D=myvalues['Phi_D']
    Phi_C1=myvalues['Phi_C1']
    Phi_D1=myvalues['Phi_D1']
    print(myvalues)
    tc_us=( Phi_D1-Phi_C1)*(t/d)
    Phi_C1_cor=Phi_C1+tc_us+(mc/100)
    print("thicknes correction us={} Phi_C1_cor={}".format(tc_us,Phi_C1_cor))
    tc_ds=(Phi_D-Phi_E)*(t/d)
    #print("thicknes correction ds={} Phi_E_cor={}".format(tc_ds,Phi_E_cor))
    Phi_E_cor=Phi_E+tc_ds+(mc/100)
    print("thicknes correction ds={} Phi_E_cor={}".format(tc_ds,Phi_E_cor))
    locations=["Phi_E","Phi_C1"]
    uncorrected=[round(Phi_E*100,2),round(Phi_C1*100,2)]
    t_corrr=[round(-tc_ds*100,2),round(tc_us*100,2)]
    mc_corr=[-mc,mc]
    corrected=[round(Phi_E_cor*100,2),round(Phi_C1_cor*100,2)]
    data={"locations":locations,"uncorrected":uncorrected,"mc_corr":mc_corr,"corrected":corrected}
    myframe=pd.DataFrame(data)
    return myframe


# In[4]:


uncorrected_khosla_value(80,6)


# In[5]:


mutual_interfernce_cooection(120,4.5,120,4.5)


# In[6]:


criticalCutoffLength(1/7.0,7.344,120)
calcualteExitGradient(120,4.49,7.344)


# In[7]:


myframe=corrected_khosla_value(80,6,1.5)


# In[8]:


myframe


# In[9]:


"""Finding Reqiured Minimum Cutoff"""
GE_crtitical=0.18
pi=4*math.atan(1)
H=1.5
b=13.0
C=GE_crtitical*pi*math.sqrt(2.0)/H
print("C={}".format(C))
a1=C
b1=(-1.0)/(2*math.pow(b,1.5))
c1=0
d1=-1.0*math.sqrt(b)
myvalues=solve_cubic(a1,b1,c1,d1)
print(myvalues)
d=myvalues['x1']*myvalues['x1']
print(d)
calcualteExitGradient(b,d,H)


# In[10]:


myvalues=solve_cubic(1,-11.385,0,28.03)
print(myvalues)


# In[ ]:




