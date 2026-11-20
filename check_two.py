from math import pi, e


def gazi_check(Q, diam = 0.2, H=1.2, k=0.004744):
    S = pi * (diam ** 2) / 4
    V = Q / S
    t = H / V

    return 100 * (1 - e**(-k*t))


