import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import pandas as pd
import scipy.ndimage
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import geopandas as gpd
from shapely.geometry import box
from rasterio.features import geometry_mask



DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRCSV2 =  '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/CSV_FILES/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Specific_Figures/serie/'

df = pd.read_csv(DIRCSV+'akara1_track_track.csv', sep=';')
df2 = pd.read_csv(DIRCSV2+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

df_plot = df[['time', 'min_max_zeta_850', 'min_hgt_850']]

df_plot['time'] = pd.to_datetime(df_plot['time'])
df2['time'] = pd.to_datetime(df2['time'])


# Plotar os dados com eixos duplos
fig, (ax1,ax3) = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), constrained_layout=True)

# Plotar no primeiro eixo y
ax1.plot(df_plot['time'], df2['mslp'], label='MSLP', marker='o', color='black')
#ax1.set_xlabel('Data')
ax1.tick_params(axis='y', labelcolor='black', labelsize=18)  # Aumenta o tamanho da fonte
ax1.set_ylabel('MSLP (hPa)', fontsize=18)


# Criar um segundo eixo y (eixo secundário) com escala diferente
ax2 = ax1.twinx()
ax2.plot(df_plot['time'], df_plot['min_max_zeta_850'], label=r'$\zeta_{850}$', marker='o', color='blue')  # Usando LaTeX para zeta com subscrito
ax2.tick_params(axis='y', labelcolor='blue', labelsize=18)
ax2.set_ylabel('$\zeta_{850}$ (1/s²)', fontsize=18, color='blue')  # Aumenta o tamanho da fonte


patches = [
    mpatches.Patch(color='black', label='MSLP'),
    mpatches.Patch(color='blue', label=r'$\zeta_{850}$')
]



time0 = pd.to_datetime('2024-02-14T21')
time1 = pd.to_datetime('2024-02-16T09')
time2 = pd.to_datetime('2024-02-19T15')
time3 = pd.to_datetime('2024-02-20T09')
time4 = pd.to_datetime('2024-02-22T21')
time5 = pd.to_datetime('2024-02-17T12')
time6 = pd.to_datetime('2024-02-21T09')

ax1.axvline(time0, color='black', linewidth=1.5)
ax1.axvline(time1, color='black', linewidth=1.5)
ax1.axvline(time2, color='black', linewidth=1.5)
ax1.axvline(time3, color='black', linewidth=1.5)
ax1.axvline(time4, color='black', linewidth=1.5)


colors_phases = {'Incipient': '#65a1e6', 'Intensification': '#f7b538',
                 'Mature': '#d62828', 'Decay': '#9aa981'}

ax1.axvspan(time0, time1, color='#65a1e6', alpha=0.3)
ax1.axvspan(time1, time2, color='#f7b538', alpha=0.3)
ax1.axvspan(time2, time3, color='#d62828', alpha=0.3)
ax1.axvspan(time3, time4, color='#9aa981', alpha=0.3)



time_ticks = df_plot['time'][::2]

ax1.set_xticks(time_ticks)  # Configurar os ticks no eixo X
ax1.set_xticklabels([t.strftime('%d %HZ') for t in time_ticks], rotation=90, fontsize=18)  # Formatando as datas
ax1.tick_params(axis='x', 
                bottom=True,          # Marcadores na parte inferior
                top=True,             # Marcadores na parte superior
                labelbottom=True,     # Rótulos na parte inferior
                labeltop=False)       # Sem rótulos na parte superior

plt.xlim(df_plot['time'][0], df_plot['time'][64])


bbox_props = dict(
    boxstyle="round,pad=0.3",
    facecolor='lightcoral',
    edgecolor='firebrick',
    alpha=0.7
)

arrow_props_bidirecional = dict(
    arrowstyle='<->',          # ⭐ Seta nas duas pontas
    color='black',
    linewidth=4,
    connectionstyle="arc3,rad=0",  # ⭐ Força linha reta
)

