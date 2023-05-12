
from Class.Complex import *


def divergence(z, w):
    t_reel = []
    t_imag = []
    v = 2
    z = z * z + w
    t_reel.append(z.re)
    t_imag.append(z.im)
    z = z * z + w
    t_reel.append(z.re)
    t_imag.append(z.im)
    for i in range(2, 50):
        v += 1
        z = z * z + w
        t_reel.append(z.re)
        t_imag.append(z.im)

        if t_reel[i] >= 10 or t_imag[i] >= 10 or t_reel[i] <= -10 or t_imag[i] <= -10:
            return [False, v]
        elif t_reel[i - 2] == t_reel[i] and t_imag[i - 2] == t_imag[i]:
            return [True, v]

    return [True, v]


