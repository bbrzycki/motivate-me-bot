import sys
import os
sys.path.append('../')

import numpy as np

import motivate_me_bot as mmb

if __name__ == '__main__':
    download_dir = 'images/'
    new_dir = 'new_images/'

    quote_keyword = '#motivation'
    image_keyword = '#sunset'

    api = mmb.setup_api()

    quote_name, quote_screen_name, quote = mmb.find_quote(api, quote_keyword)
    image_name, image_screen_name, image_filename = mmb.find_image(api,
                                                                   image_keyword,
                                                                   output_dir=download_dir,
                                                                   min_dimensions = (1440, 1080))

    img = mmb.get_image(image_filename)

    location, color = mmb.select_region_and_color(img)
    box_corners = mmb.get_box_corners(img, location=location)
    font_file = 'Apple Chancery.ttf'

    all_lines, font_size, spacing, max_char_height = mmb.fit_text_to_box(box_corners,
                                                                     quote,
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

    mmb.draw_signature(img)

    mmb.draw_credits(img,
                     quote_name,
                     quote_screen_name,
                     image_name,
                     image_screen_name)

    img.show()
