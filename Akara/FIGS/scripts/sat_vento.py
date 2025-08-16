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
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap
from metpy.calc import equivalent_potential_temperature
from metpy.units import units
from metpy.calc import dewpoint_from_relative_humidity
from metpy.interpolate import cross_section
import cartopy.io.shapereader as shpreader
import matplotlib.colors as cm
from datetime import datetime
import pandas as pd


DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Automated_Figures/sat_vento/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRSAT = '/home/victor/USP/sat_goes/fig_dados/20240214_22/ch13/'
DIRCSV2 = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'

# Paleta sem tons de cinza, ajustando as cores para temperaturas
tb_cmap_noaa = LinearSegmentedColormap.from_list('my_gradient', (
    (0.000, (0.961, 0.961, 0.961)),
    (0.068, (0.961, 0.961, 0.961)),
    (0.070, (0.541, 0.043, 0.522)),
    (0.110, (0.820, 0.820, 0.820)),
    (0.150, (0.012, 0.012, 0.012)),
    (0.190, (0.957, 0.024, 0.000)),
    (0.220, (0.937, 1.000, 0.000)),
    (0.280, (0.016, 0.957, 0.000)),
    (0.300, (0.000, 0.341, 0.298)),
    (0.300, (0.000, 0.161, 0.380)),
    (0.399, (0.200, 1.000, 1.000)),
    (0.400, (1.000, 1.000, 1.000)),
    (1.000, (0.000, 0.000, 0.000))
))


ds_akara_slevel = xr.open_dataset(DIRDADO+'akara_reboita1.nc')

df2 = pd.read_csv(DIRCSV2+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

## extraindo lat, lon
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]

times = ds_akara_slevel['valid_time'].values
n_final = len(ds_akara_slevel['valid_time'])
X, Y = np.meshgrid(lon, lat)

pressure_levels = ds_akara_slevel['pressure_level'].values


arquivos_netCDF = sorted([f for f in os.listdir(DIRSAT) if f.endswith('.nc')])
for i in range(0, n_final):
    ## definindo string de data
    time_ds = str(times[i])[:13]
    
    print('Data do ds: '+time_ds)
    data_hora = datetime.strptime(time_ds, "%Y-%m-%dT%H")

    data_hora_formatada = str(data_hora.strftime("%Y%m%d%H"))

    lat_point = df2.loc[i, 'Lat']
    lon_point = df2.loc[i, 'Lon']
    data_point = df2.loc[i, 'time']

    print('Data formatada do ds: '+data_hora_formatada)
    for arquivo in arquivos_netCDF:
        data_arquivo = str(arquivo[10:20])
        if data_arquivo == data_hora_formatada:
            print(f'arquivo {data_arquivo} encontrad: {arquivo}')

            arq_entrada = xr.open_dataset(DIRSAT+arquivo, engine='netcdf4')
            
            print(f'Criando a imagem da data {data_arquivo}')

            print(f'data_point: {data_point}')

            ch13 = arq_entrada.Band1
            ch13.data = ch13.data / 100 - 273.15  # Convertendo de Kelvin para Celsius

            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
            
            ax.add_feature(cfeature.LAND, edgecolor='black')
            ax.add_feature(cfeature.COASTLINE, linewidth=2.0)  # Aumenta a grossura da linha de costa
            ax.add_feature(cfeature.BORDERS, linestyle=':')

            # Adicionando o shapefile dos estados
            shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
            ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)

            # Plotando os dados do canal 13
            img = ch13.plot(
    ax=ax, cmap=tb_cmap_noaa, transform=ccrs.PlateCarree(), vmin=-100, vmax=100,
    cbar_kwargs={
        "label": "Brightness Temperature (°C)", 
        "orientation": "vertical",  # Barra de cores vertical
        "pad": 0.05,                # Distância da barra para o gráfico
        "aspect": 20,               # Aumenta a espessura da barra de cores
        "shrink": 0.8,              # Aumenta a altura total da barra de cores
        "ticks": np.arange(-100, 100, 10),  # Personalizar os ticks
        "extend": 'neither'             # Aumenta o tamanho da fonte dos ticks
    }
)
            cbar = img.colorbar
            cbar.set_label("Brightness Temperature (°C)", fontsize=16)  # Aumenta o tamanho do rótulo principal
            cbar.ax.tick_params(labelsize=13)
            
            u_1000 = ds_akara_slevel['u'].isel(valid_time=i, pressure_level=0)
            v_1000 = ds_akara_slevel['v'].isel(valid_time=i, pressure_level=0)

            sep = 5

# Plotar o campo de vento com barbelas
            ax.barbs(X[::sep,::sep], Y[::sep,::sep], u_1000[::sep,::sep], v_1000[::sep,::sep], 
            transform=ccrs.PlateCarree(), 
            barbcolor='black', flagcolor='black', flip_barb=True, length=4) 

            ax.scatter(lon_point, lat_point, color='#50C878', marker='X', s=100, label="Center")

            # Ajustando os limites do gráfico para o intervalo desejado
            ax.set_extent([-60, -30, -40, -15], crs=ccrs.PlateCarree())
    
            # Linhas de grade
            gl = ax.gridlines()
            gl.bottom_labels = True
            gl.left_labels = True
            gl.xlabel_style = {'fontsize': 18}  # Ajuste o tamanho da fonte no eixo X (longitude)
            gl.ylabel_style = {'fontsize': 18}

            

            # Título
            plt.title(
    f"Akará GOES16 CH13\nWind 1000 hPa - {data_arquivo}Z", 
    loc='left', 
    fontsize=18  # Altere para o tamanho desejado
) 
            file_name = f"ch13_AKARA_vento{data_arquivo}.png"
            plt.savefig(os.path.join(DIRFIG, file_name), dpi=300, bbox_inches='tight')
            plt.close(fig)

            break

        else:
            print('')