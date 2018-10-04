from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

import numpy as np

import sys
import os

from image_analysis import average_color, contrast_color

def get_image(image_path):
    return Image.open(image_path)

def get_box_dims(img):
    img_width, img_height = img.size

    boundary = int(img_height / 15)
    box_x = boundary
    box_y = boundary
    # box_y = int(img_height / 4)
    box_width = int(img_width - 2 * box_x)
    box_height = int(img_height / 2 - 2 * box_y)
    # box_height = int(img_height / 2)

    return (box_x, box_y, box_width, box_height)

def fit_text_to_box(box_dims,
                    text,
                    font_file='Apple Chancery.ttf',
                    equal_spacing=True,
                    spacing_limit=2):
    box_x, box_y, box_width, box_height = box_dims

    font_size = 0
    spacing = 1

    text_block_height = 0
    max_char_height = 0

    while True:
        # Increase font size and check if it fits
        proposed_font_size = font_size + 1
        proposed_max_char_height = 0
        fits_horizontally = True
        fits_vertically = True

        font = ImageFont.truetype(font_file, proposed_font_size)

        words = text.split()
        all_lines_temp = []
        current_line = []
        for word in words:
            proposed_line = current_line + [word]
            proposed_text_width, proposed_text_height = font.getsize(' '.join(proposed_line))                # Check line width fits within box width
            if proposed_text_height > proposed_max_char_height:
                proposed_max_char_height = proposed_text_height

            if proposed_text_width <= box_width:
                current_line = proposed_line
            else:
                word_width, word_height = font.getsize(word)
                if word_width > box_width:
                    fits_horizontally = False
                    break
                else:
                    all_lines_temp.append(' '.join(current_line))
                    current_line = [word]
        # Add last valid line
        all_lines_temp.append(' '.join(current_line))

        # Check text fits within box height
    #             proposed_max_char_height = 0
    #             for i, line in enumerate(all_lines_temp):
    #                 line_width, line_height = font.getsize(line)
    #                 if line_height > proposed_max_char_height:
    #                     proposed_max_char_height = line_height
        if equal_spacing:
            proposed_text_block_height = proposed_max_char_height * (len(all_lines_temp) + 1) * spacing * 1.2
        else:
            proposed_text_block_height = proposed_max_char_height * ((len(all_lines_temp) - 1) * spacing * 1.2 + 1)
        if proposed_text_block_height > box_height:
            fits_vertically = False

        if fits_horizontally and fits_vertically:
            font_size = proposed_font_size
            all_lines = all_lines_temp
            max_char_height = proposed_max_char_height
            text_block_height = proposed_text_block_height
        else:
            break

    # We know the text fits with spacing = 1
    # Maximized separation from top to bottom, with a limit of double spacing

    proposed_spacing = spacing
    while True:
        proposed_spacing = spacing + 0.01
        if proposed_spacing > spacing_limit:
            break
        if equal_spacing:
            proposed_text_block_height = max_char_height * (len(all_lines) + 1) * proposed_spacing * 1.2
        else:
            proposed_text_block_height = max_char_height * ((len(all_lines) - 1) * proposed_spacing * 1.2 + 1)

        if proposed_text_block_height <= box_height:
            spacing = proposed_spacing
            text_block_height = proposed_text_block_height
        else:
            break

    return all_lines, font_size, spacing, max_char_height

