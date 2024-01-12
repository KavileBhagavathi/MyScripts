# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 10:46:39 2023

@author: arjun
"""

import numpy as np


def compute_qr(A):
    m,n = np.shape(A)
    #checking whether m>=n is False
    if n > m:
        return("Matrix with more columns than rows. Try again")
    #Select each column vector from matrix A using array slicing
    W = np.zeros((m, n),dtype=complex)
    R = A.copy().astype(complex)
    for k in range(0,n):
        Xk = np.copy(R[k:,k])
        ek = np.zeros((m-k,1))
        ek[0]=1
        Vk = (1 if Xk[0]>0 else -1)*np.linalg.norm(Xk,ord=2)*ek + Xk.reshape(-1,1)
        Vk = Vk/np.linalg.norm(Vk,ord=2)
        #R[k:m, k:n] = R[k:m, k:n] - 2*np.outer(np.outer(Vk,Vk.T),R[k:m,k:n])
        R[k:m, k:n] = R[k:m, k:n] - 2 * np.dot(Vk, (Vk.T @ R[k:m, k:n]))
        W[k:,[k]] = Vk
    return W,R


def form_q(W):
    m,n = np.shape(W)
    if n > m:
        return("Invalid input matrix!")
    x = np.eye(m).astype(complex)
    for i in range(0,m):
        for j in range(n-1,-1,-1):
            x[j:, i] = x[j:, i] - 2 * W[j:, j] * np.dot(W[j:, j].T, x[j:, i])
    return x

      
# def implicit_qr(A):
#     m, n = A.shape
#     W = np.zeros((m, n), dtype=complex)
#     R = A.copy()

#     for k in range(n):
#         x = R[k:m, k]
#         norm_x = np.linalg.norm(x)
#         e = np.zeros((m - k, 1), dtype=complex)
#         e[0] = 1
#         V = (np.sign(x[0])) * norm_x * e + x.reshape(-1, 1)
#         C = V / (np.linalg.norm(V))

#         R[k:m, k:n] = R[k:m, k:n] - 2 * np.dot(C, (C.conj().T @ R[k:m, k:n]))
#         W[k:m, k] = C.reshape(1, -1)
#         print(f"iteration{k+1}\n{V}\n{R}\n{W}")
#     return W, R        
        

if __name__ == "__main__":
    A = np.array([[-1,-1,1],[1,3,3],[-1,-1,5]])
    A = np.random.randint(0,5,(3,3))
    W,R = compute_qr(A)
    Q = form_q(W)
    print("Hello")
    

def house(A):
    m, n = A.shape

    if m < n:
        print("[HOUSEHOLDER] Error: This is forbidden!")
        return np.array([]), np.array([])
    W = np.zeros((m, n), dtype=float)
    R = np.copy(A).astype(float)
    for k in range(n):
        vk = np.copy(R[k:, k])
        vk[0] += (1 if (vk[0]) >= 0 else -1) * np.linalg.norm(vk, 2)
        W[k:, k] = vk / np.linalg.norm(vk, 2)
        R[k:, k:] -= np.dot((2 / np.dot(vk, vk))
                            * np.dot(vk[:, None], vk[None, :]), R[k:, k:])
    return W, R