ax1.annotate('',
    xy=(df_plot['time'][0], 1015.7),      # Ponta 1
    xytext=(df_plot['time'][20], 1015.7),  # Ponta 2
    arrowprops=arrow_props_bidirecional,
    ha='center'
)

ax1.annotate('',
    xy=(df_plot['time'][20], 1015.7),      # Ponta 1
    xytext=(df_plot['time'][50], 1015.7),  # Ponta 2
    arrowprops=arrow_props_bidirecional,
    ha='center'
)
ax1.annotate('',
    xy=(df_plot['time'][50], 1015.7),      # Ponta 1
    xytext=(df_plot['time'][64], 1015.7),  # Ponta 2
    arrowprops=arrow_props_bidirecional,
    ha='center'
)

# Configurações do texto
text_props = {
    'fontsize': 14,          # Tamanho da fonte
    'ha': 'center',          # Alinhamento horizontal
    'va': 'bottom',          # Alinhamento vertical
    'color': 'black',        # Cor do texto
    'bbox': bbox_props       # Caixa de fundo (usando suas configurações)
}

# Altura do texto (acima das setas - ajuste conforme necessário)
text_height = 1016.5  # Um pouco acima da altura das setas (1015.7)

# Adicionar setas e textos com os rótulos especificados
ax1.annotate('',
    xy=(df_plot['time'][0], 1015.7),
    xytext=(df_plot['time'][20], 1015.7),
    arrowprops=arrow_props_bidirecional,
    ha='center'
)
ax1.text(
    x=df_plot['time'][10],  # Ponto médio entre 0 e 20
    y=text_height,
    s='Subtropical Phase',  # Primeiro rótulo
    **text_props
)

ax1.annotate('',
    xy=(df_plot['time'][20], 1015.7),
    xytext=(df_plot['time'][50], 1015.7),
    arrowprops=arrow_props_bidirecional,
    ha='center'
)
ax1.text(
    x=df_plot['time'][35],  # Ponto médio entre 20 e 50
    y=text_height,
    s='Tropical Phase',     # Segundo rótulo
    **text_props
)

ax1.annotate('',
    xy=(df_plot['time'][50], 1015.7),
    xytext=(df_plot['time'][64], 1015.7),
    arrowprops=arrow_props_bidirecional,
    ha='center'
)
ax1.text(
    x=df_plot['time'][57],  # Ponto médio entre 50 e 64
    y=text_height,
    s='Subtropical Phase',  # Terceiro rótulo
    **text_props
)


















# Crie legendas apenas para as fases que você deseja mostrar
patches = [mpatches.Patch(color=color, label=phase) for phase, color in colors_phases.items()]

# Adicione a legenda ao gráfico
plt.legend(handles=patches, loc=(0.82, 0.01))

handles, labels = [], []
handles.append(ax1.lines[0])
handles.append(ax2.lines[0])
handles.extend(patches)
labels = ['MSLP', r'$\zeta_{850}$'] + list(colors_phases.keys())

# Adicione a legenda ao gráfico
plt.legend(handles=handles, labels=labels, loc='lower left', ncol=1, fontsize=13)




DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/World_Continents.shp'
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/CSV_FILES/'


# Abrindo os dados
df = pd.read_csv(DIRCSV+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])
ds_akara = xr.open_dataset(DIRDADO+'akara_reboita1.nc')

# Carregando o shapefile
shapefile = gpd.read_file(DIRSHAPE)
shapefile = shapefile.to_crs("EPSG:4326")

# Pegando os tempos e os níveis de pressão
times = ds_akara['valid_time'].values
pressure_levels = ds_akara['pressure_level'].values

# Criando a máscara com o shapefile e ajustando a forma para coincidir com os dados
mask = geometry_mask(
    geometries=shapefile.geometry,
    transform=ds_akara.rio.transform(),  # Transforma o dataset para o CRS correto
    invert=True,
    out_shape=(ds_akara.sizes["latitude"], ds_akara.sizes["longitude"])
)

