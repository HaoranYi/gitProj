import numpy as np
n = 200
Z = np.zeros((n+2, n+2), [('U', np.double), ('V', np.double)])
U, V = Z['U'], Z['V']
u,v = U[1:-1, 1:-1], V[1:-1, 1:-1]

def laplacian(Z):
    return (                Z[0:-2, 1:-1] +
            Z[1:-1, 0:-2] - 4*Z[1:-1,1:-1] + Z[1:-1,2:] +
                            Z[2:, 1:-1])

for i in xrange(25000):    
    Lu = laplacian(U)
    Lv = laplacian(V)
    uvv = u*v*v
    u += (Du*Lu - uvv + F*(1-u))
    v += (Dv*Lv + uvv - (F+k)*v)
