import numpy as np


def cubic_roots(a, b, c, d):
    """Compute the roots of the cubic polynomial :math:`ax^3 + bx^2 + cx + d`.
    
    :param a: cubic coefficient
    :param b: quadratic coefficient
    :param c: linear coefficient
    :param d: constant
    :return: list of three complex roots
    
    This function does not check if the found roots are real or complex.
    """
    if (a != 0): # Case: ax^3 + bx^2 + cx + d = 0
        delta_0 = b**2 - 3*a*c
        delta_1 = 2*b**3 - 9*a*b*c + 27*a**2*d
        C = ((delta_1 + np.sqrt(delta_1**2 - 4*delta_0**3 + 0j)) / 2)**(1/3)
        zeta = -1/2 + 1j/2 * np.sqrt(3)
        return [-1/(3*a) * (b + zeta**k * C + delta_0 / (zeta**k * C))
                for k in [0, 1, 2]]
        
    elif (b != 0): # Case: bx^2 + cx + d = 0
        delta = c**2 - 4*b*d
        return [(-c + k*np.sqrt(delta + 0j))/(2*b)
                for k in [-1, 1]]
    
    elif (c != 0): # Case: cx + d = 0
        return -d/c
    
    elif (d != 0): # Case: d != 0 (without solution)
        return np.nan
    
    else: # Case: d = 0 (with trivial solution)
        return 0
