import os
import shutil
from PIL import Image 

img_dir = "./S/"
res_dir = "../src/assets/S/"
if not os.path.exists(res_dir):
    os.makedirs(res_dir)
else:
    print("clearing contents")
    shutil.rmtree(res_dir)
    os.makedirs(res_dir)
for f in os.listdir(img_dir):
    if f.endswith(".png"):
        print("processing {}".format(f))
        src_path = img_dir + f
        img = Image.open(src_path)
        # 363 x 88
        w, h = img.size
        # adding offset to make 156x88 so we can scale using common factors
        left = 100 + 3
        right = w - left - 1
        top = 0
        bottom = h
        img_res = img.crop((left, top, right, bottom))
        res_path = res_dir + f
        img_res.save(res_path)
    else:
        continue