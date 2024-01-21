# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:55:12 2024

@author: arjun
"""
import numpy as np
import matplotlib.pyplot as plt
#A = hilbert(4)
# A = np.diag([1, 2, 3, 4]) + np.ones((4, 4))

def gershgorin(A):
    """Function that returns the maximum and minimum eigen value estimates 
    using Gershgorin theorem"""
    m,_ = np.shape(A)
    Lambda_min,Lambda_max = 0,0
    for k in range(m):
        g_radius = sum(np.abs(A[k,:])) - np.abs(A[k,k])
        Lambda_max = max(Lambda_max, A[k,k] + g_radius)
        Lambda_min = min(Lambda_min, A[k,k] - g_radius)    
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
    v = v0.copy()
    m,_ = np.shape(A)
    while conv > 1e-13:
        A_muI = A - mu*np.eye(m)
        w = np.linalg.solve(A_muI,v)
        v_k = w/np.linalg.norm(w)
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

if __name__ == '__main__':
    pass
    #n = 5  # Size of the matrix
    # A = np.array([[14, 0, 1],
    #               [-3, 2,-2],
    #               [ 5,-3, 3]])  # Generate a random symmetric matrix
    # v0 = np.array([0, 0, 1])  # Initial eigenvector guess
    A,v0 = randomInput(5)
    mu = 1  # Eigenvalue estimate

    # Test the gershgorin function
    Lamb_min, Lamb_max = gershgorin(A)
    print(f"Gershgorin: λ_min = {Lamb_min}, λ_max = {Lamb_max}")

    # Test the power function
    v, Lambda, err = power(A, v0)
    print(f"Power: v = {v}, λ = {Lambda}, err = {err}")

    # Test the inverse function
    v, Lambda, err = inverse(A, v0, mu)
    print(f"Inverse: v = {v}, λ = {Lambda}, err = {err}")

    # Test the rayleigh function
    v, Lambda, err = rayleigh(A, v0)
    print(f"Rayleigh: v = {v}, λ = {Lambda}, err = {err}")