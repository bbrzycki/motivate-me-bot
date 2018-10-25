from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

import numpy as np

import sys
import os

from image_sizing import get_image, get_boundary, get_box_corners
from text_formatting import fit_text_to_box
from text_color import average_color, average_contrast_color, get_all_luminances, \
    overall_contrast_color, select_region_and_color, check_image_colors

def quote_width(img,
                  all_lines=['Hello, world!'],
                  quote_font_file='Apple Chancery.ttf',
                  font_size=14,
                  min_font_size=14):
    font = ImageFont.truetype(quote_font_file, max(font_size, min_font_size))
    max_width = 0
    for line in all_lines:
        line_width, line_height = font.getsize(line)
        if line_width > max_width:
            max_width = line_width
    return max_width

def signature_width(img,
                   user='@MotivateMeBot',
                   footer_font_file='AppleGothic.ttf',
                   min_font_size=14):
    boundary = get_boundary(img)
    sig_size = max(int(boundary / 2), min_font_size * 2)

    sig = user
    sig_font = ImageFont.truetype(footer_font_file, sig_size)
    sig_width, sig_height = sig_font.getsize(sig)
    return sig_width

def credit_width(img, name, screen_name, footer_font_file='AppleGothic.ttf', min_font_size=14):
    boundary = get_boundary(img)
    sig_size = max(int(boundary / 2), min_font_size * 2)
    cred_size = int(sig_size / 2)

    cred_font = ImageFont.truetype(footer_font_file, cred_size)

    # Image Credit
    image_cred = 'Image Credit: %s (@%s)' % (name, screen_name)
    image_cred_width, image_cred_height = cred_font.getsize(image_cred)

    # Quote Credit
    quote_cred = 'Quote Credit: %s (@%s)' % (name, screen_name)
    quote_cred_width, quote_cred_height = cred_font.getsize(quote_cred)
    return max(image_cred_width, quote_cred_width)

def full_credits_width(img,
                 quote_name,
                 quote_screen_name,
                 image_name,
                 image_screen_name,
                 footer_font_file='AppleGothic.ttf',
                 min_font_size=14):
    image_cred_width = credit_width(img, image_name, image_screen_name, footer_font_file=footer_font_file, min_font_size=min_font_size)
    quote_cred_width = credit_width(img, quote_name, quote_screen_name, footer_font_file=footer_font_file, min_font_size=min_font_size)
    return max(image_cred_width, quote_cred_width)

def check_quote_width(img, name, screen_name, full_text,
                      quote_font_file='Apple Chancery.ttf',
                      min_font_size=14):
    # Check quote width
    boundary = get_boundary(img)
    location, color = select_region_and_color(img)
    box_corners = get_box_corners(img, location=location)

    all_lines, font_size, spacing, max_char_height = fit_text_to_box(box_corners, full_text, quote_font_file=quote_font_file, equal_spacing=True)
    return font_size >= min_font_size

def check_footer_width(img, name, screen_name, footer_font_file='AppleGothic.ttf'):
    boundary = get_boundary(img)
    sig_width = signature_width(img, footer_font_file=footer_font_file)
    cred_width = credit_width(img, name, screen_name, footer_font_file=footer_font_file)
    return sig_width + cred_width <= img.width - 2 * boundary
