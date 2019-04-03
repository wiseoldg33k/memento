from PIL import Image
from resizeimage import resizeimage


def crop_profile_picture(input_file, output_file):
    with open(input_file, "rb") as fd_img:
        img = Image.open(fd_img)
        img = resizeimage.resize_height(img, 200)
        img = resizeimage.resize_crop(img, [112, 200])
        img.save(output_file, img.format)
        fd_img.close()

    return True
