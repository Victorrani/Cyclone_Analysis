import imageio.v2 as imageio
import os

path = "/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Automated_Figures/sat_ch13"
output_file = "akara.mp4"
fps = 15

images = sorted([img for img in os.listdir(path) if img.endswith(".png") or img.endswith(".jpg")])

writer = imageio.get_writer(
    output_file,
    fps=fps,
    codec='libx264',
    quality=8,  # escala de 0 (pior) a 10 (melhor)
    ffmpeg_params=[
        '-crf', '18',     # controle de compressão (quanto menor, melhor qualidade)
        '-preset', 'slow' # controle de tempo x compressão (ultrafast, fast, medium, slow...)
    ]
)

for filename in images:
    image = imageio.imread(os.path.join(path, filename))
    writer.append_data(image)
writer.close()

print(f"Vídeo salvo como {output_file}")
