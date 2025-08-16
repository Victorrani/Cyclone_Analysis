import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patheffects as pe
import os

DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Specific_Figures/new_figs/' 
DIR_SST = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Specific_Figures/sst_t2m/'
DIR_SAT = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Automated_Figures/sat_vento/'
DIR_GEO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Automated_Figures/pv200_1/'


for i in range(0, 62, 1):

    arquivos_sst = sorted([f for f in os.listdir(DIR_SST) if os.path.isfile(os.path.join(DIR_SST, f))])
    arquivos_sat = sorted([f for f in os.listdir(DIR_SAT) if os.path.isfile(os.path.join(DIR_SAT, f))])
    arquivos_geo = sorted([f for f in os.listdir(DIR_GEO) if os.path.isfile(os.path.join(DIR_GEO, f))])
    
    imgs = [DIR_SAT+arquivos_sat[i], DIR_SST+arquivos_sst[i+3], DIR_GEO+arquivos_geo[i]]

    
    labels = ['a)', 'b)', 'c)']

    # Figura más “achatada” para 1×4, sin layout automático
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))

    for ax, img_path, label in zip(axes, imgs, labels):
        img = mpimg.imread(img_path)
        ax.imshow(img)
        ax.axis('off')
        # Letra dentro de la imagen (esquina superior derecha)
        ax.text(
            0.75, 0.9, label, transform=ax.transAxes,  # usa (0.02, 0.98) si la quieres arriba-izq
            ha='right', va='bottom', fontsize=16, fontweight='bold'  # borde para contraste
        )

    # Márgenes y espacios mínimos
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.01, hspace=0)

    # Guardado sin relleno extra
    plt.savefig(f'{DIRFIG}composition_{i+1}.png', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
