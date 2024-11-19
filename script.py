from PIL import Image
import os
import sys
import math


def main():
    if len(sys.argv) != 4:
        print("Utilizzo: python script_nome.py immagine.tiff percentuale cartella_output")
        print("Esempio: python script_nome.py immagine.tiff 50 output_folder")
        sys.exit(1)

    input_image_path = sys.argv[1]
    scaling_percentage = float(sys.argv[2])
    output_folder = sys.argv[3]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_image_name = os.path.splitext(os.path.basename(input_image_path))[0]

    subfolder_name = input_image_name
    subfolder_path = os.path.join(output_folder, subfolder_name)
    suffix = 1
    while os.path.exists(subfolder_path):
        subfolder_name = f"{input_image_name}_{suffix}"
        subfolder_path = os.path.join(output_folder, subfolder_name)
        suffix += 1

    os.makedirs(subfolder_path)

    try:
        img = Image.open(input_image_path)
    except IOError:
        print("Impossibile aprire l'immagine.")
        sys.exit(1)

    width, height = img.size
    new_width = int(width * scaling_percentage / 100)
    new_height = int(height * scaling_percentage / 100)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    tile_width = 512
    tile_height = 512

    n_cols = math.ceil(new_width / tile_width)
    n_rows = math.ceil(new_height / tile_height)

    for row in range(n_rows):
        for col in range(n_cols):
            left = col * tile_width
            upper = row * tile_height
            right = min(left + tile_width, new_width)
            lower = min(upper + tile_height, new_height)
            box = (left, upper, right, lower)
            tile = img.crop(box)
            tile_path = os.path.join(subfolder_path, f"tile_r{row}_c{col}.png")  
            tile.save(tile_path, format='PNG') 

    print(f"Operazione completata. I blocchi sono stati salvati nella cartella '{subfolder_path}'.")

if __name__ == "__main__":
    main()