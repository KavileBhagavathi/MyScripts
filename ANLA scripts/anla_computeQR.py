def compute_qr(A):
    m,n = np.shape(A)
    #checking whether m>=n is False
    if n>m:
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
        R[k:m, k:n] = R[k:m, k:n] - 2 * np.dot(Vk, (Vk.conj().T @ R[k:m, k:n]))
        W[k:,[k]] = Vk
    return R,W