
from Class.Complex import *


def divergence(z:, w) -> [bool, int]:
    """
    Verify if the coordonate diverge with the equation z² + w
    :param z: complex for each coordinate
    :param w: complex number for the Julia set
    :return: [bool, int]
    """
    # Create 2 lists to compare
    t_reel = []
    t_imag = []

    # Initial conditions
    velocity = 2    # Divergence velocity to put colors
    z = z * z + w
    t_reel.append(z.re)
    t_imag.append(z.im)
    z = z * z + w
    t_reel.append(z.re)
    t_imag.append(z.im)

    # Verify if the coordonate diverge
    for i in range(2, 50):
        velocity += 1
        z = z * z + w
        t_reel.append(z.re)
        t_imag.append(z.im)

        # Verify if the equation diverge
        if t_reel[i] >= 10 or t_imag[i] >= 10 or t_reel[i] <= -10 or t_imag[i] <= -10:
            return [False, velocity]

        # Verify if the equation loop
        elif t_reel[i - 2] == t_reel[i] and t_imag[i - 2] == t_imag[i]:
            return [True, velocity]

    return [True, velocity]

