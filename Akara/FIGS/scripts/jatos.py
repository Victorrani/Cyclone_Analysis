# -*- coding: utf-8 -*-
"""
AKARÁ | Viento 250 hPa + Z500 (contornos)
Genera una figura por tiempo con:
 - Intensidad del viento (m/s) a 250 hPa (contourf)
 - Altura geopotencial Z a 500 hPa (contornos)
 - Marca y caja de 5°x5° alrededor del centro (track)
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

from metpy.calc import potential_vorticity_baroclinic
from metpy.calc import potential_temperature
import metpy.calc as mpcalc
from metpy.units import units


# =========================
# RUTAS / CONSTANTES
# =========================
DIRDADO  = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG   = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Automated_Figures/geo500_jatos/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRCSV2  = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'

# Dominio del mapa (lon_min, lon_max, lat_min, lat_max)
EXTENT = (-60, -30, -40, -15)

# Niveles y estilos
LEVELS_WIND = np.arange(30, 95, 5)      # m/s, 30..90
CMAP_WIND   = 'twilight'
LEVELS_Z500 = np.arange(540, 595, 3)    # 540..592 (unid. según dataset)
Z_CONTOUR_COLOR = 'red'
Z_CONTOUR_LW    = 2.0
CLABEL_KW = dict(fmt='%d', fontsize=15, colors='black')

# Gridlines
GRID_XLOCS = np.arange(-180, 181, 5)
GRID_YLOCS = np.arange(-90,  91, 5)
GRID_STYLE = dict(color='black', alpha=1.0, linestyle='--', linewidth=0.25)

# Caja alrededor del centro (±2.5°)
BOX_DELTA = 2.5

# Salida
DPI = 300


# =========================
# CARGA DE DATOS
# =========================
ds = xr.open_dataset(os.path.join(DIRDADO, 'akara_reboita1.nc'))

df_track = pd.read_csv(
    os.path.join(DIRCSV2, 'trackfile.v3.txt'),
    sep=r'\s+', header=None,
    names=["time", "Lat", "Lon", "mslp", "vort850"]
)

lat = ds['latitude'][:]
lon = ds['longitude'][:]
times = ds['valid_time'].values
n_final = len(times)

# Mallas para barbelas/contourf
LON2D, LAT2D = np.meshgrid(lon, lat)

os.makedirs(DIRFIG, exist_ok=True)


# =========================
# LOOP PRINCIPAL
# =========================
for i in range(n_final):
    # Timestamp para título/archivo
    time_str = str(times[i])[:13]                # 'YYYY-MM-DDTHH'
    print(f'Processando: {time_str}')

    # Centro (track)
    lat_c = float(df_track.loc[i, 'Lat'])
    lon_c = float(df_track.loc[i, 'Lon'])

    # Campos en 250 y 500 hPa
    u250 = ds['u'].isel(valid_time=i).sel(pressure_level=250)   # m/s
    v250 = ds['v'].isel(valid_time=i).sel(pressure_level=250)   # m/s
    z500 = ds['z'].isel(valid_time=i).sel(pressure_level=500)   # unidad según dataset
    z500 = z500 / 100.0  # mantiene tu conversión original (p.ej., a "dam" si z estaba en gpm*10)
    wind_speed = mpcalc.wind_speed(u250, v250) 

    u = ds['u'].sel(pressure_level=[300, 250, 200]) * units('m/s')
    v = ds['v'].sel(pressure_level=[300, 250, 200]) * units('m/s')
    t = ds['t'].sel(pressure_level=[300, 250, 200]) * units('kelvin')

    u = u.isel(valid_time=i)
    v = v.isel(valid_time=i)
    t = t.isel(valid_time=i)

    pressure_levels = [300, 250,  200] * units.hPa

    theta = mpcalc.potential_temperature(t.pressure_level, t)
    
    pot_vort = potential_vorticity_baroclinic(theta, theta.pressure_level, u, v)


    pot_vort = pot_vort.sel(pressure_level=250)  # Selecciona el nivel de 250 hPa

    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent(EXTENT, crs=ccrs.PlateCarree())

    # Features y shapefile
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)
    ax.coastlines()

    shapes = list(shpreader.Reader(DIRSHAPE).geometries())
    ax.add_geometries(shapes, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)

    # Grid con etiquetas
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, xlocs=GRID_XLOCS, ylocs=GRID_YLOCS, **GRID_STYLE)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'fontsize': 18}
    gl.ylabel_style = {'fontsize': 18}

    # Relleno: velocidad del viento a 250 hPa
    #cf = ax.contourf(lon, lat, wind_speed, levels=LEVELS_WIND, cmap=CMAP_WIND, extend='max')

    cpv = ax.contourf(
    lon, lat,
    pot_vort * 1e6,   
    cmap='turbo',    # cor preta
    alpha=0.5
)
    cbar = fig.colorbar(cpv, ax=ax, orientation='vertical', pad=0.05, shrink=0.7)
    pv = ax.contour(lon, lat, pot_vort * 1e6, levels=[-2], colors='black', linewidths=1.0)
    #ax.clabel(cpv, inline=True, fontsize=10, fmt='%1.1f', colors='black')

    # Contornos: z500
    #cz = ax.contour(lon, lat, z500, levels=LEVELS_Z500, colors=Z_CONTOUR_COLOR, linewidths=Z_CONTOUR_LW)
    #ax.clabel(cz, **CLABEL_KW)

    # Colorbar
    #cbar = fig.colorbar(cf, ax=ax, orientation='vertical', pad=0.05, shrink=0.7)
    #cbar.set_label('Wind Speed (m/s)', fontsize=18)
    #cbar.ax.tick_params(labelsize=18)

    # Marca del centro y caja 5x5°
    ax.scatter(lon_c, lat_c, color='black', marker='X', s=100, label='Center')

    lat_min, lat_max = lat_c - BOX_DELTA, lat_c + BOX_DELTA
    lon_min, lon_max = lon_c - BOX_DELTA, lon_c + BOX_DELTA
    ax.plot([lon_min, lon_max], [lat_min, lat_min], color='black', linewidth=2)
    ax.plot([lon_min, lon_max], [lat_max, lat_max], color='black', linewidth=2)
    ax.plot([lon_min, lon_min], [lat_min, lat_max], color='black', linewidth=2)
    ax.plot([lon_max, lon_max], [lat_min, lat_max], color='black', linewidth=2)

    # Título
    ax.set_title(f'AKARÁ reanalysis (ERA5)\n{time_str}', loc='left', fontsize=18)

    # Guardado
    out_name = f'Akara_wind_speed_z500_{time_str}.png'
    plt.savefig(os.path.join(DIRFIG, out_name), dpi=DPI, bbox_inches='tight')
    plt.close(fig)

# Cierre del dataset
ds.close()
