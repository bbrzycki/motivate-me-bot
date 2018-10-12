from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

import numpy as np

import sys
import os

from text_color import *

from image_sizing import get_boundary, get_box_corners

from blur import *

def draw_quote_in_box(img,
                      box_corners,
                      all_lines=['Hello, world!'],
                      font_file='Apple Chancery.ttf',
                      font_size=14,
                      color=None,
                      min_font_size=14,
                      spacing=1,
                      equal_spacing=True,
                      max_char_height=None,
                      draw_box=True):
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    boundary = get_boundary(img)
    blur_boundary = int(boundary / 8)

    x1, y1, x2, y2 = box_corners
    box_width = x2 - x1
    box_height = y2 - y1

    font = ImageFont.truetype(font_file, max(font_size, min_font_size))

    if max_char_height is None:
        # Compute max_char_height
        pass

    if equal_spacing:
        text_block_height = max_char_height * (len(all_lines) + 1) * spacing * 1.2
    else:
        text_block_height = max_char_height * ((len(all_lines) - 1) * spacing * 1.2 + 1)

    background_box = (x1 - blur_boundary, y1 - blur_boundary,
                      x1 + blur_boundary + box_width, y1 + blur_boundary + box_height)

    if color is None:
        color = overall_contrast_color(img, background_box)

    gradient_blur(img, background_box, 2 * blur_boundary, n=int(box_height/16))

    for i, line in enumerate(all_lines):
        line_width, line_height = font.getsize(line)
        x_coord = x1 + box_width / 2 - line_width / 2
        if equal_spacing:
            y_coord = y1 + box_height / 2 - text_block_height / 2 + max_char_height * ((i + 1) * spacing * 1.2 - 0.5)
        else:
            y_coord = y1 + box_height / 2 - text_block_height / 2 + max_char_height * i * spacing * 1.2
        draw.text((x_coord, y_coord),
                   line,
                   color,
                   font=font)

    if draw_box:
        draw_box(img, background_box)

def draw_signature(img,
                   user='@MotivateMeBot',
                   font_file='AppleGothic.ttf',
                   color=None,
                   min_font_size=14):
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    boundary = get_boundary(img)
    sig_size = max(int(boundary / 2), min_font_size * 2)
    blur_boundary = int(sig_size / 2)

    # MotivateMeBot sig
    sig = user
    sig_font = ImageFont.truetype(font_file, sig_size)
    sig_width, sig_height = sig_font.getsize(sig)

    background_box = (img_width - blur_boundary - sig_width - sig_size, img_height - blur_boundary - sig_height - sig_size,
                      img_width + blur_boundary - sig_size, img_height + blur_boundary - sig_size)

    if color is None:
        color = overall_contrast_color(img, background_box)

    gradient_blur(img, background_box, blur_boundary, n=int(sig_height/4))

    draw.text((img_width - sig_width - sig_size, img_height - sig_height - sig_size),
               sig,
               color,
               font=sig_font)

def draw_credits(img,
                 quote_name,
                 quote_screen_name,
                 image_name,
                 image_screen_name,
                 font_file='AppleGothic.ttf',
                 color=None,
                 min_font_size=14):
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    boundary = get_boundary(img)
    sig_size = max(int(boundary / 2), min_font_size * 2)
    cred_size = int(sig_size / 2)
    blur_boundary = int(cred_size / 2)

    cred_font = ImageFont.truetype(font_file, cred_size)

    # Image Credit
    image_cred = 'Image Credit: %s (@%s)' % (image_name, image_screen_name)
    image_cred_width, image_cred_height = cred_font.getsize(image_cred)

    # Quote Credit
    quote_cred = 'Quote Credit: %s (@%s)' % (quote_name, quote_screen_name)
    quote_cred_width, quote_cred_height = cred_font.getsize(quote_cred)

    background_box = (sig_size - blur_boundary, img_height - blur_boundary - image_cred_height - quote_cred_height - sig_size,
                         sig_size + blur_boundary + max(image_cred_width, quote_cred_width), img_height + blur_boundary - sig_size)

    if color is None:
        color = overall_contrast_color(img, background_box)

    gradient_blur(img, background_box, blur_boundary, n=int((image_cred_height+quote_cred_height)/4))

    draw.text((sig_size, img_height - image_cred_height - sig_size),
                image_cred,
                color,
                font=cred_font)

    draw.text((sig_size, img_height - image_cred_height * 1.2 - quote_cred_height - sig_size),
               quote_cred,
               color,
               font=cred_font)
