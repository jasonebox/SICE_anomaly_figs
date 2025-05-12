# -*- coding: utf-8 -*-
"""

@author: Jason Box and Adrien Wehrlé, GEUS (Geological Survey of Denmark and Greenland)

"""

from PIL import Image
import numpy as np
# import glob
import rasterio
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
# import pandas as pd
# from calendar import monthrange
# import calendar
# import datetime


class MidpointNormalize(mpl.colors.Normalize):
    """Normalise the colorbar."""

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        mpl.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))


# setting paths
figpath = "/Users/jason/Dropbox/S3/SICE_anomaly_figs/Figs/2024/"

os.makedirs(figpath, exist_ok=True)

font_size = 24  # JB
# font_size = 12  # JB

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
    "axes.grid": False,
}
plt.rcParams.update(params)


# maskfile = "/Users/jason/Dropbox/S3/ancil/SICE/mask_1km_1487x2687.tif"
maskfile = "/Users/jason/Dropbox/S3/SICE_ESSD/ancil/mask_500m_on_SICE_3.0_grid.tif"
msk = rasterio.open(f"{maskfile}").read(1)
msk[msk > 2] = 2
land = np.where(msk == 1)
ocean = np.where(msk == 0)
# msk[msk>2]=2
# plt.imshow(msk)
# plt.colorbar()


# land = np.where(msk==1)
ice = np.where(msk == 2)
notgl = np.where(msk == 0)

ni = msk.shape[0]
nj = msk.shape[-1]
land=np.zeros((ni,nj))*np.nan
# %% get available 2022 NRT dates to load associated years



    # date = SICE_NRT_file.split(os.sep)[-1].split(".")[0]

    # month = date[5:7]
    # day = date[8:10]

    # fignam = date + "_anom"
    # ofile = figpath + fignam + ".png"

    # if os.path.exists(fignam):
    #     continue

    # try:
    #     BBAc_NRT = rasterio.open(SICE_NRT_file).read(1)
    # except:
    #     continue
    
    # date_dt = pd.to_datetime(date)

    # date_ft = date_dt.strftime("%m-%d")

    # av_filename = f"{SICE_av_data}/{date_ft}.tif"

    # try:
    #     five_year_average = rasterio.open(av_filename).read(1)
    # except rasterio.errors.RasterioIOError:
    #     continue

varchoices=['anom','ave']
# varchoices=['ave','2023']
varchoices=['anom']
band='BBA_combination'
period='2017-2023'
season='JJA'
season='08'

