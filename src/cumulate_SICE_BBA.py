#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:24:33 2023

gap fill by cumulation

@author: jason

processing steps:
    1. src/gather_SICE_v2.3.3_or_v3.0_to_tif.py
    2. src/cumulate_SICE_BBA.py
    3. src/map_daily_albedo_anomalies.py
        ! cum_rev needed to seed 3
    4. src/albedo_timeseries_multisatellite.py
    5. src/plot_daily_alb_timeseries.py

search throughout for "!!" for clues what needs attention

"""

from pyproj import CRS,Transformer
import os
import numpy as np
from rasterio.transform import Affine
import rasterio as rio
import rasterio
from pathlib import Path
from datetime import date, timedelta
import matplotlib.pyplot as plt
import datetime

automation=0 # !! set to 1 for dates to be selected automatically

font_size=12
th=1
plt.style.use('default')
plt.rcParams["font.size"] = font_size 
plt.rcParams["mathtext.default"]='regular'
plt.rcParams['axes.grid'] = False
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.linewidth'] = th/2.
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']  # Preferred sans-serif fonts


if os.getlogin() == 'jason':
    base_path='/Users/jason/Dropbox/S3/SICE_anomaly_figs/'
    path_SICE_data_gathered_from_thredds='/Users/jason/0_dat/S3/opendap/'
else:
    # !! set to your path
    base_path='/Users/jason/Dropbox/S3/SICE_anomaly_figs/'
    path_SICE_data_gathered_from_thredds='/Users/jason/0_dat/S3/opendap/'

os.chdir(base_path)

current_year=2025

PolarProj = CRS.from_string("EPSG:3413") # example of an output projection

def get_msk(fn,product_index):
    msk = rasterio.open(fn).read(1)
    land=np.where(msk==1)
    # msk[land]=3
    # plt.imshow(msk)
    # plt.colorbar()
    notgl=np.where(msk==0)
    ice=np.where(msk==2)
    np.shape(msk)
    # assa
    return msk,notgl,land,ice

def datesx(date0,date1):
    # difference between current and previous date
    delta = timedelta(days=1)
    # store the dates between two dates in a list
    dates = []
    while date0 <= date1:
        # add current date to list by converting  it to iso format
        dates.append(date0.isoformat())
        # increment start date by timedelta
        date0 += delta
    # print('Dates between', date0, 'and', date1)
    # print(dates)
    return dates


##%% cumulate and output
years=np.arange(current_year,current_year+1).astype(str)

do_rev=0 # cumulate in reverse?
do_seed=1

for year in years:


    for product_index in range(5):
    
        if product_index==1:
            
            if product_index==0:
                sensor='OLCI'
                inpath=path_SICE_data_gathered_from_thredds ; outpath='colocated_AWS_SICE'
                var='albedo_bb_planar_sw'
                ver='Greenland_500m'
                ver2='OLCIv3.0_BSA'
                nj,ni=5424, 3007
                # basins_raster=get_basins('/Users/jason/Dropbox/Greenland map/Mouginot_sectors/basins_GrIS_done.tif',product_index)
                msk,notgl,land,ice=get_msk('/ancil/mask_500m_SICE_3.0.tif',product_index)
                inpath=f'/Users/jason/0_dat/S3/opendap/Greenland_500m/{year}/'
    
            if product_index==1:
                sensor='OLCI'
                inpath=path_SICE_data_gathered_from_thredds ; outpath='colocated_AWS_SICE'
                ver='Greenland_500m'
                var='BBA_combination'
                ver2='OLCIv3.0.1'
                nj,ni=5424, 3007
                msk,notgl,land,ice=get_msk('./ancil/mask_500m_on_SICE_3.0_grid.tif',product_index)
                inpath=f'{path_SICE_data_gathered_from_thredds}/Greenland_500m/{year}/'
    
            if product_index==2:
                sensor='OLCI'
                inpath='/Volumes/LaCie/0_dat/S3/SICE_2.3_1000m/Greenland_1000m/' ; outpath='colocated_AWS_SICE'
                inpath='/Users/jason/0_dat/S3/SICE_2.3_1000m/Greenland_1000m/'
                ver='Greenland_1000m'
                var='BBA_combination'
                ver2='OLCIv2.3.1'
                msk,notgl,land,ice=get_msk('./ancil/mask_1km_on_SICE_2.3.1_grid.tif',product_index)
                # basins_raster=get_basins('./ancil/basins_1km_on_SICE_2.3.1_grid.tif',product_index)
                nj,ni=2687, 1487

            if product_index==3:
                sensor='OLCI'
                inpath='/Users/jason/0_dat/S3/opendap/Greenland_500m/' ; outpath='colocated_AWS_SICE'
                ver='Greenland_500m'
                var='BBA_empirical'
                ver2='OLCIv3.0.1'
                msk,notgl,land,ice=get_msk('./ancil/mask_500m_on_SICE_3.0_grid.tif',product_index)
                # basins_raster=get_basins('./ancil/basins_1km_on_SICE_2.3.1_grid.tif',product_index)
                nj,ni=5424, 3007

            revname=''
            
            # if do_rev:
            #     dates=dates[::-1]
            #     print(dates)
            #     revname='_rev'
            
            if do_seed==0:
                BBA=np.zeros((nj,ni))
            else:
                d = datetime.datetime.today() - timedelta(days=1)
                m=int(d.strftime('%m'))
                day_minus_1=int(d.strftime('%d'))
                d = datetime.datetime.today() - timedelta(days=2)
                day_minus_2=int(d.strftime('%d'))
                m_minus_2=int(d.strftime('%m'))
                d = datetime.datetime.today() - timedelta(days=3)
                day_minus_3=int(d.strftime('%d'))
                m_minus_3=int(d.strftime('%m'))
                
                if automation:
                    dates=datesx(date(current_year, m_minus_3, day_minus_3),date(current_year, m, day_minus_1))
                else:
                    # for testing
                    dates=datesx(date(int(current_year), 5, 1),date(int(current_year), 5, 8))
                # d = datetime.datetime.today() - timedelta(days=10)
                # day_minus_10=int(d.strftime('%d'))
                # dates=datesx(date(int(year), 7, day_minus_10),date(int(year), m, day_minus_1))
                # print(dates)

                BBA=np.zeros((nj,ni))
                # fn=f'{inpath}{dates[0]}_BBA_empirical_cum.tif'
                fn='./ancil/BBA_combination_cum_2018-06.tif'
                band_1x = rasterio.open(fn)
                profile=band_1x.profile
                # profile=band_1x.profile
                bba=band_1x.read(1)
                # print(np.shape(bba))
                # if (np.shape(bba)[1]==3007):
                bba[notgl]=np.nan
                bba[land]=np.nan
                v=np.where(~np.isnan(bba))
                BBA[v]=bba[v]
            # count=np.zeros((5424, 3007))
            # if (np.shape(bba)[1]==3007):
                BBA[notgl]=np.nan
                BBA[land]=np.nan

            for dd,datex in enumerate(dates):
            
                # print(f'{year}{datex[4:]}')
                if product_index<=1:
                    fn=f'{inpath}{year}{datex[4:]}_BBA_combination.tif'
                if product_index==2:
                    fn=f'{inpath}{year}{datex[4:]}/BBA_combination.tif'
                if product_index==3:
                    fn=f'{inpath}{year}/{year}{datex[4:]}_BBA_empirical.tif'
                    
                print(f'cumulate albedo using {fn}')
                test_file = Path(fn)
                if test_file.is_file():
                    # print(fn)
                    band_1x = rasterio.open(fn)
                    profile=band_1x.profile
                    bba=band_1x.read(1)
                    if ((np.shape(bba)[0]==5424)&(np.shape(bba)[1]==3007)):
                        bba[notgl]=np.nan
                        bba[land]=np.nan
                        # !! bba has min of 0 not NaN
                        # v=np.where(~np.isnan(bba))
                        # BBA[v]=bba[v]
                        v=np.where(bba>0.1)
                        # print(np.nanmin(bba),np.nanmax(bba))
                        BBA[v]=bba[v]
                        
                    else:
                        print('bad raster dimensions '+fn)
                    
                    # !! set to 1 for diagnostics
                    do_plot=0
                    
                    if do_plot:
                        plt.close()
                        plt.imshow(BBA,vmin=0.4,vmax=0.9,cmap='viridis')
                        plt.title(f'{year}{datex[4:]}')
                        plt.show()
                        
                else:
                    print(f'no file {year}{datex[4:]}')        
                    if product_index==2:

                        os.system('mkdir -p '+f'{inpath}{year}{datex[4:]}')
                    write_out=1
                    if write_out:
                        temp = BBA.astype(np.float16)
                        if product_index<=1:
                            ofile=f'{inpath}{year}{datex[4:]}_BBA_combination_cum{revname}.tif'                        
                        if product_index==2:
                            ofile=f'{inpath}{year}{datex[4:]}/{year}{datex[4:]}_BBA_combination_cum{revname}.tif'
                        if product_index==3:
                            ofile=f'{inpath}{year}{datex[4:]}_BBA_empirical_cum{revname}.tif'                        

                        # print(ofile)
                        # asas
                        with rasterio.Env():
                            with rasterio.open(ofile, 'w', **profile) as dst:
                                dst.write(temp, 1)
        
                write_out=1
                if write_out:
                    temp = BBA.astype(np.float16)
                    if product_index<=1:
                        ofile=f'{inpath}{year}{datex[4:]}_BBA_combination_cum{revname}.tif'                        
                    if product_index==2:
                        ofile=f'{inpath}{year}{datex[4:]}/{year}{datex[4:]}_BBA_combination_cum{revname}.tif'
                    if product_index==3:
                        ofile=f'{inpath}{year}/{year}{datex[4:]}_BBA_empirical_cum{revname}.tif'                        
                    # print(ofile)
                    # asas
                    profile.update(compress='lzw')

                    with rasterio.Env():
                        with rasterio.open(ofile, 'w', **profile) as dst:
                            dst.write(temp, 1)
                    #     with rio.open(
                    #         ofile,
                    #         'w',
                    #         driver='GTiff',
                    #         height=band_1x.shape[0],
                    #         width=band_1x.shape[1],
                    #         count=1,
                    #         compress='lzw',
                    #         dtype=BBA.dtype,
                    #         # dtype=rasterio.uint8,
                    #         crs=PolarProj,
                    #         # transform=transform,
                    #         ) as dst:
                    #             dst.write(BBA, 1)

print()
print('next code is map_daily_albedo_anomalies')