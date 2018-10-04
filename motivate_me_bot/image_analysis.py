from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

import numpy as np

import sys
import os

def average_color(img, background_box, inverse=True):

    r_tot = 0
    g_tot = 0
    b_tot = 0
    cropped_img = img.crop(background_box)
    rgb_data = cropped_img.getdata()
    for (r,g,b) in rgb_data:
        r_tot += r
        g_tot += g
        b_tot += b
    pixel_num = len(rgb_data)
    averages = (int(np.round(r_tot / pixel_num)),
            int(np.round(g_tot / pixel_num)),
            int(np.round(b_tot / pixel_num)))
    if inverse:
        return tuple([(255-x) for x in averages])
    else:
        return averages

def contrast_color(img, background_box):
    r, g, b = average_color(img, background_box, inverse=False)
    perceived_luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    if perceived_luminance > 0.5:
        return (0,0,0)
    else:
        return (255,255,255)
