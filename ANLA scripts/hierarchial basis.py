# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 18:52:10 2023

@author: arjun
"""
import numpy as np
import matplotlib.pyplot as plt
i_list = np.linspace(0,2,5)
y_list = []
x_list_plt = []
for i in i_list:
    x_list = np.linspace(i,0.5*(2*i+1),5)
    for x in x_list:
        y = 2*x - 2*i
        print(x)
        print(y)
        y_list.append(y)
        x_list_plt.append(x)
for i in i_list:       
    x_list2 = np.linspace((2*i+1)*0.5,(2*i+2)*0.5,5)
    for x in x_list2:
        y = 2*(i+1) - 2*x
        y_list.append(y)
        x_list_plt.append(x)
plt.plot(x_list_plt,y_list)