#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 08:22:17 2024

@author: jason

processing steps:
    1. src/gather_SICE_v2.3.3_or_v3.0_to_tif.py
    2. src/cumulate_SICE_BBA.py
    3. src/map_daily_albedo_anomalies.py map
        ! cum_rev needed to seed 3
    4. src/albedo_timeseries_multisatellite.py
    5. src/plot_daily_alb_timeseries.py


"""

from PIL import Image
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import date
import matplotlib.dates as mdates

today = date.today()

if os.getlogin() == 'jason':
    os.chdir('/Users/jason/Dropbox/S3/SICE_anomaly_figs/')
else:
    # !! set to your path
    os.chdir('/Users/jason/Dropbox/S3/SICE_anomaly_figs/')

# graphics definitions
th=2 # line thickness
formatx='{x:,.3f}' ; fs=18
plt.rcParams["font.size"] = fs
plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams['axes.grid'] = False
# plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.23
plt.rcParams['grid.color'] = "k"
plt.rcParams["legend.facecolor"] ='w'
plt.rcParams["mathtext.default"]='regular'
plt.rcParams['grid.linewidth'] = th/2
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['legend.fontsize'] = fs*0.8

basin_regions=['SE','NW','CE','CW', 'SW', 'NO', 'NE']

BIA_or_alb=1

for BIA_or_alb in range(2):
    if BIA_or_alb==0:
        varnam='albedo'
        ytit='albedo, dimensionless'
        
        if BIA_or_alb:
            varnam='BIA'
            ytit='bare ice area, x1000 km$^{2}$'
            
        iyear=2017 ; fyear=2025
        # iyear=2017 ; fyear=2023
        # iyear=2017 ; fyear=2024
        n_years=fyear-iyear+1
        years=np.arange(iyear,fyear+1).astype(int)
        
        
        plt.close()
        
        fig, ax = plt.subplots(figsize=(9, 9))
        
        colors = ['purple','b', 'darkorange', 'c', 'k','grey','darkorange','r']
        colors = ['y','purple', 'r', 'c', 'm','grey','darkorange','b','b']
        
        region='all'
        # region='SW'
        
        means=np.zeros(366)
        stds=np.zeros(366)
        # statvar=np.zeros((n_years,366))
        statvar=np.zeros((n_years-1,153))
        
        product='OLCIv3.0.1'
        # product='MOD10A1'
        
        for yy,year in enumerate(years):
            opath="./stats/"
            df=pd.read_csv(f'{opath}{product}_{year}_{varnam}_daily.csv')
            if BIA_or_alb==0:
                # if year==2018:
                    # df['all'][df.date=='2018-06-19']=0.8
                    # df['all'][df.date=='2018-06-18']=0.8
                    # df['all'][df.date=='2018-06-17']=0.8
                if year==2019:
                    # df['all'][df.date=='2019-06-19']=135000
                    df['all'][df.date=='2019-07-08']=0.72
        
            if BIA_or_alb:
                if year==2017:
                    df['all'][df.date=='2017-08-20']=np.nan
                    df['all'][df.date=='2017-08-21']=np.nan
                if year==2019:
                    df['all'][df.date=='2019-06-19']=135000
                    df['all'][df.date=='2019-07-08']=195000
            df["date"] = pd.to_datetime(df['date'])
            if yy==n_years-1:
                v=np.where(df.data_gap==0)
                last_date=pd.to_datetime(df["date"][v[0][-1]])
            # df['year'] = pd.DatetimeIndex(df["date"]).year
            df['month'] = pd.DatetimeIndex(df["date"]).month
            df['day'] = pd.DatetimeIndex(df["date"]).day
            # # df['hour'] = pd.DatetimeIndex(df["date"]).hour
            df['doy'] = pd.DatetimeIndex(df["date"]).dayofyear
            df['year'] = 2001
            # df[region]*=100
            
            dummy_datetime = pd.to_datetime(df[['year', 'month', 'day']])
        
            # df.index = pd.to_datetime(df.date)
            # t0=datetime(int(year),5,1) ; t1=datetime(int(year),9,30)
        
            
            # y=refl
            # ax.plot(df['all'][t0:t1],'-s',color=colors[yy],label=year)
            df[region][df.data_gap==1]=np.nan
        
            # for dd in range(366):
            indexes=df.doy.values-df.doy[0]
            if yy<n_years-1:
                statvar[yy,indexes]=df[region][indexes]
        
            th=1
            if year==2024:
                th=2
            plot_years=[2019,2018,2025]
            # plot_years=[2018,2019,2020,2021,2022,2024]
            for yearx in plot_years:
                dev=1
                if BIA_or_alb:
                    dev=1000
                if year==yearx:ax.plot(dummy_datetime,df[region]/dev,'-',color=colors[yy],linewidth=th*2,label=year)
            
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center',fontsize=fs)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        
        means=np.nanmean(statvar,axis=0)
        stds=np.nanstd(statvar,axis=0)
        # means[-2:]=np.nan
        if BIA_or_alb:
            means/=1000
            stds/=1000
            
        co='k'
        ax.plot(dummy_datetime,means,'-',color=co,linewidth=th*2,label='daily averages\n 2017 to 2023')
        # ax.plot(dummy_datetime,means-stds,'--',color=co,linewidth=th*1)
        # ax.plot(dummy_datetime,means+stds,'--',color=co,linewidth=th*1)
        
        means_plus=means+stds
        means_minus=means-stds
        d = dummy_datetime.values
        plt.fill_between(d, means_minus, means_plus,
                        where=means_minus >= means_minus,
                        facecolor='k', alpha=0.2, interpolate=True,label='daily 1 st. dev.\nfrom 2017 to 2023')
        
        ax.set_xlim(date(2001, 5, 1),date(2001, 9, 28))
        ax.set_xlim(date(2001, 5, 1),date(2001, 9, 15))
        
        # plt.title(f'Greenland snow and ice reflectivity until '+today.strftime('%d %b %Y'))
        # plt.title('Greenland snow and ice reflectivity')#' from {product}')
        # plt.ylim(65,96)
        # plt.ylabel('%')
        plt.ylabel(ytit)
        # plt.legend()
        plt.legend(frameon=False)
        
        # ----------- annotation
        xx0=1.02 ; yy0=1.08 # expand plot area UR
        ax.text(xx0, yy0, 'o',color='w',rotation=0,
                transform=ax.transAxes,zorder=20,va='top',ha='left') # ,bbox=props 
        
        xx0=-0.13 ; yy0=-0.16 # expand plot area LL
        ax.text(xx0, yy0, 'o',color='w',rotation=0,
                transform=ax.transAxes,zorder=20,va='top',ha='left') # ,bbox=props 
        
        # mult=0.8
        # xx0=0.6 ; yy0=0.05
        # ax.text(xx0, yy0, 'latest data: '+last_date.strftime('%b %d %Y'),color='grey',rotation=0,
        #         transform=ax.transAxes,zorder=20,va='top',ha='left',fontsize=fs*mult)
        
        
        ly='x'
        
        if ly == 'x':plt.show()
        
        
        if ly == 'p':
            
            
            fancy=0
            

        
            today = date.today()
            figpath='./Figs/timeseries/'
            fignam = figpath + today.strftime('%Y-%m-%d') + product +f"_{varnam}.png"
            
            if fancy:
                plt.savefig(
                    "/tmp/tmp.png",
                    # pad_inches=0.1,
                    bbox_inches="tight",
                    # figsize=(figx, figy),
                    # type="png",
                    dpi=200,
                    facecolor="w",
                )
                
                im1 = Image.open("/tmp/tmp.png", "r")
                width, height = im1.size
                border = 20
                # Setting the points for cropped image
                left = border
                top = border
                right = width - border
                bottom = height - border
                
                # Cropped image of above dimension
                im1 = im1.crop((left, top, right, bottom))
                back_im = im1.copy()
                
                yy0 = 1200 ; xos = 1100
                fn = "./ancil/SICE_logo.png"
                SICE_logo = Image.open(fn, "r")
                sice_pixel_size = 170
                size = sice_pixel_size, sice_pixel_size
                SICE_logo.thumbnail(size, Image.Resampling.LANCZOS)
                back_im.paste(SICE_logo, (xos, yy0))  # ), msk=SICE_logo)
                
                # yy0=1000 ; xos=350
                fn = "./ancil/PTEP_logo.png"
                ptep_pixel_size = 250
                size = ptep_pixel_size, ptep_pixel_size
                PTEP_logo = Image.open(fn, "r")
                PTEP_logo.thumbnail(size, Image.Resampling.LANCZOS)
                back_im.paste(PTEP_logo, (xos + 200, yy0 + 27), mask=PTEP_logo)
                
                back_im.save(fignam, optimize=True, quality=95)
                # os.system('open '+ofile)
            else:
                plt.savefig(
                    fignam,
                    # pad_inches=0.1,
                    bbox_inches="tight",
                    # figsize=(figx, figy),
                    # type="png",
                    dpi=200,
                    facecolor="w",
                )
            
            # os.system('open '+fignam)
        