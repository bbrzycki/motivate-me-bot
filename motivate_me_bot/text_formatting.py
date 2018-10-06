from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

import numpy as np

import sys
import os

def fit_text_to_box(box_corners,
                    text,
                    font_file='Apple Chancery.ttf',
                    equal_spacing=True,
                    spacing_limit=2):
    x1, y1, x2, y2 = box_corners
    box_width = x2 - x1
    box_height = y2 - y1

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
    # Maximized separation from top to bottom, up to a given spacing limit (default: 2)
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
