def pwv_goffgratch_q(mixrat, pres):

# ---------------------------------------------------------------------------;
# This program will calculate the Precipitable Water Vapor for the column from 
# a sounding to be used for comparison with the PWV measurments derrived from 
# the MWRLOS and MWRP. 
#
# Taken from FORTRAN 77 code provided by Jim Liligren 
# Written by Ken Kehoe on 04/28/2005
# ----------------------------------------------------------------------------; 
# phase = 0 is water and anything else is ice
# tk = temp in K
# rh = rel hum in %
# pres = pressure in hpa (the units in sonde file)

#-- Calculate the saturation vapor pressure (mb) over liquid water or ice
#   given the temperature (K) using Goff-Gratch.


#-- Specific Humidity --;
    sphum = mixrat / (1.0+mixrat)

#-- Integrate specific humidity --;
    pwv = 0.0
    for ii in range(1, len(pres)-1):
        if sphum[ii] > 0: 
            pwv = pwv + 0.5*(sphum[ii]+sphum[ii-1])*(pres[ii-1]-pres[ii])
    pwv = pwv / (0.1*9.8)

    return(pwv)
