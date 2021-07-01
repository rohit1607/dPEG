
def max_min(mat):
    m,n = mat.shape
    return max([min(mat[i,:]) for i in range(m)])

import numpy as np
A = np.arange(16).reshape((4,4))
print(A, max_min(A))
