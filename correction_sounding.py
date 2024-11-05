# calculate difference between MWRP temperature and water vapor mixing ratio at the time of the sounding and at the time of the cloud
# does quality checks to make sure mwrp window is dry and observations are accurate
# constrains the qv correction profile to the MWR PWV

# year, month, day of the cloud
# oheightm = height profile of the sounding variables (m)
# time_s = time the sounding was launched (s)
# time_c = time of the start of the cloud (s)
# rhsonde = sounding relative humidity (%)
# psonde = sounding pressure (hPa)
# tsonde = soudning temperature (K)

import numpy as np
import xarray as xr
from check_quality import check_quality
from rescaleq_to_pwv import rescaleq_to_pwv
from qvsat import qvsat

def correction_sounding(vyear,vmonth,vday, oheightm, time_s, time_c, rhsonde, psonde, tsonde):
# convert sounding RH to qv
    qsonde = psonde.copy()
    qsonde[:] = np.nan
    for h in range(0, len(tsonde)):
        qvsonde = qvsat(tsonde[h],psonde[h])
        qvsonde = qvsonde * 1000.
        oq = (rhsonde[h]/100) * qvsonde
        qsonde[h] = oq
    
    bad_mwrp = 0
    bad_pwv = 0
    real_time_dif = 0

# import MWRP data
    file_string = 'maomwrpM1.b1.'+vyear+vmonth+vday+'.000919.cdf'
    ds = xr.open_dataset(file_string,decode_times=False)
    heights_c = ds.height.values

    
# do quality checks of mwrp profile at time of cloud and sounding and search up to an hour before for good profile
    temp_c,q_c,quality_time_c = check_quality(file_string, time_c)
    temp_s,q_s,quality_time_s = check_quality(file_string, time_s)
    if quality_time_c != 0: 
        real_time_dif = 1
    if quality_time_s != 0: 
        real_time_dif = 2
    if quality_time_c != 0 and quality_time_s != 0: 
        real_time_dif = 3 


    t_corrected = tsonde.copy()
    q_new_corrected = qsonde.copy()

    x = np.where(q_c <= 0.) 
    xx = np.where(q_s <= 0.)
    nx = len(x[0])
    nxx = len(xx[0])
    y = np.where(temp_c <= -9990.)
    yy = np.where(temp_s <= -9990.)
    ny = len(y[0])
    nyy = len(yy[0])
   
    if nx > 0 or nxx > 0 or ny > 0 or nyy > 0 :
        bad_mwrp = 1
        print('bad mwrp')
        return([t_corrected, q_new_corrected, bad_mwrp, bad_pwv, real_time_dif])
    
    q_c[x] = np.nan
    q_s[x] = np.nan
    temp_c[y] = np.nan
    temp_s[y] = np.nan
        
# get deltas between time of cloud and sounding 
    temp_dif = temp_c - temp_s
    q_dif = q_c - q_s

    temp_correct_new = np.zeros(len(oheightm))
    temp_correct_new[:] = 0. 
    w_correct_new = np.zeros(len(oheightm))
    w_correct_new[:] = 0.
    for h in range(0, len(heights_c)-1): 
        x = np.where((oheightm >= heights_c[h]) & (oheightm < heights_c[h+1]))
        temp_correct_new[x] = temp_dif[h]
        w_correct_new[x] = q_dif[h]
    
# no corrections above 10 km
    y = np.where(oheightm > 10000.)
    temp_correct_new[y] = 0. 
    w_correct_new[y] = 0. 

# add correction to sounding values
    print(tsonde)
    print(qsonde)
    print(psonde)
    x = np.where((tsonde > -99.) & (qsonde > -99.) & (psonde > -99.))
    t_corrected = tsonde[x] + temp_correct_new[x]
    q_corrected = (qsonde[x] + w_correct_new[x])/1000.
    psonde = psonde[x]
    print(q_corrected)
#plot, tsonde, oheightm
#oplot, t_corrected, oheightm

#***************Constrain Q correct to PWV***************
    q_new_corrected = rescaleq_to_pwv(vyear, vmonth, vday, time_c, q_corrected, psonde, oheightm[x])	
    q_new_corrected = q_new_corrected*1000
    print('new q', q_new_corrected)

    if q_new_corrected[0] < 0.:
        q_new_corrected=q_corrected*1000
        bad_pwv = 1

    #q_correct = q_new_corrected - qsonde
    return([t_corrected,q_new_corrected,bad_mwrp,bad_pwv,real_time_dif])



