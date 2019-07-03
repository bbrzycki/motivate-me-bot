import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from image_sizing import get_boundary, get_box_corners, get_image
from text_color import (average_color, average_contrast_color,
                        check_image_colors, get_all_luminances,
                        overall_contrast_color, select_region_and_color)
from text_formatting import fit_text_to_box


def quote_width(img,
                  all_lines=['Hello, world!'],
                  quote_font_file='Apple Chancery.ttf',
                  font_size=14,
                  min_font_size=14):
    font = ImageFont.truetype(quote_font_file, max(font_size, min_font_size))
    max_width = 0
    for line in all_lines:
        line_width = font.getsize(line)[0]
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
    sig_width = sig_font.getsize(sig)[0]
    return sig_width


def credit_width(img, name, screen_name, footer_font_file='AppleGothic.ttf', min_font_size=14):
    boundary = get_boundary(img)
    sig_size = max(int(boundary / 2), min_font_size * 2)
    cred_size = int(sig_size / 2)

    cred_font = ImageFont.truetype(footer_font_file, cred_size)

    # Image Credit
    image_cred = 'Image Credit: %s (@%s)' % (name, screen_name)
    image_cred_width = cred_font.getsize(image_cred)[0]

    # Quote Credit
    quote_cred = 'Quote Credit: %s (@%s)' % (name, screen_name)
    quote_cred_width = cred_font.getsize(quote_cred)[0]
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
    location = select_region_and_color(img)[0]
    box_corners = get_box_corners(img, location=location)

    font_size = fit_text_to_box(box_corners, full_text, quote_font_file=quote_font_file, equal_spacing=True)[1]
    return font_size >= min_font_size


def check_footer_width(img, name, screen_name, footer_font_file='AppleGothic.ttf'):
    boundary = get_boundary(img)
    sig_width = signature_width(img, footer_font_file=footer_font_file)
    cred_width = credit_width(img, name, screen_name, footer_font_file=footer_font_file)
    return sig_width + cred_width <= img.width - 2 * boundary
