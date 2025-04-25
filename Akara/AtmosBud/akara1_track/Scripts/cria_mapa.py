import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.ticker import ScalarFormatter
from matplotlib.dates import DateFormatter

# Diretórios dos dados e das figuras
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/Figures/V_balanc_track/'

# Arquivos
arquivo_sigma = DIRDADO + 'Sigma_omega.csv'
arquivo_ck = DIRDADO + 'Ck_pressure_level.csv'

# Cria figura com 2 linhas e 1 coluna
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 10), sharex=True)

# ========= PRIMEIRO GRÁFICO: SigmaOmega =========
df1 = pd.read_csv(arquivo_sigma, index_col=0)
df1.columns = pd.to_datetime(df1.columns, utc=True).tz_convert(None)
df1.index = df1.index / 100  # Pa para hPa

norm1 = TwoSlopeNorm(vmin=-15, vcenter=0, vmax=8)
im1 = ax[0].contourf(df1.columns, df1.index, df1.values * 86400, cmap='coolwarm', extend='both',
                     norm=norm1, levels=np.linspace(-15, 8, 11))

cbar1 = fig.colorbar(im1, ax=ax[0], pad=0.01)
cbar1.set_label('[K / day]', fontsize=14)
cbar1.ax.tick_params(labelsize=15)


ax[0].invert_yaxis()
ax[0].set_ylim(1000, 100)
ax[0].set_yscale('log')
ax[0].set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
ax[0].set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
ax[0].set_ylabel("Pressure (hPa)", fontsize=18)
ax[0].set_title('Total Vertical Motion Effect', fontsize=16, loc='left')
for time in ['2024-02-14T21', '2024-02-16T09', '2024-02-19T15', '2024-02-20T06']:
    ax[0].axvline(pd.to_datetime(time), color='k', linestyle='--')
ax[0].tick_params(labelsize=15)

# ========= SEGUNDO GRÁFICO: Ck =========
df2 = pd.read_csv(arquivo_ck, index_col=0).T
df2.columns = pd.to_datetime(df2.columns, utc=True).tz_convert(None)
df2.index = pd.to_numeric(df2.index, errors='coerce') / 100
df2 = df2.dropna()

norm2 = TwoSlopeNorm(vmin=-20e-4, vcenter=0, vmax=9e-4)
im2 = ax[1].contourf(df2.columns, df2.index, df2.values, cmap='coolwarm', extend='both',
                     norm=norm2, levels=np.linspace(-20e-4, 9e-4, 11))

cbar2 = fig.colorbar(im2, ax=ax[1], pad=0.01)
cbar2.set_label('W/m²', fontsize=14)
cbar2.ax.tick_params(labelsize=15)
cbar2.formatter = ScalarFormatter(useMathText=True)
cbar2.formatter.set_scientific(True)
cbar2.formatter.set_powerlimits((-3, 3))
cbar2.update_ticks()

ax[1].invert_yaxis()
ax[1].set_ylim(1000, 100)
ax[1].set_yscale('log')
ax[1].set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
ax[1].set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
ax[1].set_ylabel("Pressure (hPa)", fontsize=18)
ax[1].set_title('Ck', fontsize=16, loc='left')
for time in ['2024-02-14T21', '2024-02-16T09', '2024-02-19T15', '2024-02-20T06']:
    ax[1].axvline(pd.to_datetime(time), color='k', linestyle='--')
ax[1].xaxis.set_major_locator(mdates.AutoDateLocator())
ax[1].xaxis.set_major_formatter(DateFormatter('%m-%d'))
ax[1].tick_params(axis='x', labelrotation=90, labelsize=16)
ax[1].tick_params(axis='y', labelsize=15)

# Salvar a figura final
output_path = DIRFIGS + 'SigmaOmega_Ck_combined_hov.png'
plt.savefig(output_path, bbox_inches='tight', dpi=300)
plt.close()

print(f"Figura combinada salva em: {output_path}")