for i,varchoice in enumerate(varchoices):
    
    
    # BBA_clim = rasterio.open('/Users/jason/0_dat/S3/SICE_2023Adrien/SICE_albedo_july_2017_2022.tiff').read(1)
    # BBA = rasterio.open('/Users/jason/0_dat/S3/SICE_2023Adrien/SICE_albedo_july_2023.tiff').read(1)
    if season=='JJA':
        BBA_clim = rasterio.open(f'/Users/jason/0_dat/S3/seasonal/BBA_combination_cum_{period}_JJA.tif').read(1)
        BBA = rasterio.open(f'/Users/jason/0_dat/S3/seasonal/{band}_cum_2024_JJA.tif').read(1)
    else:
        BBA_clim = rasterio.open(f'/Users/jason/0_dat/S3/seasonal/BBA_combination_cum_{period}_{season}.tif').read(1)
        BBA = rasterio.open(f'/Users/jason/0_dat/S3/monthly/{band}_cum_2024-{season}.tif').read(1)

    if varchoice=='anom':
        BBAc_anomaly = BBA - BBA_clim
        wo=1
        if wo:
            outpath='/Users/jason/0_dat/S3/seasonal/'
            profile_file='/Users/jason/0_dat/S3/opendap/Greenland_500m/2018/2018-06-22_r_TOA_01.tif'
            temp = rasterio.open(profile_file)
            profile=temp.profile
    
            ofile=f'{outpath}{band}_{season}_2024_vs_2017-2023.tif'
    
            with rasterio.Env():
                with rasterio.open(ofile, 'w', **profile) as dst:
                    dst.write(BBAc_anomaly, 1)

        my_cmap = plt.cm.get_cmap('seismic_r')
        plt.imshow(BBAc_anomaly,cmap=my_cmap,vmin=-0.1,vmax=0.1)
        # plt.imshow(BBA)
        # plt.colorbar()
        # plt.show()

        plotvar=BBAc_anomaly
        hi= 0.1
        lo= -hi
        # txt = "albedo anomaly\nJuly 2023"
        txt = "albedo anomaly\nJune through August 2024"
        fignam='anom_JJA_2024_vs_2017-2023'

    if varchoice=='2023':
        my_cmap = plt.cm.get_cmap('Blues_r')
        plotvar=BBA
        txt = "albedo\nJuly 2023"
        fignam='albedo_072023'
        period='2023'
        band=""

    if varchoice=='ave':
        my_cmap = plt.cm.get_cmap('Blues_r')
        plotvar=BBA_clim
        txt = "albedo\nJuly 2023"
        fignam='albedo_072023'
        band=""

    
    # hi= 0.9
    # lo= 0.35
    # plt.imshow(BBA,cmap=my_cmap,vmin=lo,vmax=hi)
        
    # plt.colorbar()
    land[(np.isnan(plotvar)&(msk>0))]=1

        # make map
    

    # plt.imshow(land)
    # plt.colorbar()
    plotvar[land==1]=-2
    
        # # ---------------------------- progress pie
        # day_float = int(day)
        # monthinteger = int(month)
        # n_days_per_month = monthrange(int(yearx), monthinteger)
        # month_name = datetime.date(1900, monthinteger, 1).strftime("%B")
    
        # frac = day_float / n_days_per_month[1]
        # sizes = [1 - frac, frac]
    plt.clf()
    
    # fig1, ax1 = plt.subplots(figsize=(1.5, 1.5))
    # pie_colours = ["w", "thistle"]
    # # ax1.pie(sizes, startangle=90, colors=pie_colours)
    # # ax1.set_title(month_name, fontsize=20)
    # ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    # # circle_fig = "/tmp/" + yearx + month + day + "_circle.png"
    # # plt.savefig(circle_fig, bbox_inches="tight", type="png", dpi=100, transparent=True)
    # # os.system('open '+circle_fig)
    # plt.close()
    
    # my_cmap = plt.cm.get_cmap('bwr_r')
    my_cmap.set_under("#AA7748")  #  brown, land
    fig, ax = plt.subplots(figsize=(12,16))
    plt.clf()
    # plt.figure()
    # BBAc_anomaly[land] = -1
    if varchoice=='anom':
        plotvar[((plotvar < lo) & (plotvar > -2) & (msk > 1))] = lo
    # BBAc_anomaly[((BBAc_anomaly > hi) & (msk > 1))] = hi
    
    im=plt.imshow(plotvar, vmin=lo,vmax=hi,cmap=my_cmap)
    # plt.title(date, fontsize=20)
    
    plt.axis("off")
    
    do_annotate=0
    
    if do_annotate:
        # -------------------------------------------------- upper left
        # xx0 = 0.44
        # yy0 = 0.99
        # dy = -0.04
        # cc = 0
        xx0 = 0.26
        yy0 = 0.995
        dy = -0.04
        cc = 0
        mult = 1.1  # JB shell
        
        # txt = "2022," + " " + calendar.month_name[int(month)] + " " + day
        
        
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
        xx0 = 0.82
        dy = -0.04
        cc = 0
        mult = 0.8
        
        # txt = "albedo\nanomaly:"
        # plt.text(
        #     xx0,
        #     yy0 + cc * dy,
        #     txt,
        #     fontsize=font_size * mult,
        #     color="k",
        #     transform=ax.transAxes,
        #     va="top",
        # )
        cc += 2.0
        
        if varchoice=='anom':
            txt = "2023 minus the\n2017-2022 average"
        
            co=0.5
            
            plt.text(
                xx0,
                yy0 + cc * dy,
                txt,
                fontsize=font_size*mult,
                color=[co,co,co],
                transform=ax.transAxes,
                va="top",
            )
            cc += 2.0
        
        # -------------------------------------------------- sat info
        xx0 = 0.77
        yy0 = 0.2
        dy = -0.03
        cc = 0
        mult = 0.7
        
        xx0 = 0.69
        yy0 = 0.23
        dy = -0.03
        cc = 0
        mult = 0.8
        box_dy = 0.05
        color_code = "#6CE577"
        color_code = "#6AD8EA"
        color_code = "grey"
        
        # plt.text(
        #     xx0,
        #     yy0 + cc * dy,
        #     # 'via Kokhanovsky et al 2020', fontsize=font_size*mult,
        #     "polarportal.dk",
        #     fontsize=font_size * mult,
        #     transform=ax.transAxes,
        #     color=color_code,
        # )
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
       
    # cax = fig.add_axes([0.68, 0.135, 0.03, 0.2]) # tucked in lower right
    # cb=fig.colorbar(im, orientation='vertical', cax=cax)

    # for t in cb.ax.get_yticklabels():
    #     t.set_horizontalalignment('left')   
    #     t.set_x(1.5)
    # cbax = ax.inset_axes([1, 0.2, 0.7, 0.05], transform=ax.transAxes)
    # fig.colorbar(im, ax=ax, cax=cbax, shrink=0.7, orientation='vertical')
    # cbar.ax.get_yaxis().set_ticks([])
    # for j, lab in enumerate(['$0$','$1$','$2$','$>3$']):
    #     cbar.ax.text(.5, (2 * j + 1) / 8.0, lab, ha='center', va='center')
    # cbar.ax.get_yaxis().labelpad = 25
    # cbar.ax.set_ylabel('# of contacts', rotation=270)
    
    # plt.clim(lo, hi)
    
    # https://stackoverflow.com/questions/13714454/specifying-and-saving-a-figure-with-exact-size-in-pixels
    
    os.system("mkdir -p " + figpath)
    
    figx, figy = 16, 12
    
    ly='p'
    
    if ly=='x':
        plt.show()
    else:
        DPI=300
        plt.savefig(
            "/tmp/tmp.png",
            bbox_inches="tight",
            # figsize=(figx, figy),
            # type="png",
            dpi=DPI,
            facecolor="w",
        )
        
        plt.savefig(
            f"/Users/jason/0_dat/S3/Figs/SICE_{season}_"+period+"_"+str(lo)+"-"+str(hi)+band+f"_{DPI}_DPI.png",
            bbox_inches="tight",
            # figsize=(figx, figy),
            # type="png",
            dpi=DPI,
            facecolor="w",
        )
        #%%
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
        
        yy0 = 3100
        xos = 1200
        fn = "/Users/jason/Dropbox/S3/SICE_anomaly_figs/ancil/SICE_logo.png"
        SICE_logo = Image.open(fn, "r")
        pixelsx = 300
        size = pixelsx, pixelsx
        SICE_logo.thumbnail(size, Image.ANTIALIAS)
        back_im.paste(SICE_logo, (xos, yy0))  # ), mask=SICE_logo)
        
        # yy0=1000 ; xos=350
        fn = "/Users/jason/Dropbox/S3/SICE_anomaly_figs/ancil/PTEP_logo.png"
        pixelsx = 350
        size = pixelsx, pixelsx
        PTEP_logo = Image.open(fn, "r")
        PTEP_logo.thumbnail(size, Image.ANTIALIAS)
        back_im.paste(PTEP_logo, (xos + 570, yy0 + 150), mask=PTEP_logo)
        
        # ---------------------------- progress pie
        # im_pie = Image.open(circle_fig)
        # back_im.paste(im_pie, (485, 700), mask=im_pie)
            
        ofile = figpath + fignam + ".png"
        back_im.save(ofile, optimize=True, quality=95)
        print(ofile)
        ofile = figpath + "sm_" + fignam + ".png"
        size = 1080, 1080
        back_im.thumbnail(size, Image.ANTIALIAS)
        back_im.save(ofile, optimize=True, quality=95)
        
        os.system('open '+ofile)
        
    
