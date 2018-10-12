import sys
import os
sys.path.append('../')

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import numpy as np

import motivate_me_bot as mmb

if __name__ == '__main__':
    # img = mmb.get_image('../images/flowers.jpg')
    img = mmb.get_image('../images/elizabeth_lab.jpg')
    # img = mmb.get_image('../images/chris.jpg')
    # img = mmb.get_image('../images/github_page.jpg')

    location, color = mmb.select_region_and_color(img)
    box_corners = mmb.get_box_corners(img, location=location)

    text = 'i just saw a guy in the library cry for five or so minutes and then his phone alarm went off and he just? stopped crying? and went right on back to work'
    # text = 'A lantern can give you light only when you light it.'
    font_file = 'Apple Chancery.ttf'

    all_lines, font_size, spacing, max_char_height = mmb.fit_text_to_box(box_corners,
                                                                     text,
                                                                     font_file,
                                                                     equal_spacing=True)

    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size
    boundary = mmb.get_boundary(img)
    blur_boundary = int(boundary / 8)

    x1, y1, x2, y2 = box_corners
    box_width = x2 - x1
    box_height = y2 - y1

    font = ImageFont.truetype(font_file, font_size)

    text_block_height = max_char_height * (len(all_lines) + 1) * spacing * 1.2

    background_box = (x1 - blur_boundary, y1 - blur_boundary,
                      x1 + blur_boundary + box_width, y1 + blur_boundary + box_height)

    mmb.blur_box(img, background_box, blur_boundary, n=int(box_height/16))

    for i, line in enumerate(all_lines):
        line_width, line_height = font.getsize(line)
        x_coord = x1 + box_width / 2 - line_width / 2
        y_coord = y1 + box_height / 2 - text_block_height / 2 + max_char_height * ((i + 1) * spacing * 1.2 - 0.5)
        draw.text((x_coord, y_coord),
                   line,
                   color,
                   font=font)

    img.show()
