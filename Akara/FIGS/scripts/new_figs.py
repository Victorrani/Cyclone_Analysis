import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patheffects as pe

DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Specific_Figures/new_figs/' 
DIR_SST = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Specific_Figures/sst_t2m/'
DIR_SAT = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Automated_Figures/sat_vento/'
DIR_GEO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Automated_Figures/pv200_1/'

os.makedirs(DIRFIG, exist_ok=True)

img_sat = [
    'ch13_AKARA_vento2024021421.png', 'ch13_AKARA_vento2024021521.png',
    'ch13_AKARA_vento2024021621.png', 'ch13_AKARA_vento2024021721.png',
    'ch13_AKARA_vento2024021915.png', 'ch13_AKARA_vento2024022012.png',
]
img_sst = [
    'Akara_mslp_sst_t2m2024-02-14T21.png', 'Akara_mslp_sst_t2m2024-02-15T21.png',
    'Akara_mslp_sst_t2m2024-02-16T21.png', 'Akara_mslp_sst_t2m2024-02-17T21.png',
    'Akara_mslp_sst_t2m2024-02-19T15.png', 'Akara_mslp_sst_t2m2024-02-20T12.png',
]
img_geo = [
    'Akara_wind_speed_z500_2024-02-14T21.png', 'Akara_wind_speed_z500_2024-02-15T21.png',
    'Akara_wind_speed_z500_2024-02-16T21.png', 'Akara_wind_speed_z500_2024-02-17T21.png',
    'Akara_wind_speed_z500_2024-02-19T15.png', 'Akara_wind_speed_z500_2024-02-20T12.png',
]

labels = ['a)', 'b)', 'c)']

# segurança: garantir que as três listas têm o mesmo tamanho
n = min(len(img_sat), len(img_sst), len(img_geo))
for k, (sat_fn, sst_fn, geo_fn) in enumerate(zip(img_sat[:n], img_sst[:n], img_geo[:n]), start=1):
    paths = [
        os.path.join(DIR_SAT, sat_fn),
        os.path.join(DIR_SST, sst_fn),
        os.path.join(DIR_GEO, geo_fn),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    for ax, img_path, label in zip(axes, paths, labels):
        img = mpimg.imread(img_path)
        ax.imshow(img)
        ax.axis('off')
        ax.text(
            0.7, 0.97, label, transform=ax.transAxes,
            ha='left', va='top', fontsize=16, fontweight='bold', color='black')

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.01, hspace=0)
    outpath = os.path.join(DIRFIG, f'composition_{k:02d}.png')
    plt.savefig(outpath, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    print(f'✔ salvo: {outpath}')
