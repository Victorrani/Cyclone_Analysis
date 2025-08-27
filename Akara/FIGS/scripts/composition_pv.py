import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Specific_Figures/pv_composition/' 
os.makedirs(DIRFIG, exist_ok=True)
caminho = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Automated_Figures/pv_corte/'
# imagens e rótulos
img_pv = [
    caminho+'Akara_cross_2024-02-16T21.png',
    caminho+'Akara_cross_2024-02-19T00.png',
    caminho+'Akara_cross_2024-02-19T06.png',
    caminho+'Akara_cross_2024-02-21T03.png'
]
labels = ['(a)', '(b)', '(c)', '(d)']  # rótulos para cada subfigura

# cria figura 2x2
fig, axes = plt.subplots(2, 2, figsize=(12, 7.2))
axes = axes.ravel()  # transforma em lista

for ax, img_path, label in zip(axes, img_pv, labels):
    img = mpimg.imread(img_path)
    ax.imshow(img)
    ax.axis('off')
    ax.text(
        0.78, 0.9, label, transform=ax.transAxes,
        ha='left', va='top', fontsize=16, fontweight='bold', color='black'
    )

plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.01, hspace=0)

outpath = os.path.join(DIRFIG, 'composition.png')
plt.savefig(outpath, dpi=300, bbox_inches='tight', pad_inches=0)
plt.close(fig)

print(f'✔ salvo: {outpath}')
