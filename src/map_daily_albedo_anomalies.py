#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 10:07:20 2024

@author: jason

processing steps:
    1. src/gather_SICE_v2.3.3_or_v3.0_to_tif.py
    2. src/cumulate_SICE_BBA.py
    3. src/map_daily_albedo_anomalies.py map
        ! cum_rev needed to seed 3
    4. src/albedo_timeseries_multisatellite.py
    5. src/plot_daily_alb_timeseries.py

search throughout for "!!" for clues what needs attention

"""
from PIL import Image
import numpy as np
import rasterio
import os
# import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from calendar import monthrange
import calendar
import datetime
from datetime import date, timedelta

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

if os.getlogin() == 'jason':
    base_path='/Users/jason/Dropbox/S3/SICE_anomaly_figs/'
    path_SICE_data_gathered_from_thredds='/Users/jason/0_dat/S3/opendap/Greenland_500m/'
else:
    # !! set to your path
    base_path='/Users/jason/Dropbox/S3/SICE_anomaly_figs/'
    path_SICE_data_gathered_from_thredds='/Users/jason/0_dat/S3/opendap/Greenland_500m/'
    
os.chdir(base_path)

automation=0 # !! set to 1 for dates to be selected automatically

msk_file="./ancil/mask_500m_on_SICE_3.0_grid.tif"
msk = rasterio.open(msk_file).read(1)
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
np.shape(msk)


current_year=2025
anom_year=current_year

   
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

do_ftp=0

# multi-year mean

years=np.arange(2017,2025).astype(str)

revname=''

# reverse cumulation
do_rev=0

# revname='_rev'
if do_rev:
    dates=dates[::-1]
    print(dates)
    revname='_rev'

for datex in dates:
    # dates=datesx(date(int(year), 7, 19),date(int(year), 7, 19))

    anom=np.zeros((5424, 3007))
    # count=np.zeros((5424, 3007))
    anom[notgl]=np.nan
    anom[land]=np.nan

    meanx=np.zeros((5424, 3007))

    cc=0
    for yearx in np.arange(2017,current_year).astype(str):
        fn=f'{path_SICE_data_gathered_from_thredds}{yearx}/{yearx}{datex[4:]}_BBA_combination_cum{revname}.tif'
        print(fn)
        band_1x = rasterio.open(fn)
        # profile=band_1x.profile
        # profile=band_1x.profile
        bba=band_1x.read(1)
        meanx+=bba
        cc+=1
    meanx/=cc
    meanx[notgl]=np.nan
    meanx[land]=np.nan
    do_plot=0
    
    if do_plot:
        plt.imshow(meanx,vmin=0.4,vmax=0.95,cmap='Blues_r')
        plt.title(f'mean 2017 to 2023 {datex[5:]}')
        plt.colorbar()
        plt.show()

#%% compute anom
    revname=''
    fn=f'{path_SICE_data_gathered_from_thredds}/{anom_year}/{anom_year}{datex[4:]}_BBA_combination_cum{revname}.tif'
    # fn=f'/Users/jason/0_dat/S3/opendap/Greenland_500m/{anom_year}/{anom_year}{datex[4:]}_BBA_combination.tif'
    print(fn)
    band_1x = rasterio.open(fn)
    bba_anom_year=band_1x.read(1)

    do_plot=0
    if do_plot:
        plt.close()
        plt.imshow(bba_anom_year)
        plt.colorbar()
        plt.title(f'{anom_year}{datex[4:]}')
    #%%
    BBAc_anomaly=bba_anom_year-meanx
    # BBAc_anomaly[BBAc_anomaly<-0.2]=np.nan
    do_plot=0
    
    if do_plot:
        lo=-0.1 ; hi=-lo
        plt.close()
        plt.imshow(BBAc_anomaly,vmin=lo,vmax=hi,cmap='bwr_r')
        # plt.title(f'mean 2017 to 2023 {datex[5:]}')
        plt.colorbar()
        plt.title(f'{anom_year}{datex[4:]}')
        plt.show()

#%% plot anom

    font_size = 12  # JB
    
    # plt.rcParams['font.sans-serif'] = ['Georgia']
    
    params = {
        "legend.fontsize": font_size,
        # 'figure.figsize': (15, 5),
        "axes.labelsize": font_size,
        "axes.titlesize": font_size,
        "xtick.labelsize": font_size,
        "ytick.labelsize": font_size,
        "ytick.color": "k",
        "xtick.color": "k",
        "axes.labelcolor": "k",
        "axes.edgecolor": "k",
        "figure.facecolor": "w",
        "axes.grid": True,
    }
    plt.rcParams.update(params)
    
    
    msk_file="./ancil/mask_500m_on_SICE_3.0_grid.tif"
    msk = rasterio.open(msk_file).read(1)
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
    np.shape(msk)
    
    
    # land = np.where(msk==1)
    ice = np.where(msk == 2)
    
    ni = msk.shape[0]
    nj = msk.shape[-1]
    

    # make map
    my_cmap = plt.colormaps["bwr_r"]
    my_cmap.set_under("#AA7748")  #  brown, land
    
    # dates=datesx(date(int(anom_year), 5, 6),date(int(anom_year), 5, 6))
    
    datexx=pd.to_datetime(datex)
    day=datexx.strftime('%d')
    month=datexx.strftime('%m')
    yearx=datexx.strftime('%Y')

    day_float = int(day)
    monthinteger = int(month)
    n_days_per_month = monthrange(int(yearx), monthinteger)
    month_name = datetime.date(1900, monthinteger, 1).strftime("%B")

    do_progress_pie=1
    if do_progress_pie:
        # ---------------------------- progress pie

    
        frac = day_float / n_days_per_month[1]
        sizes = [1 - frac, frac]
        plt.clf()
    
        fig1, ax1 = plt.subplots(figsize=(1.5, 1.5))
        pie_colours = ["w", "thistle"]
        ax1.pie(sizes, startangle=90, colors=pie_colours)
        ax1.set_title(month_name, fontsize=20)
        ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        circle_fig = "/tmp/" + yearx + month + day + "_circle.png"
        plt.savefig(circle_fig, bbox_inches="tight", dpi=100, transparent=True)
        # os.system('open '+circle_fig)
        plt.close()

    # fig, ax = plt.subplots(figsize=(16, 12))
    fig, ax = plt.subplots(figsize=(7, 6))
    plt.clf()
    # plt.figure()
    hi = 0.1
    lo = -hi
    BBAc_anomaly[land] = -1
    BBAc_anomaly[((BBAc_anomaly < lo) & (msk > 1))] = lo
    BBAc_anomaly[((BBAc_anomaly > hi) & (msk > 1))] = hi
    # BBAc_anomaly[((BBAc_anomaly < lo) & (msk > 1))] = 0
    # BBAc_anomaly[((BBAc_anomaly > hi) & (msk > 1))] = 0

    # BBAc_anomaly[((BBAc_anomaly < lo) & (msk > 1))] = np.nan
    # BBAc_anomaly[((BBAc_anomaly > hi) & (msk > 1))] = np.nan
    plt.imshow(BBAc_anomaly, cmap=my_cmap)
    # plt.title(date, fontsize=20)
    plt.axis("off")

    # -------------------------------------------------- date
    xx0 = 0.44
    yy0 = 0.99
    dy = -0.04
    cc = 0
    mult = 0.95  # JB
    xx0 = 0.53
    yy0 = 0.99
    dy = -0.04
    cc = 0
    mult = 0.75  # JB shell

    txt = yearx+"," + " " + calendar.month_name[int(month)] + " " + day
    plt.text(
        xx0,
        yy0 + cc * dy,
        txt,
        fontsize=font_size * mult,
        color="k",
        transform=ax.transAxes,
        va="top",
    )
    cc += 1.0
    # -------------------------------------------------- upper right title
    xx0 = 0.9
    dy = -0.04
    cc = 0
    mult = 0.7

    txt = "albedo\nanomaly:"
    plt.text(
        xx0,
        yy0 + cc * dy,
        txt,
        fontsize=font_size * mult,
        color="k",
        transform=ax.transAxes,
        va="top",
    )
    cc += 2.0

    txt = yearx+f" minus the\n2017-{current_year-1} average"
    plt.text(
        xx0,
        yy0 + cc * dy,
        txt,
        fontsize=font_size * 0.6,
        color="b",
        transform=ax.transAxes,
        va="top",
    )
    cc += 2.0

    # -------------------------------------------------- sat info
    xx0 = 0.77
    yy0 = 0.25
    dy = -0.03
    cc = 0
    mult = 0.7

    xx0 = 0.82
    yy0 = 0.22
    dy = -0.03
    cc = 0
    mult = 0.6
    box_dy = 0.05
    color_code = "#6CE577"
    color_code = "#6AD8EA"
    color_code = "grey"

    plt.text(
        xx0,
        yy0 + cc * dy,
        # 'via Kokhanovsky et al 2020', fontsize=font_size*mult,
        "polarportal.dk",
        fontsize=font_size * mult,
        transform=ax.transAxes,
        color=color_code,
    )
    cc += 1.0
    plt.text(
        xx0,
        yy0 + cc * dy,
        "ESA EO Science for Society",
        fontsize=font_size * mult,
        color=color_code,
        transform=ax.transAxes,
    )
    cc += 1.0
    plt.text(
        xx0,
        yy0 + cc * dy,
        "SICE, snow.geus.dk ",
        fontsize=font_size * mult,
        color=color_code,
        transform=ax.transAxes,
    )
    cc += 1.0
    # plt.text(xx0, yy0+cc*dy, '@climate_ice',
    # if cumulate:
    #     plt.text(xx0, yy0+cc*dy,
    #          'gapless', fontsize=font_size*mult*0.8,
    #          transform=ax.transAxes,color='gold') ; cc+=1.
    # plt.text(xx0, yy0+cc*dy, 'J. Box, A. Wehrlé, B. Vandecrux, K. Mankoff',
    #          fontsize=font_size*mult*0.8,color='w',transform=ax.transAxes)

    # --------------------------------------------------------------- colorbar

    clb = plt.colorbar(
        fraction=0.017, orientation="vertical", pad=0.005
    )  # , extend='both')
    clb.ax.set_title("       unitless", fontsize=font_size * 0.5, c="k")
    clb.ax.tick_params(labelsize=7)  # ,horizontalalignment='center')

    plt.clim(lo, hi)

    # https://stackoverflow.com/questions/13714454/specifying-and-saving-a-figure-with-exact-size-in-pixels

    figpath='./Figs/'
    # os.system("mkdir -p " + figpath)

    # figx, figy = 16, 12
    # figx,figy=16*2,12*2
    plt.savefig(
        "/tmp/tmp.png",
        bbox_inches="tight",
        # figsize=(figx, figy),
        # type="png",
        dpi=300,
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

    yy0 = 990 ; xos = 400
    yy0 = 1200 ; xos = 500
    fn = "./ancil/SICE_logo.png"
    SICE_logo = Image.open(fn, "r")
    pixelsx = 130
    size = pixelsx, pixelsx
    SICE_logo.thumbnail(size, Image.Resampling.LANCZOS)
    back_im.paste(SICE_logo, (xos, yy0))  # ), msk=SICE_logo)

    # yy0=1000 ; xos=350
    fn = "./ancil/PTEP_logo.png"
    pixelsx = 180
    size = pixelsx, pixelsx
    PTEP_logo = Image.open(fn, "r")
    PTEP_logo.thumbnail(size, Image.Resampling.LANCZOS)
    back_im.paste(PTEP_logo, (xos + 170, yy0 + 27), mask=PTEP_logo)

    # ---------------------------- progress pie
    im_pie = Image.open(circle_fig)
    pp_yy0 = 900 ; pp_xx0 = 580
    back_im.paste(im_pie, (pp_xx0, pp_yy0), mask=im_pie)

    fignam = datex + "_anom"

    ofile = figpath + fignam + ".png"
    back_im.save(ofile, optimize=True, quality=95)
    print(f'saving {ofile}')
    ofile = figpath + "sm_" + fignam + ".png"
    size = 1080, 1080
    back_im.thumbnail(size, Image.Resampling.LANCZOS)
    back_im.save(ofile, optimize=True, quality=95)

    # os.system('open '+ofile)

    languages = ["EN", "DK"]
    # languages = ["EN"]

    # ===========================================================================================
    for ll, language in enumerate(languages):
        # for ll,language in enumerate(languages[0:1]): # for development
        # print(ll)

        # language_string='EN'
        # anomaly_string='albedo anomaly'
        # period_string='same period'
        # sunlight_string='insufficient!Csunlight'
        # to_string='to'

        # if ll:
        #   language_string='DK'
        #   anomaly_string='albedoanomali'
        #   period_string='samme periode'
        #   sunlight_string='For lidt!Csollys'
        #   to_string='til'
        YMD = datex.replace("-", "")
        size = 1080, 1080
        back_im.save(
            figpath + "Alb_LG_" + language + "_" + YMD + ".png",
            optimize=True,
            quality=95,
        )

        back_im.save(
            figpath + "Alb_LG_" + language + ".png",
            optimize=True,
            quality=95,
        )

        size = 602, 602
        back_im.thumbnail(size, Image.Resampling.LANCZOS)
        back_im.save(
            figpath + "Alb_SM_" + language + "_" + YMD + ".png",
            optimize=True,
            quality=95,
        )
        back_im.thumbnail(size, Image.Resampling.LANCZOS)

        nam=figpath + "Alb_SM_" + language + ".png"
        back_im.save(nam, optimize=True, quality=95)

        # if ll == 0:
        #     back_im.save(
        #         figpath + "Alb_SM_" + language + "_latest.png",
        #         optimize=True,
        #         quality=95,
        #     )

        # os.system('open '+ figpath + "Alb_LG_" + language + "_" + YMD + ".png")
        
        if do_ftp:
            msg = (
                "curl -T "
                + figpath
                + "Alb_LG_"
                + language
                + "_"
                + YMD
                + ".png ftp://0573dmi:Arc516d@ftpserver.dmi.dk/upload/"
            )
            print(msg)
            os.system(msg)
    
            msg = (
                "curl -T "
                + figpath
                + "Alb_SM_"
                + language
                + "_"
                + YMD
                + ".png ftp://0573dmi:Arc516d@ftpserver.dmi.dk/upload/"
            )
            print(msg)
            os.system(msg)
    
            msg = (
                "curl -T "
                + figpath
                + "Alb_LG_"
                + language
                + ".png ftp://0573dmi:Arc516d@ftpserver.dmi.dk/upload/"
            )
            print(msg)
            os.system(msg)
    
            msg = (
                "curl -T "
                + figpath
                + "Alb_SM_"
                + language
                + ".png ftp://0573dmi:Arc516d@ftpserver.dmi.dk/upload/"
            )
            print(msg)
            os.system(msg)
print()
print('next is albedo_timeseries_multisatellite.py')