import sys
import os
sys.path.append('../')

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import numpy as np

import motivate_me_bot as mmb

if __name__ == '__main__':
    img = mmb.get_image('../images/flowers.jpg')
    # img = mmb.get_image('../images/elizabeth_lab.jpg')
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

    mmb.draw_quote_in_box(img,
                          box_corners,
                          all_lines,
                          font_file,
                          font_size,
                          color=color,
                          spacing=spacing,
                          equal_spacing=True,
                          max_char_height=max_char_height,
                          draw_box=False)

    mmb.draw_signature(img,
                       color=color)

    # mmb.draw_credits(img, quote_tweeter='Mulia Khan', image_tweeter='NA', color=color)
    mmb.draw_credits(img,
                    quote_name='???',
                    quote_screen_name='@maggieisntcool',
                    image_name='Elizabeth Li',
                    image_screen_name='@ElizabethLi',
                     color=color)

    img.show()
