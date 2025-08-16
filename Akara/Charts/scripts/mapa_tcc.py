import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import cartopy.io.shapereader as shpreader
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

# Diretórios de dados e figuras
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRCSV2 = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'

ds_akara_slevel = xr.open_dataset(DIRDADO + 'akara_maps.nc')
df2 = pd.read_csv(DIRCSV2 + 'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

# Definir dicionários para símbolos e cores
symbols = {'Incipient': 'x', 'Intensification': 'o', 'Mature': '^', 'Decay': 'd'}
colors = {'Incipient': '#65a1e6', 'Intensification': '#f7b538',
          'Mature': '#d62828', 'Decay': '#9aa981'}

# Definir fase, símbolo e cor para cada índice
df2['phase'] = ''
df2.loc[0:11, 'phase'] = 'Incipient'
df2.loc[12:37, 'phase'] = 'Intensification'
df2.loc[38:42, 'phase'] = 'Mature'
df2.loc[43:, 'phase'] = 'Decay'

# Adicionar colunas de símbolos e cores correspondentes às fases
df2['symbol'] = df2['phase'].map(symbols)
df2['color'] = df2['phase'].map(colors)

df2.to_csv(DIRCSV2 + 'track_csv_formatado.csv', index=False)

fig = plt.figure(figsize=(16, 12))  # Layout geral

# --------- MAPA 1 (GLOBAL) ---------
ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2, projection=ccrs.PlateCarree())
ax1.set_global()
ax1.add_feature(cfeature.LAND, facecolor='lightgrey')
ax1.add_feature(cfeature.OCEAN, facecolor='white')
ax1.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax1.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)

shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
ax1.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)

# Caixa do domínio do Mapa 2
lon_min2, lon_max2 = -90, -25
lat_min2, lat_max2 = -60, 15
width2 = lon_max2 - lon_min2
height2 = lat_max2 - lat_min2

rect2 = mpatches.Rectangle((lon_min2, lat_min2), width2, height2,
                            linewidth=2, edgecolor='red', facecolor='none',
                            transform=ccrs.PlateCarree(), zorder=5)
ax1.add_patch(rect2)

# Gridlines
gl = ax1.gridlines(crs=ccrs.PlateCarree(), color='black', alpha=1.0, linestyle='--', linewidth=0.25)

# Definir ticks manualmente
ax1.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
ax1.set_yticks(np.arange(-90, 91, 30), crs=ccrs.PlateCarree())

# Definir labels
lon_formatter = ccrs.cartopy.mpl.ticker.LongitudeFormatter()
lat_formatter = ccrs.cartopy.mpl.ticker.LatitudeFormatter()

ax1.xaxis.set_major_formatter(lon_formatter)
ax1.yaxis.set_major_formatter(lat_formatter)

# Controlar o tamanho da fonte dos labels
ax1.tick_params(labelsize=14)

# Plot trackfile no mapa global
ax1.plot(df2['Lon'], df2['Lat'], transform=ccrs.PlateCarree(),
         color='black', linewidth=1, linestyle='-')
for phase in df2['phase'].unique():
    phase_data = df2[df2['phase'] == phase]
    ax1.scatter(phase_data['Lon'], phase_data['Lat'], transform=ccrs.PlateCarree(),
                color=colors[phase], marker=symbols[phase], s=40, label=phase)
ax1.legend(loc='lower right', fontsize=16)
ax1.set_title('(a) MONAN - Global Domain', loc='left')

# --------- MAPA 2 (REGIONAL) ---------
ax2 = plt.subplot2grid((2, 2), (1, 0), projection=ccrs.PlateCarree())
ax2.set_extent([-90, -25, -60, 15], crs=ccrs.PlateCarree())  # América do Sul ou o domínio que quiser
ax2.add_feature(cfeature.LAND, facecolor='lightgrey')
ax2.add_feature(cfeature.OCEAN, facecolor='white')
ax2.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax2.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)

shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
ax2.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)

# Caixa do domínio do Mapa 3
lon_min3, lon_max3 = -60, -33
lat_min3, lat_max3 = -45, -15
width3 = lon_max3 - lon_min3
height3 = lat_max3 - lat_min3

rect3 = mpatches.Rectangle((lon_min3, lat_min3), width3, height3,
                            linewidth=2, edgecolor='blue', facecolor='none',
                            transform=ccrs.PlateCarree(), zorder=5)
ax2.add_patch(rect3)

# Gridlines
gl = ax2.gridlines(crs=ccrs.PlateCarree(), color='black', alpha=1.0, linestyle='--', linewidth=0.25,
                  xlocs=np.arange(-180, 180, 10), ylocs=np.arange(-90, 90, 10), draw_labels=True)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'fontsize': 16}  # Ajuste o tamanho da fonte no eixo X (longitude)
gl.ylabel_style = {'fontsize': 16}

# Plot trackfile no mapa regional 1
ax2.plot(df2['Lon'], df2['Lat'], transform=ccrs.PlateCarree(),
         color='black', linewidth=1, linestyle='-')
for phase in df2['phase'].unique():
    phase_data = df2[df2['phase'] == phase]
    ax2.scatter(phase_data['Lon'], phase_data['Lat'], transform=ccrs.PlateCarree(),
                color=colors[phase], marker=symbols[phase], s=40, label=phase)
ax2.set_title('(b) MONAN – Zoom over South America', loc='left')

# --------- MAPA 3 (REGIONAL) ---------
ax3 = plt.subplot2grid((2, 2), (1, 1), projection=ccrs.PlateCarree())
ax3.set_extent([-60, -33, -45, -15], crs=ccrs.PlateCarree())  # Domínio específico, exemplo Brasil Sul
ax3.add_feature(cfeature.LAND, facecolor='lightgrey')
ax3.add_feature(cfeature.OCEAN, facecolor='white')
ax3.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax3.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)

shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
ax3.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)


# Gridlines
gl = ax3.gridlines(crs=ccrs.PlateCarree(), color='black', alpha=1.0, linestyle='--', linewidth=0.25,
                  xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'fontsize': 16}  # Ajuste o tamanho da fonte no eixo X (longitude)
gl.ylabel_style = {'fontsize': 16}

# Plot trackfile no mapa regional 2
ax3.plot(df2['Lon'], df2['Lat'], transform=ccrs.PlateCarree(),
         color='black', linewidth=1, linestyle='-')
for phase in df2['phase'].unique():
    phase_data = df2[df2['phase'] == phase]
    ax3.scatter(phase_data['Lon'], phase_data['Lat'], transform=ccrs.PlateCarree(),
                color=colors[phase], marker=symbols[phase], s=40, label=phase)
ax3.set_title('(c) Object-based Verification Domain', loc='left')

# Salvar a figura completa
plt.tight_layout()
plt.subplots_adjust(wspace=-0.4)
plt.savefig(f'{DIRFIG}Akara_trackfile_multimaps.png', dpi=300, bbox_inches='tight')

