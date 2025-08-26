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
from metpy.calc import potential_vorticity_baroclinic
from metpy.calc import potential_temperature
import metpy.calc as mpcalc
from metpy.units import units

DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Automated_Figures/pv_corte/'



df = pd.read_csv(DIRCSV+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

ds_akara = xr.open_dataset(DIRDADO+'akara_maps.nc')

ds_akara = ds_akara.metpy.parse_cf()

theta = mpcalc.potential_temperature(
    ds_akara['pressure_level'] * units.hPa,
    ds_akara['t']
)


ds_akara['theta'] = xr.DataArray(
    theta.data,
    coords=theta.coords,
    dims=theta.dims,
    attrs={
        'long_name': 'Potential Temperature',
        'units': 'K',
        'standard_name': 'air_potential_temperature'
    }
)
print(ds_akara['theta']) # criou tudo certo, mesma dismensao para tudo

pv = mpcalc.potential_vorticity_baroclinic(ds_akara['theta'], ds_akara['pressure_level'] * units.hPa,
                                           ds_akara['u'], ds_akara['v'])

ds_akara['pv'] = xr.DataArray(
    pv.data,
    coords=theta.coords,   # herda coords do theta (que já bate com t, u, v)
    dims=theta.dims,
    attrs={
        'long_name': 'Baroclinic Potential Vorticity',
        'units': 'K m^2 kg^-1 s^-1',
        'standard_name': 'atmosphere_potential_vorticity'
    }
)

print(ds_akara['pv'])


lat_ = ds_akara['latitude'][:]
lon_ = ds_akara['longitude'][:]


#print(pot_vort)
times = ds_akara['valid_time'].values
for i in range(len(df)):
    time = str(times[i])[:13]
    tempo = df.loc[i, 'time']
    lat = df.loc[i, 'Lat']
    lon = df.loc[i, 'Lon']


    print(f'Processando o tempo: {time}')
    mslp = ds_akara['msl'].isel(valid_time=i) / 100  # Converte para hPa

    # Cross-section
    ds_akara_tempo = ds_akara.isel(valid_time=i)

    





    # Também prepara o dataset completo para outras variáveis
    data = ds_akara_tempo.metpy.parse_cf().squeeze()
    #print(data)

   
    # Define linha do corte
    start = (lat, lon - 4.5)
    end   = (lat, lon + 4.5)

    # Cross-section das variáveis originais
    cross = cross_section(data, start, end).set_coords(('latitude', 'longitude'))



   
    print('###########################')
    #rint(cross['pv'])
    print('#############')
    #print(cross['pv'].shape)
    




   













    # Criação da figura
    fig, ax = plt.subplots(figsize=(16, 9))
    extent = [-47.5, -35, -35, -17.5]

    # Minimap
    minimapa = fig.add_axes([0.037, 0.58, 0.3, 0.3], projection=ccrs.PlateCarree())
    minimapa.set_extent(extent, crs=ccrs.PlateCarree())
    minimapa.set_xticks([])
    minimapa.set_yticks([])
    minimapa.add_feature(cfeature.COASTLINE)
    minimapa.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
    minimapa.add_feature(cfeature.LAND, facecolor="lightgrey", zorder=2)
    shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
    minimapa.add_geometries(
        shapefile, ccrs.PlateCarree(), edgecolor="black", facecolor="none", linewidth=0.3, zorder=3
    )

    # Contorno no minimapa
    contour = minimapa.contour(
        lon_, lat_, mslp, levels=np.arange(980, 1020, 2), colors="black", linewidths=2, zorder=1
    )
    ax.clabel(contour, inline=1, inline_spacing=0, fontsize="10", fmt="%1.0f", colors="black", zorder=1)

    # Pontos do cross-section
    transform = ccrs.Geodetic()._as_mpl_transform(minimapa)
    endpoints = transform.transform(np.vstack([start, end]))
    minimapa.scatter(endpoints[:, 0], endpoints[:, 1], c="black", zorder=2)
    minimapa.plot([start[1], end[1]], [start[0], end[0]], c="black", zorder=2)


    levels = np.arange(-1, 1.1, 0.2)

    norm = mcolors.TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    w_contourf = ax.contourf(
        cross["longitude"], cross["pressure_level"], cross["w"], cmap='coolwarm',
          levels=levels, norm=norm, extend='both')
    cbar = plt.colorbar(w_contourf, ax=ax, orientation='vertical', pad=0.05)
    cbar.set_label('Vertical Velocity (Pa/s)', fontsize=12)
    cbar.ax.tick_params(labelsize=14)

    pot_contour = ax.contour(
    cross["longitude"], 
    cross["pressure_level"], 
    cross["pv"] * 1e6,
    colors='black', levels=np.arange(-4, 0, 1), linewidths=2.0
)
    ax.clabel(pot_contour, inline=1, inline_spacing=0, fontsize=10, fmt="%1.0f")

    
    
    # Configuração dos eixos
    ax.set_title(
    f"Akara Cross Section {time}\nPotential Vorticity (PV) and Vertical Velocity (ω) Lat: {lat:.2f} | Central Lon: {lon:.2f}",
    loc="left", fontsize=16
)
    ax.set_ylabel("Pressure (hPa)", fontsize=16)
    ax.set_xlabel("Longitude (degrees east)", fontsize=14)
    
    ax.tick_params(axis='x', labelsize=16)
    ax.set_yscale("symlog")
    ax.set_ylim(1000, 100)
    yticks = np.arange(1000, 0, -100)  # 1000, 900, ..., 100
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks, fontsize=14)
    


    # Salva e fecha a figura
    plt.savefig(f"{DIRFIG}Akara_cross_{time}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)  # Fecha a figura no final de cada iteração
