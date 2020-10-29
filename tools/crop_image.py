import os
from PIL import Image 

img_dir = "./S/"
res_dir = "../src/assets/S_cropped/"
if not os.path.exists(res_dir):
    os.makedirs(res_dir)
else:
    pass
for f in os.listdir(img_dir):
    if f.endswith(".png"):
        print("processing {}".format(f))
        src_path = img_dir + f
        img = Image.open(src_path)
        w, h = img.size
        left = 100
        right = w - left
        top = 0
        bottom = h
        img_res = img.crop((left, top, right, bottom))
        res_path = res_dir + f
        img_res.save(res_path)
    else:
        continue