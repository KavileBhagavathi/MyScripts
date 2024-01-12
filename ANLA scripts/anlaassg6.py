# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:55:12 2024

@author: arjun
"""
import numpy as np
from scipy.linalg import hilbert
import matplotlib.pyplot as plt
A = hilbert(4)

def gershgorin(A):
    """Function that returns the maximum and minimum eigen value estimates 
    using Gershgorin theorem"""
    gershgorin_dict = {}
    m,_ = np.shape(A)
    for row in range(m):
        gershgorin_dict.update({f"Lambda {row+1}":
                                {
                                "Radius": sum(np.abs(A[row]))-A[row][row],
                                "Centre": A[row][row],
                                "Xmax": sum(np.abs(A[row])),
                                "Xmin": A[row][row]-(sum(np.abs(A[row]))-A[row][row])
                                 }
                                }
                               )
    Lambda_min = None
    Lambda_max = None
    for key in gershgorin_dict.keys():
        if Lambda_min == None or gershgorin_dict[key]["Xmin"] < Lambda_min:
            Lambda_min = gershgorin_dict[key]["Xmin"]
            
        if Lambda_max == None or gershgorin_dict[key]["Xmax"] > Lambda_max:
            Lambda_max = gershgorin_dict[key]["Xmax"]
        print("Current min: " + str(Lambda_min))
        print("Current max: " + str(Lambda_max))
    
    return [Lambda_min,Lambda_max]

def power(A,v0):
    """Function to implement power iteration to find eigen values of a matrix"""
    m,_ = np.shape(A)
    v = np.zeros((m,1)) 
    v[0] = 1 #Initial guess Vo
    conv = 1
    error_list = []
    while conv > 1e-13:
        w = np.dot(A,v)
        v_k = w/(np.linalg.norm(w,ord=2))
        Av_k = np.dot(A, v_k)
        lambda_k = np.dot(v_k.T,Av_k)
        diff = np.dot(A,v_k) - lambda_k*v_k
        conv = max(np.abs(diff))
        conv = conv[0] #since I don't need an array but a number
        error_list.append(conv)
        v = v_k #v_k would be the new eigen vector estimation
    return v,lambda_k,error_list
        
        