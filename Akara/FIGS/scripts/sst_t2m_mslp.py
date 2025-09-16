import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import cartopy, cartopy.crs as ccrs
import matplotlib.colors as mcolors
import matplotlib.colors
import metpy.calc as mpcalc
from metpy.calc import equivalent_potential_temperature
from metpy.units import units
from metpy.calc import dewpoint_from_relative_humidity
from metpy.interpolate import cross_section
import cartopy.io.shapereader as shpreader
import pandas as pd


DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Specific_Figures/sst_t2m/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRCSV2 = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'



df2 = pd.read_csv(DIRCSV2+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])


colors = ["#2d001c", "#5b0351", "#780777", "#480a5e", "#1e1552", "#1f337d", "#214c9f", "#2776c6", "#2fa5f1", "#1bad1d", "#8ad900", "#ffec00", "#ffab00", "#f46300", "#de3b00", "#ab1900", "#6b0200"]
dif_sstt2m = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
dif_sstt2m.set_over('#3c0000')
dif_sstt2m.set_under('#28000a')


ds_akara_slevel = xr.open_dataset(DIRDADO+'akara_maps.nc')
## extraindo lat, lon
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]
sst = ds_akara_slevel['sst'][:]
sst = sst - 273
media_sst = sst.mean().values

## extraindo tempo
times = ds_akara_slevel['valid_time'].values
n_final = len(ds_akara_slevel['valid_time'])

for i in range(0, n_final):
    ## definindo string de data
    time = str(times[i])[:13]
    print(time)
    ## extraindo msl
    msl = ds_akara_slevel['msl'][:].isel(valid_time=i)
    msl = msl / 100
    ## sst e t2m
    sst = ds_akara_slevel['sst'][:].isel(valid_time=i)
    sst = sst - 273
    t2m = ds_akara_slevel['t2m'][:].isel(valid_time=i)
    t2m = t2m - 273
    dif_temp = sst - t2m
    extent = [-47.5, -35, -35, -17.5]
    

    lat_point = df2.loc[i, 'Lat']
    lon_point = df2.loc[i, 'Lon']

    

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    #ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)
    interval=0.5
    ## plot dfi_temp
    img1 = ax.contourf(lon, lat, dif_temp,np.arange(-3, 3, interval), cmap='turbo', extend='both')
    cbar = plt.colorbar(img1, ax=ax, aspect=15, extend='both')
    cbar.set_label('SST - T2M (°C)', rotation=270, labelpad=20, fontsize=18)
    ticks = np.arange(-4, 4, interval)
    cbar.set_ticks(ticks)
    cbar.ax.tick_params(labelsize=18)
  
    ticks = np.arange(-3, 3, 1)
    cbar.set_ticks(ticks)
    ### plot mslp
    data_min_mslp = 980
    data_max_mslp = 1030
    interval_mslp = 2
    levels_mslp = np.arange(data_min_mslp, data_max_mslp, interval_mslp)
    levels2_mslp = np.arange(data_min_mslp ,data_max_mslp, 3)

    ct1 = ax.contour(lon, lat, msl, linewidths=2.5, levels=levels_mslp, colors='grey')
    ct2 = ax.contour(lon, lat, msl, linewidths=2.5, levels=levels2_mslp, colors='grey')
    ax.clabel(ct2, inline=1, inline_spacing=0, fontsize='12',fmt = '%1.0f', colors= 'grey')
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='black',
                 alpha=1.0, linestyle='--', linewidth=0.25,
                xlocs=np.arange(-180, 180, 5),
                  ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 18}  # Aumenta o tamanho da fonte dos rótulos do eixo X
    gl.ylabel_style = {'size': 18}
    plt.title(f'AKARÁ reanalysis (ERA5)\nSST - T2M (°C), MSLP (hPa) \n{time}', loc='left', fontsize=18)
    ax.coastlines()


    ax.scatter(lon_point, lat_point, color='black', marker='X', s=100, label="Center")
    lat_min = lat_point - 2.5
    lat_max = lat_point + 2.5
    lon_min = lon_point - 2.5
    lon_max = lon_point + 2.5

    # Criando um retângulo para a caixa
    ax.plot([lon_min, lon_max], [lat_min, lat_min], color='black', linewidth=2)  # Linha inferior
    ax.plot([lon_min, lon_max], [lat_max, lat_max], color='black', linewidth=2)  # Linha superior
    ax.plot([lon_min, lon_min], [lat_min, lat_max], color='black', linewidth=2)  # Linha esquerda
    ax.plot([lon_max, lon_max], [lat_min, lat_max], color='black', linewidth=2)  # Linha direita

    plt.savefig(f'{DIRFIG}Akara_mslp_sst_t2m{time}.png', bbox_inches='tight', dpi=300)

    plt.tight_layout()
    plt.close()