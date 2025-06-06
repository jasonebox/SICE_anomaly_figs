# -*- coding: utf-8 -*-
"""
Creation started Mar 28 2023

search below for ##! where you may need to make adjustments

@author: Rasmus Nielsen (rabni@geus.dk) and Jason Box (jeb@geus.dk)

code is to read SICE data from the GEUS Thredds server, main point is to gather just what variables are needed instead of gathering the entire product

dependencies are hopefully satisfied using:
    pip install opendap-protocol
    conda update --all
and
    conda install -c conda-forge netcdf4

Depending on the SICE version, a list of available variables is given here.

v2.3.2 data:
    ['lat',
     'lon',
     'crs',
     'albedo_bb_planar_sw',
     'BBA_combination',
     'diagnostic_retrieval',
     'num_scenes',
     'r_TOA_01',
     'r_TOA_06',
     'r_TOA_17',
     'r_TOA_21',
     'SCDA_final',
     'snow_specific_surface_area']

v3.0 data:
    ['ANG', 'AOD_550', 'O3_SICE', 'al', 'albedo_bb_planar_sw',
    'albedo_bb_spherical_sw', 'albedo_spectral_planar_01',
    'albedo_spectral_planar_02', 'albedo_spectral_planar_03',
    'albedo_spectral_planar_04', 'albedo_spectral_planar_05',
    'albedo_spectral_planar_06', 'albedo_spectral_planar_07',
    'albedo_spectral_planar_08', 'albedo_spectral_planar_09',
    'albedo_spectral_planar_10', 'albedo_spectral_planar_11',
    'albedo_spectral_planar_16', 'albedo_spectral_planar_17',
    'albedo_spectral_planar_18', 'albedo_spectral_planar_19',
    'albedo_spectral_planar_20', 'albedo_spectral_planar_21',
    'cloud_mask', 'crs', 'cv1', 'cv2', 'factor', 'grain_diameter',
    'isnow', 'lat', 'lon', 'r0', 'rBRR_01', 'rBRR_02', 'rBRR_03',
    'rBRR_04', 'rBRR_05', 'rBRR_06', 'rBRR_07', 'rBRR_08', 'rBRR_09',
    'rBRR_10', 'rBRR_11', 'rBRR_16', 'rBRR_17', 'rBRR_18', 'rBRR_19',
    'rBRR_20', 'rBRR_21', 'r_TOA_01', 'r_TOA_02', 'r_TOA_03',
    'r_TOA_04', 'r_TOA_05', 'r_TOA_06', 'r_TOA_07', 'r_TOA_08',
    'r_TOA_09', 'r_TOA_10', 'r_TOA_11', 'r_TOA_12', 'r_TOA_13',
    'r_TOA_14', 'r_TOA_15', 'r_TOA_16', 'r_TOA_17', 'r_TOA_18',
    'r_TOA_19', 'r_TOA_20', 'r_TOA_21', 'saa',
    'snow_specific_surface_area', 'sza', 'threshold', 'vaa', 'vza']

"""

import xarray as xr
from pyproj import CRS,Transformer
import os
import numpy as np
from rasterio.transform import Affine
import rasterio as rio
import rasterio
from pathlib import Path
from datetime import date, timedelta
import datetime

if os.getlogin() == 'jason':
    base_path='/Users/jason/Dropbox/S3/SICE_anomaly_figs/'
    output_base_path = '/Users/jason/0_dat/S3/opendap/'
else:
    # !! set to your path
    base_path='/Users/jason/Dropbox/S3/SICE_anomaly_figs/'
    output_base_path = '/Users/jason/0_dat/S3/opendap/'

os.chdir(base_path)

##! choose a data version
version_index=1
resolution=['1000','500']
version_number=['2.3.2','3.']
##! choose a region

region='Greenland'

# projection info
# WGSProj = CRS.from_string("+init=EPSG:4326") # source projection
# PolarProj = CRS.from_string("+init=EPSG:3413") # example of an output projection
WGSProj = CRS.from_string("EPSG:4326") # source projection
PolarProj = CRS.from_string("EPSG:3413") # example of an output projection
wgs_data = Transformer.from_proj(WGSProj, PolarProj) 

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

def ExportGeoTiff(x,y,z,crs,path):
    
    "Input: xgrid,ygrid, data paramater, the data projection, export path, name of tif file"
    
    resx = (x[1] - x[0])
    resy = (y[1] - y[0])
    transform = Affine.translation((x[0]),(y[0])) * Affine.scale(resx, resy)
    
    # z[z>1.1]=np.nan
    with rio.open(
        path,
        'w',
        driver='GTiff',
        height=z.shape[0],
        width=z.shape[1],
        count=1,
        compress='lzw',
        dtype=z.dtype,
        # dtype=rasterio.uint8,
        crs=crs,
        transform=transform,
        ) as dst:
            dst.write(z, 1)
    
    return None 

