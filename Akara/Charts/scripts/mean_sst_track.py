import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import cartopy.io.shapereader as shpreader
import pandas as pd

# Diretórios de dados e figuras
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/mean_sst/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRCSV2 = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'

# Abrir o dataset de Akara e o arquivo CSV
ds_akara_slevel = xr.open_dataset(DIRDADO + 'akara_maps.nc')
df2 = pd.read_csv(DIRCSV2 + 'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

# Definir dicionários para símbolos e cores
symbols = {'Incipient': 'x', 'Intensification': 'o', 'Mature': '^', 'Decay': 'd'}

colors= {'Incipient': '#65a1e6', 'Intensification': '#f7b538',
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

# Extração e cálculos de dados do NetCDF
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]
sst = ds_akara_slevel['sst'][:] - 273.15  # SST em Celsius
t2m = ds_akara_slevel['t2m'][:] - 273.15  # T2M em Celsius

# Cálculo da média temporal
media_sst = sst.mean(dim='valid_time')
media_t2m = t2m.mean(dim='valid_time')
dif_temperatura = media_sst - media_t2m  # Diferença entre SST e T2M

# Plotando o mapa
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
extent = [-47.5, -35, -35, -17.5]
ax.set_extent(extent, crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor='lightgrey')
ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)

# Adicionar shapefile
shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)

# Gridlines
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='black', alpha=1.0, linestyle='--', linewidth=0.25,
                  xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
gl.top_labels = False
gl.right_labels = False

# Contorno da diferença de temperatura (SST - T2M)
levels = np.arange(-1, 3, 0.25)
img = ax.contourf(lon, lat, dif_temperatura, levels=levels, transform=ccrs.PlateCarree(), cmap='RdBu_r', extend='both')

# Adicionar barra de cores
cb = plt.colorbar(img, ax=ax, orientation='vertical', pad=0.05, shrink=0.8, label="SST - T2M (°C)")

# Plotar cada fase com linhas conectando os pontos e marcadores

ax.plot(df2['Lon'], df2['Lat'], transform=ccrs.PlateCarree(),
        color='black', linewidth=1, linestyle='-')

for phase in df2['phase'].unique():
    phase_data = df2[df2['phase'] == phase]
    ax.scatter(phase_data['Lon'], phase_data['Lat'], transform=ccrs.PlateCarree(),
               color=colors[phase], marker=symbols[phase], s=40, label=f'{phase}', linestyle='-')

# Adicionar legenda
ax.legend(loc='lower right', fontsize=8)

# Título do gráfico
plt.title('AKARÁ reanalysis (ERA5) Mean SST - Mean T2M', loc='left')

# Salvar e exibir o gráfico
plt.savefig(f'{DIRFIG}Akara_mean_sst_t2m_track.png', dpi=300)

