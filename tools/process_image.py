import os
import shutil
from PIL import Image 


def get_dir_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def print_dir_size(path):
    res = get_dir_size(path)
    print('Drictory size: {:,} bytes'.format(res).replace(',', ' '))
    print('Drictory size: {:,} KB'.format(int(res/1024)).replace(',', ' '))
    print('Drictory size: {:,} MB'.format(int(res/1024**2)).replace(',', ' '))
    # print('Drictory size: {:,} GB'.format(int(res/1024**3)).replace(',', ' '))
    # print('Drictory size: {:,} TB'.format(int(res/1024**4)).replace(',', ' '))

def crop_images():
    '''
    For cropping ship images, 363x88 -> 156x88
    '''
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
            print("Cropping {}".format(f))
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
            pass

    print("==== Before ====")
    print_dir_size(img_dir)
    print("==== After ====")
    print_dir_size(res_dir)

def resize_images():
    '''
    For resizing equipment images, 512x512 -> 64x64
    '''
    img_dir = "./equip_512/"
    res_dir = "../src/assets/E/"
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    else:
        print("clearing contents")
        shutil.rmtree(res_dir)
        os.makedirs(res_dir)

    for f in os.listdir(img_dir):
        if f.endswith(".png"):
            print("Resizing {}".format(f))
            src_path = img_dir + f
            img = Image.open(src_path)
            # 512x512 -> 64x64
            w, h = img.size
            new_w = int(w / 8)
            new_h = int(h / 8)
            new_img = img.resize((new_w, new_h))
            res_path = res_dir + f
            new_img.save(res_path)
        else:
            pass
    print("==== Before ====")
    print_dir_size(img_dir)
    print("==== After ====")
    print_dir_size(res_dir)

# crop_images()
# resize_images()