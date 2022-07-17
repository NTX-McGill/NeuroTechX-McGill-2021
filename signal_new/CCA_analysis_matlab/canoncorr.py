import numpy as np
import scipy.linalg

def canoncorr(X, Y):
    '''
    Follows MATLAB's CCA implementation (canoncorr function).
    Shape of X and Y: (n_samples, n_channels)

    Returns: A, B, r, U, V (same as MATLAB canoncorr())
    '''

    def rank_helper(X):
        Q, T, perm = scipy.linalg.qr(X, mode='economic', pivoting=True)
        rank = np.sum(np.abs(np.diag(T)) > (np.spacing(np.abs(T[0,0])) * np.max(X.shape)))
        if rank == 0:
            raise ValueError("Bad data")
        elif rank < p1:
            print('Warning: not full rank')
            Q = Q[:, :rank]
            T = T[:rank, :rank]
        return rank, Q, T, perm

    n, p1 = X.shape
    if n != Y.shape[0]:
        raise ValueError(f'X and Y must have the same number of rows, got {n} and {Y.shape[0]}')
    _, p2 = Y.shape

    # center the variables
    X -= np.mean(X, axis=0)
    Y -= np.mean(Y, axis=0)

    # factor the inputs, and find a full rank set of columns if necessary
    rankX, Q1, T11, perm1 = rank_helper(X)
    rankY, Q2, T22, perm2 = rank_helper(Y)

    # compute canonical coefficients and canonical correlations
    d = min(rankX, rankY)
    L, D, M_T = np.linalg.svd(Q1.T @ Q2, full_matrices=False)
    M = M_T.T
    A_tmp = np.linalg.solve(T11, L[:, :d]) * np.sqrt(n-1)
    B_tmp = np.linalg.solve(T22, M[:, :d]) * np.sqrt(n-1)
    r = np.minimum(np.maximum(D[:d], 0), 1)

    # put coefficients back to their full size and their correct order
    A = np.zeros((p1, d))
    B = np.zeros((p2, d))
    A[perm1[:rankX]] = A_tmp
    B[perm2[:rankY]] = B_tmp

    # compute canonical variates
    U = X @ A
    V = Y @ B
    
    return A, B, r, U, V

if __name__ == '__main__':

    import matlab
    import matlab.engine
    eng = matlab.engine.start_matlab()

    np.set_printoptions(precision=4, suppress=True, linewidth=100, sign=' ')

    n_rows = 1250
    n_cols_X = 8
    n_cols_Y = 10
    n_tests = 100

    seed = None
    rng = np.random.default_rng(seed)

    n_passed = 0
    for i_test in range(n_tests):
        X = rng.random((n_rows, n_cols_X))
        Y = rng.random((n_rows, n_cols_Y))

        out_matlab_all = [np.array(out) for out in eng.canoncorr(matlab.double(X.tolist()), matlab.double(Y.tolist()), nargout=5)]
        out_python_all = canoncorr(X, Y)

        passed = True
        for i_out, (out_matlab, out_python) in enumerate(zip(out_matlab_all, out_python_all)):
            # check r (correlation) only because A/B/U/V might have columns with opposite signs
            if i_out == 2:
                if not np.allclose(out_matlab, out_python):
                    passed = False
                    # print(out_matlab)
                    # print('--------------------')
                    # print(out_python)
                    # print('====================')
        if passed:
            n_passed += 1

    print(f'{n_passed} out of {n_tests} tests passed')