def draw_quote_in_box(img,
                      box_dims,
                      all_lines=['Hello, world!'],
                      font_file='Apple Chancery.ttf',
                      font_size=12,
                      color=(255,255,255),
                      use_average_color=False,
                      spacing=1,
                      equal_spacing=True,
                      max_char_height=None,
                      draw_box=True):
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    boundary = int(img_height / 15)
    sig_size = int(boundary / 2)
    blur_boundary = int(boundary / 8)

    box_x, box_y, box_width, box_height = box_dims

    font = ImageFont.truetype(font_file, font_size)

    if max_char_height is None:
        # Compute max_char_height
        pass

    if equal_spacing:
        text_block_height = max_char_height * (len(all_lines) + 1) * spacing * 1.2
    else:
        text_block_height = max_char_height * ((len(all_lines) - 1) * spacing * 1.2 + 1)

    box_x, box_y, box_width, box_height = box_dims
    background_box = (box_x - blur_boundary, box_y - blur_boundary,
                      box_x + blur_boundary + box_width, box_y + blur_boundary + box_height)

    region = img.crop(background_box)
    region = region.filter( ImageFilter.GaussianBlur(radius=blur_boundary / 2))
    img.paste(region, background_box)

    if use_average_color:
        color = average_color(img, background_box, inverse=True)
        color = contrast_color(img, background_box)
        print(color)

    # text = "Sample Text Sample Text Sample Text Sample Text Sample Text Sample Text Sample Text Sample Text "
    for i, line in enumerate(all_lines):
        line_width, line_height = font.getsize(line)
        x_coord = box_x + box_width / 2 - line_width / 2
        if equal_spacing:
            y_coord = box_y + box_height / 2 - text_block_height / 2 + max_char_height * ((i + 1) * spacing * 1.2 - 0.5)
        else:
            y_coord = box_y + box_height / 2 - text_block_height / 2 + max_char_height * i * spacing * 1.2
        draw.text((x_coord, y_coord),
                   line,
                   color,
                   font=font)

    if draw_box:
        line_width = int(boundary / 15)
        if line_width % 2 == 0:
            line_width += 1
        draw.line((box_x, box_y - line_width / 2 + 1, box_x, box_y + box_height + line_width / 2 - 1), width=line_width)
        draw.line((box_x, box_y, box_x + box_width, box_y), width=line_width)
        draw.line((box_x + box_width, box_y + box_height, box_x, box_y + box_height), width=line_width)
        draw.line((box_x + box_width, box_y + box_height + line_width / 2 - 1, box_x + box_width, box_y - line_width / 2 + 1), width=line_width)

def draw_signature(img,
                   user='@MotivateMeBot',
                   font_file='AppleGothic.ttf',
                   color=(255,255,255),
                   use_average_color=False):
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    boundary = int(img_height / 15)
    sig_size = int(boundary / 2)
    blur_boundary = int(boundary / 8)

    # MotivateMeBot sig
    sig = user
    sig_font_file = font_file
    sig_font = ImageFont.truetype(sig_font_file, sig_size)
    sig_width, sig_height = sig_font.getsize(sig)

    background_box = (img_width - blur_boundary - sig_width - sig_size, img_height - blur_boundary - sig_height - sig_size,
                      img_width + blur_boundary - sig_size, img_height + blur_boundary - sig_size)



    region = img.crop(background_box)
    region = region.filter( ImageFilter.GaussianBlur(radius=2*blur_boundary))
    img.paste(region, background_box)

    if use_average_color:
        color = average_color(img, background_box, inverse=True)
        color = contrast_color(img, background_box)
        print(color)

    draw.text((img_width - sig_width - sig_size, img_height - sig_height - sig_size),
               sig,
               color,
               font=sig_font)

def draw_credits(img,
                 quote_tweeter,
                 image_tweeter,
                 font_file='AppleGothic.ttf',
                 color=(255,255,255),
                 use_average_color=False):
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    boundary = int(img_height / 15)
    sig_size = int(boundary / 2)
    cred_size = int(boundary / 4)
    blur_boundary = int(boundary / 8)

    # Image Credit
    image_cred = 'Image Credit: %s' % image_tweeter
    image_cred_font_file = font_file
    image_cred_font = ImageFont.truetype(image_cred_font_file, cred_size)
    image_cred_width, image_cred_height = image_cred_font.getsize(image_cred)

    # Quote Credit
    quote_cred = 'Quote Credit: %s' % quote_tweeter
    quote_cred_font_file = font_file
    quote_cred_font = ImageFont.truetype(quote_cred_font_file, cred_size)
    quote_cred_width, quote_cred_height = quote_cred_font.getsize(quote_cred)

    background_box = (sig_size - blur_boundary, img_height - blur_boundary - image_cred_height - quote_cred_height - sig_size,
                         sig_size + blur_boundary + max(image_cred_width, quote_cred_width), img_height + blur_boundary - sig_size)


    region = img.crop(background_box)
    region = region.filter( ImageFilter.GaussianBlur(radius=2*blur_boundary))
    img.paste(region, background_box)

    if use_average_color:
        color = average_color(img, background_box, inverse=True)
        color = contrast_color(img, background_box)
        print(color)

    draw.text((sig_size, img_height - image_cred_height - sig_size),
                image_cred,
                color,
                font=image_cred_font)

    draw.text((sig_size, img_height - image_cred_height * 1.2 - quote_cred_height - sig_size),
               quote_cred,
               color,
               font=quote_cred_font)