##! choose year range
years=np.arange(2025,2026).astype(str)
 
for year in years:

    ##! choose date range
    d = datetime.datetime.today() - timedelta(days=1)
    m=int(d.strftime('%m'))
    day_minus_1=int(d.strftime('%d'))
    d = datetime.datetime.today() - timedelta(days=2)
    day_minus_2=int(d.strftime('%d'))
    d = datetime.datetime.today() - timedelta(days=3)
    day_minus_3=int(d.strftime('%d'))
    m_minus_3=int(d.strftime('%m'))
    d = datetime.datetime.today() - timedelta(days=9)
    day_minus_9=int(d.strftime('%d'))
    m_minus_9=int(d.strftime('%m'))
    day_minus_9=int(d.strftime('%d'))
    dates=datesx(date(int(year), m_minus_9, day_minus_9),date(int(year), m, day_minus_1))    # dates=datesx(date(2023, 7, 12),date(2023, 7, 12))
    # dates=datesx(date(int(year), m_minus_3, day_minus_3),date(int(year), m, day_minus_1))    # dates=datesx(date(2023, 7, 12),date(2023, 7, 12))

    # dates=datesx(date(int(year), 4, 20),date(int(year), 5, 11))

    print(f'dates to gather {dates}')
    ##! choose what bands you need
  
    bands=['BBA_combination']
    
    # ############### main code
    
    
    output_path=f'/Users/jason/0_dat/S3/opendap/{region}_{resolution[version_index]}m/'
    if not(os.path.exists(output_path) and os.path.isdir(output_path)):
        os.makedirs(output_path)
    output_path=f'/Users/jason/0_dat/S3/opendap/{region}_{resolution[version_index]}m/'+ year + os.sep
    if not(os.path.exists(output_path) and os.path.isdir(output_path)):
        os.makedirs(output_path)
        
    # loop over dates
    for d in dates:
        if version_index==0:
            DATASET_ID = f'SICEv2.3.2_{region}_1000m_daily{d}.nc'
        else:
            # DATASET_ID = 'sice_500_' + d.replace('-', '_') + '.nc'
            DATASET_ID = f'SICEv3.0_{region}_500m_{d}.nc'
            # SICE_500m/Greenland/SICEv3.0_Greenland_500m_2024_04_15.nc
            DATASET_ID = f'SICEv3.0_{region}_500m_{d}.nc'


        # print(d)

        for var in bands:
            ofile=output_path + d + '_' + var + '.tif'
            test_file = Path(ofile)
            print(f'{d} {var}')


            if not(test_file.is_file()):
                fn=f'https://thredds.geus.dk/thredds/dodsC/SICE_{resolution[version_index]}m/{region}/{DATASET_ID}'                
                # print(fn)
                # ds = xr.open_dataset(fn)
                
                try:
                    print('    gathering')

                    ds = xr.open_dataset(fn)
                    # ds.variables
                    # list(ds.keys())
                    yshape,xshape = np.shape(ds[var])
                    
                    if version_index:
                        if yshape != 5424: 
                            ds = ds.rename({'x2':'xcoor'})
                            ds = ds.rename({'y2':'ycoor'})        
                        else:
                            ds = ds.rename({'x':'xcoor'})
                            ds = ds.rename({'y':'ycoor'})
                        # print(yshape)
                        
                        data = ds[var]#.sel(ycoor=y_slice,xcoor=x_slice)
                        x = ds['xcoor']#.sel(xcoor=x_slice)
                        y = ds['ycoor']#.sel(ycoor=y_slice)
                    else:
                        x = ds['x']#.sel(xcoor=x_slice)
                        y = ds['y']#.sel(ycoor=y_slice)
                                            
                    # print(np.shape(ds[var]))
                    # data = data.where(data <= plotting_dict[v]['maxval'])
                    # data = data.where(data >= plotting_dict[v]['minval'])
                    
                    # z = data.to_numpy()
                    # x = x.to_numpy()
                    # y = y.to_numpy()
    
                    z = ds[var].to_numpy()
                    x = x.to_numpy()
                    y = y.to_numpy()
                                # 
                    ExportGeoTiff(x, y, z, PolarProj, ofile)
                    
                    ds.close()
            
                except:
                    print('   no such data to gather on this server')
            else:
                print('   local file already exists')

print()
print('next code is cumulate_SICE_BBA.py')