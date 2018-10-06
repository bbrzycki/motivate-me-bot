from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

import numpy as np

import sys
import os

from image_sizing import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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

def average_contrast_color(img, background_box):
    r, g, b = average_color(img, background_box, inverse=False)
    perceived_luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if perceived_luminance > 0.5:
        return BLACK
    else:
        return WHITE

def get_all_luminances(img, background_box, range=64):
    if range > 256:
        sys.exit('Invalid range!')
    cropped_img = img.crop(background_box)
    luminances = []
    for (r,g,b) in cropped_img.convert('RGB').getdata():
        perceived_luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        luminances.append(perceived_luminance)
    light = 0
    dark = 0
    for luminance in luminances:
        if luminance < range:
            dark += 1
        if luminance > 255 - range:
            light += 1
    return light, dark

def overall_contrast_color(img, background_box, range=64):
    light, dark = get_all_luminances(img, background_box, range=range)
    ratio = light / dark
    if ratio >= 1 or dark == 0:
        return BLACK
    else:
        return WHITE

def select_region_and_color(img, range=64):
    top_box = get_box_corners(img, location='top')
    middle_box = get_box_corners(img, location='middle')

    top_light, top_dark = get_all_luminances(img, top_box, range=range)
    middle_light, middle_dark = get_all_luminances(img, middle_box, range=range)

    shades = [('top_light', top_light),
              ('top_dark', top_dark),
              ('middle_light', middle_light),
              ('middle_dark', middle_dark)]
    shades.sort(key=(lambda x: x[1]))
    minimum_shade = shades[0][0]

    if minimum_shade == 'top_light':
        return 'top', WHITE
    elif minimum_shade == 'top_dark':
        return 'top', BLACK
    elif minimum_shade == 'middle_light':
        return 'middle', WHITE
    else: # minimum_shade == 'middle_dark'
        return 'middle', BLACK
