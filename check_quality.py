import numpy as np
from netCDF4 import Dataset
import xarray as xr

# function to check quality of profile

#mwrpfile = mwrp file name
#start_time = 
def check_quality(mwrpfile, start_time):
    
    ds = xr.open_dataset(mwrpfile,decode_times=False)
    wet_wind = ds.wetWindowFlag.values
    dqf_all = ds.dataQualityFlags.values
    time = ds.time_offset.values
    qv = ds.waterVaporMixingRatio.values
    qv_q = ds.qc_waterVaporMixingRatio.values
    temp = ds.temperature.values
    height = ds.height.values
    start_i = (np.abs(time-start_time)).argmin()
    end_t = start_time - 3600 # up to an hour prior
    end_i = (np.abs(time-end_t)).argmin()
    q_fix = qv[start_i,:]
    t_fix = temp[start_i,:]

    qv_q = qv_q[start_i,:]
    wet_wind2 = wet_wind[start_i]
    dqf = dqf_all[start_i,:]
    quality_time = 0.  
    t = start_i
    x = np.where(dqf != 0.)
    nx = len(x[0])
    y = np.where(q_fix <= 0)
    ny = len(y[0])

    if (wet_wind2 == 1) or (nx != 0):
        
        t_fix = height.copy()
        t_fix[:] = np.nan
        q_fix = height.copy()
        q_fix[:] = np.nan
   # check wet windows and data quality flags in prior times - up to an hour - make note of this lag
        while ((wet_wind2 != 0) or (nx != 0) or (ny != 0)) and (t <= end_i):
            t=t-1  
            wet_wind2 = wet_wind[t] 
            dqf = dqf_all[t,:]
            x = np.where(dqf != 0.)
            nx = len(x)
       # print(t, time[t], wet_wind2, nx, ny)
            t_fix = temp[t,:]
            q_fix = qv[t,:]
            y = np.where(q_fix <= 0.)
        quality_time = start_time - time[t]

  
    #print(wet_wind, nx)

    return([t_fix,q_fix,quality_time])


