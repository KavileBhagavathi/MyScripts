# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 12:32:49 2024

@author: arjun
"""
import numpy as np
import matplotlib.pyplot as plt
#0<=i<=2**(n-1)
#n = 1,2,...

"""Hierarchial Basis"""
x_main = []
phi = []
for n in [3]:
    i_range = list(range(0,2**(n-1)))
    for i in i_range:
        x_upper1 = (2*i+1)*(2**(-n))
        x_lower1 = 2*i*(2**(-n))
        x_range1 = np.linspace(x_lower1, x_upper1,10,endpoint=False)
        for x in x_range1:
            phi.append(x*(2**n)-2*i)
            x_main.append(x)
        x_upper2 = (2*i+2)*(2**(-n))
        x_lower2 = (2*i+1)*(2**(-n))
        x_range2 = np.linspace(x_lower2, x_upper2,10,endpoint=False)
        for x in x_range2:
            phi.append(2*(i+1)-x*(2**n))
            x_main.append(x)
        x_range = np.concatenate((x_range1, x_range2))
plt.plot(x_main,phi)
plt.title(label="Plot of Basis Bh for n = 3")

"""Nodal Basis"""
# n = 7 
# i_range = list(range(1,n+1))
# nodal_phi = []
# for i in i_range:
#     x_lower1 = 

i = 1
n = 3
print("xlower1 is " + str(2*i*(2**(-n))) )
print("xupper1 is " + str((2*i+1)*(2**(-n))) )
print("xlower2 is " + str(2*(i+1)-x*(2**n) ))
print("xupper2 is " + str((2*i+2)*(2**(-n))) )


xi = np.array([2.95e-3,0.0332,7.125e-3,7.7125e-3,7.125e-3,5.4563e-3,2.95e-3])
vi = np.array([0.125 for i in range(0,7)])

xivi = np.array([i*j for i,j in zip(xi,vi)])
n = np.array([i for i in range(1,8)])
plt.plot(n,xivi)
plt.title(label="h) Plot of Un(x) for i = 1,2..7")


















