import sys
import os
import errno
sys.path.append('../')

import numpy as np

import motivate_me_bot as mmb

if __name__ == '__main__':
    download_dir = 'images/'
    new_dir = 'new_images/'

    quote_keyword = '#motivation'
    image_keyword = '#sunset'

    try:
        os.makedirs(download_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    api = mmb.setup_api()

    print('Finding image...')
    image_name, image_screen_name, image_filename = mmb.find_image(api,
                                                                   image_keyword,
                                                                   output_dir=download_dir,
                                                                   min_dimensions = (1440, 1080))

    img = mmb.get_image(image_filename)
    img_width, img_height = img.size
    boundary = mmb.get_boundary(img)

    print('Selecting text region and color...')
    location, color = mmb.select_region_and_color(img)
    box_corners = mmb.get_box_corners(img, location=location)
    font_file = 'Apple Chancery.ttf'

    print('Finding quote...')
    quote_name, quote_screen_name, quote = mmb.find_quote(api, img, quote_keyword)

    print('Fitting quote to image...')
    all_lines, font_size, spacing, max_char_height = mmb.fit_text_to_box(box_corners,
                                                                         quote,
                                                                         font_file,
                                                                         equal_spacing=True)

    print('Writing quote to image...')
    # Actually draw onto image
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

    print('Writing signature to image...')
    mmb.draw_signature(img)

    print('Writing credits to image...')
    mmb.draw_credits(img,
                     quote_name,
                     quote_screen_name,
                     image_name,
                     image_screen_name)

    print('Finished!')
    img.show()
