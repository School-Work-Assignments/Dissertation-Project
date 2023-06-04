import os
from PIL import Image
import imghdr

# Declaring data directories*
input_dir = 'Outputs/Heightmaps'
output_dir = 'Outputs/BMP_Heightmaps/'

for file in os.listdir(input_dir):
    path = os.path.join(input_dir, file)
    name_full = os.path.basename(path)
    name_stripped = os.path.splitext(name_full)[0]

    if os.path.isfile(path) and imghdr.what(path) == "png":
        img_png = Image.open(path)
        img_porcessed =  img_png.convert("P", palette=Image.ADAPTIVE, colors=8)
        img_porcessed.save(output_dir + name_stripped + ".bmp")