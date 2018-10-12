from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

import numpy as np

import sys
import os

from image_sizing import *

def draw_box(img, box, line_width=1):
    x1, y1, x2, y2 = box
    box_width = x2 - x1
    box_height = y2 - y1
    boundary = get_boundary(img)
    if line_width is None:
        line_width = int(boundary / 15)
        if line_width % 2 == 0:
            line_width += 1

    draw = ImageDraw.Draw(img)
    draw.line((x1, y1 - line_width / 2 + 1, x1, y1 + box_height + line_width / 2 - 1), width=line_width)
    draw.line((x1, y1, x1 + box_width, y1), width=line_width)
    draw.line((x1 + box_width, y1 + box_height, x1, y1 + box_height), width=line_width)
    draw.line((x1 + box_width, y1 + box_height + line_width / 2 - 1, x1 + box_width, y1 - line_width / 2 + 1), width=line_width)

def constant_blur(img, background_box, blur_radius):
    region = img.crop(background_box)
    region = region.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img.paste(region, background_box)

def blur_box(img, background_box, max_blur_radius, n=0):
    '''
    Blur section of img object according to the background box of locations and
    blur radius
    '''
    if n == 0:
        constant_blur(img, background_box, max_blur_radius)
    elif n > 0:
        box = x1, y1, x2, y2 = background_box
        width = x2 - x1
        height = y2 - y1

        # blur_radius = max_blur_radius / (n + 1)
        for i in range(n, -1, -1):
            blur_radius = max_blur_radius * np.sqrt(i + 1) / np.sqrt(n + 1)**2
            box = (x1 + int(i / n * width / 4),
                   y1 + int(i / n * height / 4),
                   x2 - int(i / n * width / 4),
                   y2 - int(i / n * height / 4))

            constant_blur(img, box, blur_radius)
            # draw_box(img, box)
