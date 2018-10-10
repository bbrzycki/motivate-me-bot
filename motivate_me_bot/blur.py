from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

import numpy as np

import sys
import os

def blur_box(img, background_box, blur_radius):
    '''
    Blur section of img object according to the background box of locations and
    blur radius
    '''
    region = img.crop(background_box)
    region = region.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img.paste(region, background_box)
    
def gradient_blur_box(img, background_box, max_blur_radius):
    pass
