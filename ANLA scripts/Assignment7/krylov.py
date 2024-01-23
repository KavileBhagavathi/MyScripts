# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:02:11 2024

@author: arjun
"""

import numpy as np
def create_A(k, ω=1):
    np.random.seed(17)
    D = np.diag(sum([[i] * i for i in range(1, k + 1)], []))
    m = D.shape[0]
    M = np.random.rand(m, m) - 0.5
    return D + ω * M
#b = np.ones(A.shape[0])
def cg(A, b, tol=1e-12):
    m = A.shape[0]
    x = np.zeros(m, dtype=A.dtype)
    r = b
    residual = []
    p = r
    # todo
    i = 0
    while i<=m or residual[-1]<tol:
        print(i)
        alpha_numer = np.dot(r.T,r)
        alpha_denom1 = np.dot(p.T,A)
        alpha_denom2 = np.dot(alpha_denom1,p)
        alpha = alpha_numer/alpha_denom2
        x_n = x + alpha*p 
        r_n = r - alpha*np.dot(A,p)
        beta_n = np.dot(r_n.T,r_n)/np.dot(r.T,r)
        p_n = r_n + beta_n*p
        #Updating inputs for next iteration
        x = x_n
        r = r_n
        p = p_n
        residual.append(np.linalg.norm(r_n,ord=2)/np.linalg.norm(b,ord=2))
        i = i +1
    return x, residual