import sys
import os
sys.path.append('../')

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import numpy as np

import motivate_me_bot as mmb

def average_color(img, box_dims, inverse=True):

    r_tot = 0
    g_tot = 0
    b_tot = 0
    cropped_img = img.crop(box_dims)
    rgb_data = cropped_img.getdata()
    for (r,g,b) in rgb_data:
        r_tot += r
        g_tot += g
        b_tot += b
    pixel_num = len(rgb_data)
    averages = (int(np.round(r_tot / pixel_num)),
            int(np.round(g_tot / pixel_num)),
            int(np.round(b_tot / pixel_num)))
    if inverse:
        return tuple([(255-x) for x in averages])
    else:
        return averages

if __name__ == '__main__':
    # img = mmb.get_image('../images/flowers.jpg')
    # img = mmb.get_image('../images/elizabeth_lab.jpg')
    img = mmb.get_image('../images/chris.jpg')
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

    box_x, box_y, box_width, box_height = box_dims
    background_box = (box_x - blur_boundary, box_y - blur_boundary,
                      box_x + blur_boundary + box_width, box_y + blur_boundary + box_height)



    region = img.crop(background_box)
    region = region.filter( ImageFilter.GaussianBlur(radius=blur_boundary))
    img.paste(region, background_box)

    quote_color = average_color(img, background_box, inverse=True)
    print(quote_color)
    quote_color=(0,0,0)
    quote_color=(255,255,255)

    mmb.draw_quote_in_box(img,
                          box_dims,
                          all_lines,
                          font_file,
                          font_size,
                          color=quote_color,
                          spacing=spacing,
                          equal_spacing=True,
                          max_char_height=max_char_height,
                          draw_box=False)

    mmb.draw_signature(img, color=color)

    # mmb.draw_credits(img, quote_tweeter='Mulia Khan', image_tweeter='NA', color=color)
    mmb.draw_credits(img, quote_tweeter='@maggieisntcool', image_tweeter='@ChrissapherMorris')

    img.show()