mask = xr.DataArray(mask, dims=["latitude", "longitude"], coords={
    "latitude": ds_akara["latitude"].values,
    "longitude": ds_akara["longitude"].values
})

# Lista para armazenar os resultados
zonal_deviation_results = []

# Loop para processar cada tempo
for i in range(0, len(df), 2):
    time = str(times[i])[:13]  # Exibindo até horas
    lat_center = df.loc[i, 'Lat']
    lon_center = df.loc[i, 'Lon']

    # Definindo os limites das caixas
    lat_min_grande = lat_center - 1
    lat_max_grande = lat_center + 1
    lon_min_grande = lon_center - 15
    lon_max_grande = lon_center + 15

    lat_min_peq = lat_center - 1
    lat_max_peq = lat_center + 1
    lon_min_peq = lon_center - 5
    lon_max_peq = lon_center + 5

    # Selecionando os dados dentro das caixas e para o tempo
    temp_box_grande = ds_akara['t'].sel(
        latitude=slice(lat_max_grande, lat_min_grande),
        longitude=slice(lon_min_grande, lon_max_grande),
        valid_time=times[i]
    )

    # Aplicando a máscara para excluir os dados dentro do continente
    temp_box_grande_masked = temp_box_grande.where(mask == 0)

    # Selecionando o intervalo de dados menor
    temp_box_pequena = ds_akara['t'].sel(
        latitude=slice(lat_max_peq, lat_min_peq),
        longitude=slice(lon_min_peq, lon_max_peq),
        valid_time=times[i]
    )
    temp_box_pequena_masked = temp_box_pequena.where(mask == 0)

    # Calculando a temperatura média
    mean_temp_grande = temp_box_grande_masked.mean(dim=['latitude', 'longitude'], skipna=True).values
    mean_temp_pequena = temp_box_pequena_masked.mean(dim=['latitude', 'longitude'], skipna=True).values

    # Calculando o desvio zonal de temperatura
    mean_temp_reboita = np.where(
        np.isnan(mean_temp_pequena) | np.isnan(mean_temp_grande),
        np.nan,
        mean_temp_pequena - mean_temp_grande
    )

    if np.isnan(mean_temp_reboita).any():
        print(f"Erro: mean_temp_reboita contém NaN para o tempo {time}!")
        break

    # Salvando os resultados na lista para cada nível de pressão
    for pressure_level, theta_mean in zip(pressure_levels, mean_temp_reboita):
        zonal_deviation_results.append({
            'time': time,
            'pressure_level': pressure_level,
            'theta_zonal_mean': theta_mean  # Salvando o valor da média de desvio zonal de temperatura
        })

# Criando DataFrame para os resultados de desvio zonal
df_results = pd.DataFrame(zonal_deviation_results)

# Pivotando o DataFrame para colocar 'time' como índice e 'pressure_level' como colunas
df_pivot = df_results.pivot(index='pressure_level', columns='time', values='theta_zonal_mean')
df_pivoted = df_pivot.sort_index(ascending=False)

# Exibindo as primeiras linhas para verificar o formato
print(df_pivoted.head())
# Aplicando um filtro Gaussiano para suavizar os dados
smoothed_data = scipy.ndimage.gaussian_filter(df_pivoted.values, sigma=1.2)
# Criando o gráfico

# Criando o gráfico de contorno
im = ax3.contourf(df_pivoted.columns, df_pivoted.index, smoothed_data,
                 levels=np.arange(-1, 1.1, 0.2), cmap=plt.get_cmap("coolwarm"), extend='both')
