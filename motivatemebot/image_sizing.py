import sys
from PIL import Image

def get_image(image_path):
    return Image.open(image_path)

def get_boundary(img, scaling=16):
    img_width, img_height = img.size
    return min(int(img_width / scaling), int(img_height / scaling))

def get_box_corners(img, location='top'):
    img_width, img_height = img.size

    boundary = get_boundary(img)
    box_width = img_width - 2 * boundary
    box_height = int(img_height / 2) - 2 * boundary

    x1 = boundary
    x2 = x1 + box_width
    if location == 'top':
        y1 = boundary
        y2 = int(img_height / 2) - y1
    elif location == 'middle':
        y1 = int(img_height / 4) + boundary
        y2 = img_height - y1
    else:
        sys.exit('Invalid box location specified!')
    return (x1, y1, x2, y2)
