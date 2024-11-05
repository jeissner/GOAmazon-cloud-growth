# calculate saturation vapor pressure
# Based on Emanuel (1994) eq. 4.4.13
# Absolute temperature in [K]
# pressure in [hPa]

import math

def qvsat(tabs, pres):
    epsilon = 0.622
    estar = math.exp(53.67957 - 6743.769/tabs - 4.8451*math.log(tabs)) # estar [mb]

    return(epsilon*estar/(pres-estar))