# Barra de cores
cbar = fig.colorbar(im, ax=ax3, orientation='horizontal', pad=0.02)
cbar.set_label("Temperature (°C)", fontsize=18)  # Rótulo da barra de cores
cbar.ax.tick_params(labelsize=16)
ax3.invert_yaxis()
ax3.set_ylim(1000, 200)
# Ajustando o eixo Y para escala logarítmica
ax3.set_yscale('log')
# Definindo os valores de pressão para os rótulos
pressure_ticks = [1000, 900, 800, 700, 600, 500, 400, 300, 200]
# Definindo os rótulos visíveis no eixo Y
ax3.set_yticks(pressure_ticks)
ax3.set_yticklabels(pressure_ticks, fontsize=18)  # Ticks com os valores de pressão
# Definindo os rótulos de pressão reais
ax3.set_yticklabels(pressure_ticks)  # Rótulos de pressão reais
ax3.set_ylabel("Pressure (hPa)", fontsize=18)


# Lista das datas desejadas para o eixo X
desired_dates = ['2024-02-14T21', '2024-02-16T09', '2024-02-19T15', '2024-02-20T09', '2024-02-22T21']

# Convertendo as datas para o formato de string conforme necessário
desired_dates_str = pd.to_datetime(desired_dates)
# Convertendo para strings, que o Matplotlib pode entender facilmente
desired_dates_str = [dt.strftime('%m-%d %HZ') for dt in desired_dates_str]
# Pegando os índices das colunas para as datas desejadas
desired_date_indices = df_pivoted.columns.get_indexer_for(desired_dates)
# Adicionando as linhas verticais para as outras datas desejadas
for date_index in desired_date_indices:
    ax3.axvline(x=df_pivoted.columns[date_index], color='black', linestyle='--', linewidth=1)
# Definindo explicitamente os ticks do eixo X para as datas desejadas
#ax3.set_xticks(df_pivoted.columns[desired_date_indices])
#formatted_dates = pd.to_datetime(df_pivoted.columns).strftime('%d %HZ')
# Ajustando os rótulos do eixo X para as datas no formato desejado
ax3.tick_params(axis='x', bottom=False, top=True, labelbottom=False, labeltop=True)
#ax3.set_xticks(df_pivoted.columns)  # Definindo os ticks do eixo X
#ax3.set_xticklabels(formatted_dates, rotation=90, fontsize=18)
ax3.set_xticklabels([])
x_positions = range(len(df_pivoted.columns))

# Configuração comum para todas as caixas
bbox_props = dict(
    boxstyle="round,pad=0.3",
    facecolor='lightcoral',
    edgecolor='firebrick',
    alpha=0.7
)

arrow_props_bidirecional = dict(
    arrowstyle='<->',          # ⭐ Seta nas duas pontas
    color='black',
    linewidth=4,
    connectionstyle="arc3,rad=0",  # ⭐ Força linha reta
)

ax3.annotate('',
    xy=(x_positions[0], 210),      # Ponta 1
    xytext=(x_positions[10], 210),  # Ponta 2
    arrowprops=arrow_props_bidirecional,
    ha='center'
)

ax3.annotate('',
    xy=(x_positions[10], 210),      # Ponta 1
    xytext=(x_positions[25], 210),  # Ponta 2
    arrowprops=arrow_props_bidirecional,
    ha='center'
)
ax3.annotate('',
    xy=(x_positions[25], 210),      # Ponta 1
    xytext=(x_positions[32], 210),  # Ponta 2
    arrowprops=arrow_props_bidirecional,
    ha='center'
)

##ax3.text(
##    x=(x_positions[0] + x_positions[10]) / 2,  # Centro da primeira seta
##    y=150,
##    s='Subtropical Phase',
##    bbox=bbox_props,
##    ha='center',
##    va='center',
##    fontsize=14  # Tamanho da fonte
##)
##
#ax3.text(
#    x=(x_positions[10] + x_positions[25]) / 2,
#    y=800,
#    s='Tropical Phase',
#    bbox=bbox_props,
#    ha='center',
#    va='center',
#    fontsize=14
#)
#ax3.text(
#    x=(x_positions[25] + x_positions[32]) / 2,
#    y=800,
#    s='Subtropical Phase',
#    bbox=bbox_props,
#    ha='center',
#    va='center',
#    fontsize=14
#)


plt.savefig(DIRFIG+'combined_serie_zonaldeviation.png', dpi=300, bbox_inches='tight')
