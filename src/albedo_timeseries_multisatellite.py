#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created May 2024

@author: jason

The May through September 

processing steps:
    1. src/gather_SICE_v2.3.3_or_v3.0_to_tif.py
    2. src/cumulate_SICE_BBA.py
    3. src/map_daily_albedo_anomalies.py map
        ! cum_rev needed to seed 3
    4. src/albedo_timeseries_multisatellite.py
    5. src/plot_daily_alb_timeseries.py


"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
from pyproj import Transformer
import rasterio
import matplotlib.pyplot as plt
from datetime import date, timedelta

if os.getlogin() == 'jason':
    os.chdir('/Users/jason/Dropbox/S3/SICE_anomaly_figs/')
else:
    # !! set to your path
    os.chdir('/Users/jason/Dropbox/S3/SICE_anomaly_figs/')

    
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


def get_msk(fn,product_index):
    msk = rasterio.open(fn).read(1)
    ni = msk.shape[0] ; nj = msk.shape[-1]
    # v = np.where(msk == 1)
    v = np.where(msk > 0)
    land=np.where(msk==1)
    # msk[land]=3
    # plt.imshow(msk)
    ##%%
    # land=np.zeros((ni,nj))*np.nan
    # land[v]=1
    notgl=np.where(msk==0)
    ice=np.where(msk==2)
    # np.shape(msk)
    return msk,notgl,land,ice

def get_basins(fn,product_index):
    basins_raster = rasterio.open(fn).read(1)
    # v = np.where(msk == 1)
    # v = np.where(msk > 0)
    # land=np.where(msk==1)
    # msk[land]=3
    # plt.imshow(basins_raster)
    # plt.colorbar()
    return basins_raster


basin_regions=['SE','NW','CE','CW', 'SW', 'NO', 'NE']

iyear=2017 ; fyear=2023
# iyear=2017 ; fyear=2017
iyear=2025 ; fyear=2025
n_years=fyear-iyear+1
years=np.arange(iyear,fyear+1).astype(int)

do_test=0

raw_data_path='/Users/jason/0_dat/'
# raw_data_path='/Volumes/Lacie/0_dat/'

areax=0.5**2

