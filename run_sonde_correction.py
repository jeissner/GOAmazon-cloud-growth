#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 15:10:26 2024

@author: jordaneissner
"""
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from correction_sounding import correction_sounding
import xarray

sonde_file = 'maosondewnpnM1.b1.20150524.172800.cdf'
ds = xr.open_dataset(sonde_file,decode_times=False)
time_offset = ds.time_offset.values
obar_pres = ds.pres.values
base_time = ds.base_time.values
otemp = ds.tdry.values
odp = ds.dp.values
orh = ds.rh.values 
oheightm = ds.alt.values

time_s = time_offset[0]
time_c = 19.26*60*60

t_corrected,q_new_corrected,bad_mwrp,bad_pwv,real_time_dif = correction_sounding('2015','05','24',oheightm, time_s, time_c, orh, obar_pres, otemp+273.15)

plt.plot(otemp+273.15, oheightm)
plt.plot(t_corrected,oheightm)
plt.ylim(0,3000)
plt.xlim(285,305)
plt.show()
