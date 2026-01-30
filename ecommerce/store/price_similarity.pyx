import numpy as np
cimport numpy as np

def compute_similarity(np.ndarray[np.float64_t, ndim=1] prices,
                       double avg_price):
    cdef int i, n = prices.shape[0]
    cdef np.ndarray[np.float64_t, ndim=1] scores = np.zeros(n)

    for i in range(n):
        scores[i] = abs(prices[i] - avg_price)

    return scores
