import numpy as np
import xarray as xr
from pwv_goffgratch_q import pwv_goffgratch_q


def rescaleq_to_pwv(vyear, vmonth, vday,time_c, qsonde, psonde, heights):

#******** IMPORT MWRRET DATA
    file_string = 'maomwrret1liljclouM1.c2.'+vyear+vmonth+vday+'.000000.cdf'
    ds = xr.open_dataset(file_string,decode_times=False)

    time_m = ds.time.values # obs about once every 24 seconds
    height_m = ds.level_height.values #km AGL
    be_pwv = ds.be_pwv.values #(time) best estimate precip water vapor (cm)
    be_lwp = ds.be_lwp.values #(time) best estimate liquid water path  (g/m^2)
    sonde_pwv = ds.sonde_pwv.values #(time) pwv integrated from radiosonde profile (cm)
 
# Find SONDE PWV 
    pwv_sonde = pwv_goffgratch_q(qsonde, psonde)
    #print('sonde pwv', pwv_sonde) # value start iteration
# Find MWRRET PWV at time of cloud
    index2 = (np.abs(time_m - time_c)).argmin()
    pwv_mwrret = be_pwv[index2]
    # print('cloud mwr pwv',  pwv_mwrret) # value want at end of iteration


# *************** Iterate sounding q profile so that sonde pwv equals mwr pwv at time of cloud

    q2 = -9999.
    pwv_new = -9999.
    q_new = qsonde.copy()
    q_new[:] = 0.

    y = np.where(heights > 10000)

    if pwv_mwrret > 0.0 and pwv_sonde > 0.:

        q2 = qsonde
        pwv_new = pwv_sonde

    if pwv_sonde < pwv_mwrret:
        while pwv_new < pwv_mwrret:
            q2[:] = q2[:] + 0.00001
            q2[y] = qsonde[y]
            x = np.where(q2 < 0.)
            q2[x] = 0.
            pwv_new = pwv_goffgratch_q(q2, psonde)
        # print, q2[0], pwv_new, pwv_mwrret


    if pwv_sonde > pwv_mwrret:
        while pwv_new > pwv_mwrret:
            q2[:] = q2[:] - 0.00001
            q2[y] = qsonde[y]
            x = np.where(q2 < 0.)
            q2[x] = 0. 
            pwv_new = pwv_goffgratch_q(q2, psonde)
        # print, q2(0), pwv_new, pwv_mwrret

    #print('FINAL ', q2[0], pwv_new)
    q_new = q2

    return(q_new)



