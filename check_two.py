from math import pi, e

def calc_S(diam):
    return pi * (diam ** 2) / 4

def calc_V(Q, S):
    return Q / S

def time_to_down(H, V):
    return H / V

def gazi_check(Q, diam = 0.2, H=1.2, k=0.0178):
    S = calc_S(diam)
    V = calc_V(Q, S)
    t = time_to_down(H, V)

    return 100 * (1 - e**(-k*t))