for product_index in range(5):

    if product_index==1:
        
        if product_index==0:
            sensor='OLCI'
            inpath='/Users/jason/0_dat/S3/opendap/' ; outpath='colocated_AWS_SICE'
            var='albedo_bb_planar_sw'
            ver='Greenland_500m'
            ver2='OLCIv3.0_BSA'
            nj,ni=5424, 3007
            basins_raster=get_basins('/Users/jason/Dropbox/Greenland map/Mouginot_sectors/basins_GrIS_done.tif',product_index)
            msk,notgl,land,ice=get_msk('/ancil/mask_500m_SICE_3.0.tif',product_index)

        if product_index==1:
            sensor='OLCI'
            inpath='/Users/jason/0_dat/S3/opendap/' ; outpath='colocated_AWS_SICE'
            ver='Greenland_500m'
            var='BBA_combination'
            ver2='OLCIv3.0.1'
            nj,ni=5424, 3007
            basins_raster=get_basins('./ancil/basins_GrIS_done.tif',product_index)
            msk,notgl,land,ice=get_msk('./ancil/mask_500m_on_SICE_3.0_grid.tif',product_index)

        if product_index==2:
            sensor='OLCI'
            inpath='/Volumes/LaCie/0_dat/S3/SICE_2.3_1000m/' ; outpath='colocated_AWS_SICE'
            inpath='/Users/jason/0_dat/S3/SICE_2.3_1000m/'
            ver='Greenland_1000m'
            var='BBA_combination'
            ver2='OLCIv2.3.1'
            msk,notgl,land,ice=get_msk('./ancil/mask_1km_on_SICE_2.3.1_grid.tif',product_index)
            basins_raster=get_basins('./ancil/basins_1km_on_SICE_2.3.1_grid.tif',product_index)
            nj,ni=2687, 1487

        divisor=1.
        
        if product_index==3:
            sensor='MODIS'
            inpath=raw_data_path ; outpath='colocated_AWS_'+sensor    
            var='BSA' ; ver='MCD43'
            divisor=1000.
            
        if product_index==4:
            sensor='MODIS'
            inpath=raw_data_path ; outpath='colocated_AWS_'+sensor    
            var='albedo' ; ver='MOD10A1' 
            nj,ni=5444, 3064
            ver2=ver
            msk,notgl,land,ice=get_msk("./ancil/mask_500m_on_MOD10A1_grid.tif",product_index)
            basins_raster=get_basins('./ancil/Mbasins_500m_on_MOD10A1_grid.tif',product_index)

        if product_index==5:
            sensor='AVHRR'
            inpath='/Users/jason/0_dat/APP-x/' ; outpath='colocated_AWS_'+sensor    
            var='albedo' ; ver='APP-x' 
    
        for year in years:
            dates=[]
            for datex in datesx(date(year, 5, 1),date(year, 9, 30)):
                dates.append(datex)
        
            # print(dates)
            
            N_dates=len(dates)
            
            n_test=N_dates
                        
            if do_test:
                n_test=2
            
    
            sentence_list_alb=[]
            sentence_list_BIA=[]
            
            for dd,datex in enumerate(dates[0:n_test]):
                # for dd,datex in enumerate(range(10)):
                # if dd>=1000:
                if dd>=0:
                # if dd==N_dates-1:
                # if datex=='2024-07-16':
                #     print(dd)
                    
            
                        # MODIS data are integer, so divide them by 1000 or 100
                    
                        print('product_index',product_index,sensor,ver,dd,datex)
                    
                        # Path('./data/'+outpath).mkdir(parents=True, exist_ok=True)            
                        # v=np.where(datex==df.time)
                        # i=v[0][0]
                        # print(datex,dd,i)
                     
                        if sensor=='OLCI':
                            if product_index<=1:
                                fn=f"{inpath}{ver}/{datex.split('-')[0]}/{datex}_{var}.tif"
                                if dd==0:
                                    fn=f"{inpath}{ver}/{datex.split('-')[0]}/{datex}_{var}_cum.tif"
                                    cum=np.zeros((nj,ni))
                            else:
                                fn=f"{inpath}{ver}/{datex[0:4]}/{datex}/{datex}_{var}_cum.tif"
                                if dd==0:
                                    fn=f"{inpath}{ver}/{datex[0:4]}/{datex}/{datex}_{var}_cum.tif"
                                    cum=np.zeros((nj,ni))
                                    # print(fn)
                                    # asas
                                    
                        if sensor=='MODIS':
                            # /Users/jason/0_dat/MCD43/Greenland/2022/
                            if year>=2017:
                                fn=f'{inpath}{ver}/Greenland/{datex[0:4]}/{datex}.tif'
                                divisor=100.
                                if dd==0:
                                    fn=f'{inpath}{ver}/Greenland/{datex[0:4]}/{datex}_cum_rev.tif'
                                    cum=np.zeros((nj,ni))
                                if ver=='MCD43':divisor=1000.
    
                            else:
                                datex=datex.replace('-','_')
                                if ver=='MOD10A1':
                                    fn=f'{inpath}{ver}/Greenland/{datex[0:4]}/{datex}_500m_masked.tif'

                                else:
                                    fn=f'{inpath}{ver}/Greenland/{datex[0:4]}/{datex}.Albedo_BSA_shortwave_500m_masked.tif'
                                    
                                divisor=1.
                        if sensor=='AVHRR':
                            fn=f"{inpath}{datex.split('-')[0]}{datex.split('-')[1]}{datex.split('-')[2]}/ArcticLand_{datex.split('-')[0]}{datex.split('-')[1]}{datex.split('-')[2]}0.3.tif"       
                            divisor=1.
    
                        
                        my_file = Path(fn)
                        
                        missing_flag=1

                        if my_file.is_file():
                            # print(product_index,fn)
                            
                            dat = rasterio.open(fn)
                            z = dat.read()[0]/divisor
                            if ver=='MCD43' and year>=2017:
                                z=np.array(z)
                                z[z>1]=np.nan
                            if ver=='MOD10A1' and year>=2017:
                                z=np.array(z)
                                z[z>1]=np.nan
                            
                            # !! some rasters are bad
                            if ((np.shape(z)[0]==5424)&(np.shape(z)[1]==3007)):
                                v=np.where((~np.isnan(z))&(msk==2))
                                cum[v]=z[v]
                            else:
                                print('bad raster dimensions '+fn)
                            cum[cum==0]=np.nan
                            
                            valx_alb=np.zeros(8)
                            valx_BIA=np.zeros(8)
                            
                            # temp=[meanx,std]
                            for basin_index,basin_region in enumerate(basin_regions):
                                # if basin_region=='NO':
                                # if ((basin_region=='CW')or (basin_region=='SW')):
                                # if ((basin_region!='CW')&(basin_region!='SW')):
                                #if basin_region!='all':
                                v=np.where(basins_raster==basin_index+1)
                                valx_alb[basin_index+1]=np.nanmean(cum[v])
                                v=np.where((basins_raster==basin_index+1)&(cum<0.565))
                                valx_BIA[basin_index+1]=len(v[0])*areax
                            valx_alb[0]=np.nanmean(cum[ice])

                            v=np.where((msk==2)&(cum<0.565))
                            valx_BIA[0]=len(v[0])*areax
                            # print(valx_BIA)
                 
                            # std=np.nanstd(cum[ice])
                                    
                                        # temp=np.zeros((5424, 3007))
                                        # print(datex,valx_alb[0],valx_alb[1],valx_alb[2],valx_alb[3],valx_alb[4],valx_alb[5],valx_alb[6],valx_alb[7])
                            missing_flag=0
                            sentence_list_alb.append([valx_alb[0],valx_alb[1],valx_alb[2],valx_alb[3],valx_alb[4],valx_alb[5],valx_alb[6],valx_alb[7],missing_flag])
                            print('      ',datex,valx_alb[7])
                            
                            out_fn=f'/Users/jason/0_dat/S3/daily_basin_scale_albedo/{datex}.csv'
                            out_concept=open(out_fn,'w')
                            out_concept.write(datex+
                                              ',%.3f'%valx_alb[0]+',%.3f'%valx_alb[1] \
                                                    +',%.3f'%valx_alb[2] \
                                                        +',%.3f'%valx_alb[3] \
                                                            +',%.3f'%valx_alb[4] \
                                                                +',%.3f'%valx_alb[5] \
                                                                    +',%.3f'%valx_alb[6] \
                                                                        +',%.3f'%valx_alb[7] 
                                                                      )
                            
                            sentence_list_BIA.append([valx_BIA[0],valx_BIA[1],valx_BIA[2],valx_BIA[3],valx_BIA[4],valx_BIA[5],valx_BIA[6],valx_BIA[7],missing_flag])

                            out_fn=f'/Users/jason/0_dat/S3/daily_basin_scale_BIA/{datex}.csv'
                            out_concept=open(out_fn,'w')
                            out_concept.write(datex+
                                              ',%.3f'%valx_BIA[0]+',%.3f'%valx_BIA[1] \
                                                    +',%.3f'%valx_BIA[2] \
                                                        +',%.3f'%valx_BIA[3] \
                                                            +',%.3f'%valx_BIA[4] \
                                                                +',%.3f'%valx_BIA[5] \
                                                                    +',%.3f'%valx_BIA[6] \
                                                                        +',%.3f'%valx_BIA[7] 
                                                                      )
                            do_plot=0
                            if do_plot:
                                plotvar=cum
                                plotvar[msk!=2]=np.nan
                                plt.close()
                                plt.imshow(plotvar,vmin=0.4,vmax=0.9,cmap='Blues_r')
                                plt.title(datex)
                                plt.colorbar()
                                plt.axis('Off')
                                plt.show()
                            
                        else:
                            # print('no file',datex,fn)

                            sentence_list_alb.append([valx_alb[0],valx_alb[1],valx_alb[2],valx_alb[3],valx_alb[4],valx_alb[5],valx_alb[6],valx_alb[7],missing_flag])
                            sentence_list_BIA.append([valx_BIA[0],valx_BIA[1],valx_BIA[2],valx_BIA[3],valx_BIA[4],valx_BIA[5],valx_BIA[6],valx_BIA[7],missing_flag])

                        # sentence_list_alb.append(valx_alb)
                            
                            
                    # print(dd,datex,refl[:,34,dd])
    
    #%%
    
                # print(v)
            sentence_list_alb=np.array(sentence_list_alb)

            out=pd.DataFrame({
                'date':np.array(dates[0:n_test]).astype(str),
                'all':sentence_list_alb[:,0].astype(float),
                basin_regions[0]:sentence_list_alb[:,1].astype(float),
                basin_regions[1]:sentence_list_alb[:,2].astype(float),
                basin_regions[2]:sentence_list_alb[:,3].astype(float),
                basin_regions[3]:sentence_list_alb[:,4].astype(float),
                basin_regions[4]:sentence_list_alb[:,5].astype(float),
                basin_regions[5]:sentence_list_alb[:,6].astype(float),
                basin_regions[6]:sentence_list_alb[:,7].astype(float),
                'data_gap':sentence_list_alb[:,8].astype(int),
                })
            
            # adjust data precision
            vals=basin_regions
            for val in vals:
                out[val] = out[val].map(lambda x: '%.4f' % x)

            vals=['all']
            for val in vals:
                out[val] = out[val].map(lambda x: '%.4f' % x)
            # fn=f'/Users/jason/Dropbox/albedo_multi_satellite/output/daily/{ver2}_{year}_albedo_daily.csv'
            fn=f'./stats/{ver2}_{year}_albedo_daily.csv'
            out.to_csv(fn,index=None)
            # print(out)

            sentence_list_BIA=np.array(sentence_list_BIA)

            out=pd.DataFrame({
                'date':np.array(dates[0:n_test]).astype(str),
                'all':sentence_list_BIA[:,0].astype(float),
                basin_regions[0]:sentence_list_BIA[:,1].astype(float),
                basin_regions[1]:sentence_list_BIA[:,2].astype(float),
                basin_regions[2]:sentence_list_BIA[:,3].astype(float),
                basin_regions[3]:sentence_list_BIA[:,4].astype(float),
                basin_regions[4]:sentence_list_BIA[:,5].astype(float),
                basin_regions[5]:sentence_list_BIA[:,6].astype(float),
                basin_regions[6]:sentence_list_BIA[:,7].astype(float),
                'data_gap':sentence_list_BIA[:,8].astype(int),
                })
            
            # adjust data precision
            vals=basin_regions
            for val in vals:
                out[val] = out[val].map(lambda x: '%.4f' % x)

            vals=['all']
            for val in vals:
                out[val] = out[val].map(lambda x: '%.4f' % x)
            fn=f'/Users/jason/Dropbox/albedo_multi_satellite/output/daily/{ver2}_{year}_BIA_daily.csv'
            out.to_csv(fn,index=None)
            # print(out)

print()
print('next is plot_daily_alb_timeseries')