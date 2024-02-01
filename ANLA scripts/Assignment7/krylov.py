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
    """Function to implement Conjugate Gradient iteration"""
    m = A.shape[0]
    x = np.zeros(m, dtype=A.dtype)
    r = b
    residual = [1]
    p = r.copy()
    # todo
    i = 0
    for i in range(m):
        print(i)
        alpha_numer = np.dot(r.T,r)
        alpha_denom1 = np.dot(p.T,A)
        alpha_denom2 = np.dot(alpha_denom1,p)
        alpha = alpha_numer/alpha_denom2 #step length
        x_n = x + alpha*p  #approx solution
        r_n = r - alpha*np.dot(A,p) #residual
        beta_n = np.dot(r_n.T,r_n)/np.dot(r.T,r) #improvement in this step
        p_n = r_n + beta_n*p #search direction
        #Updating inputs for next iteration
        x = x_n
        r = r_n
        p = p_n
        residual.append(np.linalg.norm(r_n,ord=2)/np.linalg.norm(b,ord=2))
        if residual[-1] < tol:
            break
    return x, residual

def arnoldi_n(A, Q, P=None):
    """Function to implement Arnoldi iteration"""
    
    n = Q.shape[1] #mxn matrix in book, nxn for code
    H = np.zeros((n+1,n)) #Initialize the Hessenberg matrix
    for i in range(n):
        v = np.dot(A, Q[:, i]) 
        for j in range(i+1):
            H[j, i] = np.dot(Q[:, j].T, v)
            v = v - np.dot(H[j, i],Q[:,j])
        H[n+1,n] = np.linalg.norm(v,ord=2)
        if H[n+1,n] == 0:
            break
        q_nplus1 = v/(np.linalg.norm(v,ord=2))
    return H[:,n],q_nplus1

def arnoldi(A, Q, k):
  q = np.dot(A,Q[:, k]) # Krylov Vector
  h = np.zeros(k + 1) # Initializing Hessenberg matrix
  for i in range(k): # Modified Gram-Schmidt, keeping the Hessenberg matrix
    h[i] = q.T @ Q[:, i]
    q = q - h[i] * Q[:, i]
  h[k] = np.linalg.norm(q)
  q = q / h[k]
  return h, q

    
def gmres(A, b, P, tol):
    x = np.zeros(A.shape[1]) #initial guess 
    q = b / (np.linalg.norm(b,ord=2)) #inital guess vector
    n = q.shape[0]
    m = A.shape[0]
    Q = np.zeros((n,n)) #Initializing unitary matrix 
    Q[:,0] = q #Set first column of Q as q
    residual = [1]
    H = np.zeros((1,0))
    Q = np.c_[q]
    for k in range(m):
        
        h,q = arnoldi_n(A, Q) #applying Arnold's iteration
        
    return x, residual
    
    
    