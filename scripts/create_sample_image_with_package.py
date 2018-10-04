import sys
import os
sys.path.append('../')

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import numpy as np

import motivate_me_bot as mmb

from motivate_me_bot.image_analysis import average_color, contrast_color

if __name__ == '__main__':
    # img = mmb.get_image('../images/flowers.jpg')
    img = mmb.get_image('../images/elizabeth_lab.jpg')
    # img = mmb.get_image('../images/chris.jpg')
    box_dims = mmb.get_box_dims(img)

    img_width, img_height = img.size
    boundary = int(img_height / 15)
    sig_size = int(boundary / 2)
    cred_size = int(boundary / 4)
    blur_boundary = int(boundary / 8)

    color=(255,255,255)

    text = 'i just saw a guy in the library cry for five or so minutes and then his phone alarm went off and he just? stopped crying? and went right on back to work'
    # text = 'A lantern can give you light only when you light it.'
    font_file = 'Apple Chancery.ttf'

    all_lines, font_size, spacing, max_char_height = mmb.fit_text_to_box(box_dims,
                                                                     text,
                                                                     font_file,
                                                                     equal_spacing=True)

    mmb.draw_quote_in_box(img,
                          box_dims,
                          all_lines,
                          font_file,
                          font_size,
                          color=color,
                          use_average_color=True,
                          spacing=spacing,
                          equal_spacing=True,
                          max_char_height=max_char_height,
                          draw_box=False)

    mmb.draw_signature(img,
                       color=color,
                       use_average_color=True)

    # mmb.draw_credits(img, quote_tweeter='Mulia Khan', image_tweeter='NA', color=color)
    mmb.draw_credits(img,
                     quote_tweeter='@maggieisntcool',
                     image_tweeter='@ElizabethLi',
                     color=color,
                     use_average_color=True)

    img.show()
