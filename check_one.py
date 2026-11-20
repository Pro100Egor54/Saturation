from math import pi
from typing import List


def count_area(diameter: float) -> float:
    """Расчет площади"""
    return pi * ((diameter / 2) ** 2)

def Q_to_V(Q, S):
    return Q / S

def Reidens(Ro: float, V: float, L: float, Mu: float):
    """Число рейдена"""
    return Ro * V * L / Mu

def pressure_check(diam: float, height: float, Q: float, L = 6, Mu = 0.1, Ro = 1300) -> list[
    bool | float]:
    """
    Проверка потянет ли насос
    Q - Расход выходящей смеси
    diam - Диаметр трубки сиропа, параметризируется
    hieght - высота трубки сиропа, параметризируется
    """
    S = count_area(diam)
    V = Q_to_V(Q / 6, S)
    Re = Reidens(Ro, V, L, Mu)

    dP_Fr = 0
    if Re < 2300:
        dP_Fr = 32 * Mu * L * V / (diam ** 2)
    else:
        lamb = 64/Re
        dP_Fr = lamb * L * Ro * V ** 2 / (2 * diam)
    dP_st = Ro * 9.8 * height

    POut = 60*1000 - (dP_st + dP_Fr)
    return POut / 100_000
    # is_pushable = POut > 0
    # return [is_pushable, POut / 100_000]

    # return [False, -0.25]




