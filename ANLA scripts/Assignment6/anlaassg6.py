# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:55:12 2024

@author: arjun
"""
import numpy as np
from scipy.linalg import hilbert
import matplotlib.pyplot as plt
#A = hilbert(4)
A = np.diag([1, 2, 3, 4]) + np.ones((4, 4))

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
        # print("Current min: " + str(Lambda_min))
        # print("Current max: " + str(Lambda_max))
    
    return Lambda_min,Lambda_max

def power(A,v0):
    """Function to implement power iteration to find eigen values of a matrix"""
    conv = 1 #Just a dummy value above the convergence criterion to get started with the loop
    error_list = []
    v = v0
    while conv > 1e-13:
        w = np.dot(A,v)
        v_k = w/(np.linalg.norm(w,ord=2))
        Av_k = np.dot(A, v_k)
        lambda_k = np.dot(v_k.T,Av_k)
        diff = Av_k - lambda_k*v_k
        conv = np.max(np.abs(diff))
        #conv = conv[0] #since I don't need an array but a number
        error_list.append(conv)
        v = v_k #v_k would be the new eigen vector estimation
    return v,lambda_k,error_list

def inverse(A,v0,mu):
    """Function to implement inverse iteration to find eigen values of a matrix"""
    conv = 1 #Just a dummy value above the convergence criterion to get started with the loop
    error_list = []
    v = v0
    m,_ = np.shape(A)
    while conv > 1e-13:
        A_muI = A - mu*np.eye(m)
        A_mu_inv = np.linalg.inv(A_muI)
        w = np.dot(v,A_mu_inv)
        v_k = w/np.linalg.norm(w,ord=2)
        Av_k = np.dot(A,v_k)
        lambda_k = np.dot(v_k.T,Av_k)
        diff = Av_k - lambda_k*v_k
        conv = np.max(np.abs(diff))
        #conv = conv[0]
        error_list.append(conv)
        v = v_k
    return v,lambda_k,error_list

def rayleigh(A,v0):
    """Function to implement Rayleigh Quotient iteration to find eigen values of a matrix"""
    conv = 1 #Just a dummy value above the convergence criterion to get started with the loop
    error_list = []
    v = v0
    Av0 = np.dot(A,v0)
    lambda_0 = np.dot(v0.T,Av0)
    lambda_k = lambda_0
    m,_ = np.shape(A)
    while conv > 1e-13:
        A_lambdak = A - lambda_k*np.eye(m)
        A_lambdak_inv = np.linalg.inv(A_lambdak)
        w = np.dot(v,A_lambdak_inv)
        v_k = w/np.linalg.norm(w,ord=2)
        Av_k = np.dot(A,v_k)
        lambda_k = np.dot(v_k.T,Av_k)
        diff = Av_k - lambda_k*v_k
        conv = np.max(np.abs(diff))
        error_list.append(conv)
        v = v_k
    return v,lambda_k,error_list


def randomInput(m):
    #! DO NOT CHANGE THIS FUNCTION !#
    A = np.random.rand(m, m) - 0.5
    A += A.T  # make matrix symmetric
    v0 = np.random.rand(m) - 0.5
    v0 = v0 / np.linalg.norm(v0) # normalize vector
    return A, v0    