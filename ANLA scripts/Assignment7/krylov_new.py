# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 23:53:15 2024

@author: arjun
"""

import numpy as np

def gmres(A, b, threshold=1e-12):
    n = len(A)
    m = A.shape[1]
    x = np.zeros(A.shape[1])
    # use x as the initial vector
    r = b - np.dot(A, x)

    b_norm = np.linalg.norm(b)
    error = np.linalg.norm(r) / b_norm

    # initialize the 1D vectors
    # sn = np.zeros(m)
    # cs = np.zeros(m)
    e1 = np.zeros(m+1)
    e1[0] = 1
    e = [error]
    r_norm = np.linalg.norm(r)
    Q = np.zeros((n, m+1))
    Q[:, 0] = r / r_norm
    # Note: this is not the beta scalar in section "The method" above but
    # the beta scalar multiplied by e1
    beta = r_norm * e1
    H = np.zeros((m+1, m))
    for k in range(m):

        # run arnoldi
        H[:k+2, k], Q[:, k+1] = arnoldi(A, Q, k)

        # eliminate the last element in H ith row and update the rotation matrix
        # H[:k+2, k], cs[k], sn[k] = apply_givens_rotation(H[:k+2, k], cs, sn, k)

        # # update the residual vector
        # beta[k + 1] = -sn[k] * beta[k]
        # beta[k]     = cs[k] * beta[k]
        # error       = abs(beta[k + 1]) / b_norm
        
        # save the error
        e.append(error)

        if (error <= threshold):
            break

    # if threshold is not reached, k = m at this point (and not m+1) 

    # calculate the result
    y = np.linalg.solve(H[:k+1, :k+1], beta[:k+1])
    x = x + np.dot(Q[:, :k+1], y)
    return x, e

#----------------------------------------------------%
#                  Arnoldi Function                  %
#----------------------------------------------------%
def arnoldi(A, Q, k):
    q = np.dot(A, Q[:, k])   # Krylov Vector
    h = np.zeros(k+2)
    for i in range(k+1):     # Modified Gram-Schmidt, keeping the Hessenberg matrix
        h[i] = np.dot(q, Q[:, i])
        q = q - h[i] * Q[:, i]
    h[k + 1] = np.linalg.norm(q)
    q = q / h[k + 1]
    return h, q

#----------------------------------------------------%
#          Apply Givens Rotation Function            %
#----------------------------------------------------%
def apply_givens_rotation(H, cs, sn, k):
    def rotate(i, H, cs, sn, k):
        temp     =  cs[i] * H[i] + sn[i] * H[i+1]
        H[i+1]   = -sn[i] * H[i] + cs[i] * H[i+1]
        H[i]     = temp
    # apply for ith column
    for i in range(max(0, k-1), k):
        rotate(i, H, cs, sn, k)

    # update the next sin cos values for rotation
    r = np.sqrt(H[k]**2 + H[k+1]**2)
    cs[k] = H[k] / r
    sn[k] = -H[k+1] / r
    H[k] = cs[k] * H[k] - sn[k] * H[k+1]
    H[k+1] = 0.0
    return H, cs[k], sn[k]
