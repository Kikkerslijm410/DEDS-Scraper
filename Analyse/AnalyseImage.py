import extcolors
import os
import concurrent.futures
import math
from collections import Counter
from Database import (drop_table,conn,cursor,create_table)

table_name = "PopularColors"
drop_table(table_name)
print ("INFO: Table dropped")
create_table(table_name, "color","total")
print ("INFO: Table 'PopularColors' created")

def insert_data(color, total):
    query = f"INSERT INTO {table_name} (color, total) VALUES (?, ?)"
    cursor.execute(query, color, total)
    conn.commit()
    
COLORS = {
    "red": ((255, 0, 0), (255, 99, 71)),
    "orange": ((255, 165, 0), (255, 140, 0)),
    "yellow": ((255, 255, 0), (255, 215, 0)),
    "green": ((0, 128, 0), (0, 255, 0)),
    "blue": ((0, 0, 255), (0, 0, 128)),
    "purple": ((128, 0, 128), (218, 112, 214)),
    "pink": ((255, 192, 203), (255, 105, 180)),
    "brown": ((165, 42, 42), (139, 69, 19)),
    "black": ((0, 0, 0), (25, 25, 25)),
    "white": ((255, 255, 255), (245, 245, 245)),
    "gray": ((128, 128, 128), (169, 169, 169)),
    "navy": ((0, 0, 128), (0, 0, 139)),
    "olive": ((128, 128, 0), (107, 142, 35)),
    "silver": ((192, 192, 192), (211, 211, 211)),
    "gold": ((255, 215, 0), (255, 165, 0)),
    "sky blue": ((135, 206, 235), (135, 206, 250)),
    "turquoise": ((64, 224, 208), (0, 245, 255)),
    "indigo": ((75, 0, 130), (138, 43, 226)),
    "violet": ((238, 130, 238), (148, 0, 211)),
    "beige": ((245, 245, 220), (245, 245, 220)),
    "magenta": ((255, 0, 255), (199, 21, 133)),
    "orchid": ((218, 112, 214), (255, 131, 250)),
    "peach": ((255, 218, 185), (255, 229, 180)),
    "salmon": ((250, 128, 114), (255, 99, 71)),
    "tan": ((210, 180, 140), (210, 180, 140))
}

def determine_closest_color(rgb):
    min_distance = math.inf
    closest_color = "unknown"
    for color, (min_rgb, max_rgb) in COLORS.items():
        r_distance = rgb[0] - (min_rgb[0] + max_rgb[0]) / 2
        g_distance = rgb[1] - (min_rgb[1] + max_rgb[1]) / 2
        b_distance = rgb[2] - (min_rgb[2] + max_rgb[2]) / 2
        distance = math.sqrt(r_distance ** 2 + g_distance ** 2 + b_distance ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color

def most_common_colors(img_file):
    img_file = os.path.join("OutputOld/Images", img_file)
    colors = extcolors.extract_from_path(img_file, tolerance=12, limit=12)[0]
    color_counts = Counter(dict(colors)).most_common(4)
    print(f" picture {img_file} is done")
    del color_counts[0]
    return [color[0] for color in color_counts]

def main():
    img_files = os.listdir("OutputOld/Images")
    colors_dict = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(most_common_colors, img_file) for img_file in img_files]
        list_colors = [color for future in concurrent.futures.as_completed(futures) for color in future.result()]
    for rgb in list_colors:
        color = determine_closest_color(rgb)
        if color in colors_dict:
            colors_dict[color] += 1
        else:
            colors_dict[color] = 1
    for color in colors_dict:
        insert_data(color, colors_dict[color])
    print("Data has been saved in database")
if __name__ == '__main__':
    print("Analyse has been started")
    main()
    print("Analysis has ended")

