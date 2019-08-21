import math


def flux_to_power(flux, distance):
    return flux * 4 * math.pi * (distance * 3.086E18)**2 * 1e-7
