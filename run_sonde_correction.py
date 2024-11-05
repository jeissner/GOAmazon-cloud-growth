
#***********
# Example script for running the sounding correction
#
# Cloud 1 from GOAmazon campaign 20150118 16:12 UTC
# The modified qv profile includes corrections from the MWRP and MWR 
# The modified temp profile includes corrections from the MWRP
#
# Cloud 2 from GOAmazon campaign 20150524 19:16 UTC 
# The MWRP for this cloud time is not available or has a wet-window and therefore 
# shows an error of bad_mwrp=1 and no correction is applied
#
#***********
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from correction_sounding import correction_sounding
import xarray
from qvsat import qvsat

# CLOUD 1

sonde_file = 'maosondewnpnM1.b1.20150118.112900.cdf'
ds = xr.open_dataset(sonde_file,decode_times=False)
time_offset = ds.time_offset.values
obar_pres = ds.pres.values
base_time = ds.base_time.values
otemp = ds.tdry.values
odp = ds.dp.values
orh = ds.rh.values 
oheightm = ds.alt.values

otempK = otemp + 273.15
time_s = time_offset[0]
time_c = 16.2*60*60

oqv = oheightm.copy()
oqv[:] = np.nan
for h in range(0,len(oheightm)):
    qvsonde = qvsat(otempK[h],obar_pres[h])
    qvsonde = qvsonde * 1000.
    oqv[h] = (orh[h]/100) * qvsonde
    

t_corrected,q_new_corrected,bad_mwrp,bad_pwv,real_time_dif = correction_sounding('2015','01','18',oheightm, time_s, time_c, orh, obar_pres, otempK)

plt.plot(oqv, oheightm, label='sonde')
plt.plot(q_new_corrected,oheightm, label='corrected')
plt.ylim(0,5000)
plt.xlim(0,20)
plt.ylabel("Height [m]")
plt.xlabel("$q_v$ [g kg$^{-1}$]")
plt.legend()
plt.show()


# CLOUD 2

sonde_file = 'maosondewnpnM1.b1.20150524.172800.cdf'
ds = xr.open_dataset(sonde_file,decode_times=False)
time_offset = ds.time_offset.values
obar_pres = ds.pres.values
base_time = ds.base_time.values
otemp = ds.tdry.values
odp = ds.dp.values
orh = ds.rh.values 
oheightm = ds.alt.values

otempK = otemp + 273.15
time_s = time_offset[0]
time_c = 19.26*60*60

t_corrected,q_new_corrected,bad_mwrp,bad_pwv,real_time_dif = correction_sounding('2015','05','24',oheightm, time_s, time_c, orh, obar_pres, otemp+273.15)

plt.plot(otempK, oheightm)
plt.plot(t_corrected,oheightm)
plt.ylim(0,5000)
plt.xlim(270,305)
plt.ylabel("Height [m]")
plt.xlabel("Temperature [K]")
plt.show()