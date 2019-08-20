import sys

import numpy as np

from image_sizing import get_boundary, get_box_corners


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def average_color(img, background_box, inverse=True):

    r_tot = 0
    g_tot = 0
    b_tot = 0
    cropped_img = img.crop(background_box)
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


def average_contrast_color(img, background_box):
    r, g, b = average_color(img, background_box, inverse=False)
    perceived_luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if perceived_luminance > 0.5:
        return BLACK
    else:
        return WHITE


def get_all_luminances(img, background_box, range=64):
    if range > 256:
        sys.exit('Invalid range!')
    cropped_img = img.crop(background_box)
    luminances = []
    for (r, g, b) in cropped_img.convert('RGB').getdata():
        perceived_luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        luminances.append(perceived_luminance)
    light = 0
    dark = 0
    for luminance in luminances:
        if luminance < range:
            dark += 1
        if luminance > 255 - range:
            light += 1
    return light, dark


def overall_contrast_color(img, background_box, range=64):
    light, dark = get_all_luminances(img, background_box, range=range)
    if dark == 0 or light / dark >= 1:
        return BLACK
    else:
        return WHITE


def select_region_and_color(img, range=64):
    top_box = get_box_corners(img, location='top')
    middle_box = get_box_corners(img, location='middle')

    top_light, top_dark = get_all_luminances(img, top_box, range=range)
    middle_light, middle_dark = get_all_luminances(img, middle_box, range=range)

    shades = [('top_light', top_light),
              ('top_dark', top_dark),
              ('middle_light', middle_light),
              ('middle_dark', middle_dark)]
    shades.sort(key=(lambda x: x[1]))
    minimum_shade = shades[0][0]

    if minimum_shade == 'top_light':
        return 'top', WHITE
    elif minimum_shade == 'top_dark':
        return 'top', BLACK
    elif minimum_shade == 'middle_light':
        return 'middle', WHITE
    else:
        # minimum_shade == 'middle_dark'
        return 'middle', BLACK


def check_region_colors(img,
                        region,
                        color=None,
                        target_fraction=0.001,
                        verification_range=64):
    '''
    Filter out "bad" images.
    '''
    pixel_num = (region[2] - region[0]) * (region[3] - region[1])
    light, dark = get_all_luminances(img, region, range=verification_range)
    print('Total pixel num = %s' % pixel_num)
    print('(light, dark) = (%s, %s)' % (light, dark))
    print('Corresponding fractions: (%.6f, %.6f)' % (light / pixel_num, dark / pixel_num))
    if color is not None:
        if color == 'WHITE':
            print('Selected: WHITE')
            return light / pixel_num < target_fraction
        else:
            print('Selected: BLACK')
            return dark / pixel_num < target_fraction
    else:
        return (light / pixel_num < target_fraction
                or dark / pixel_num < target_fraction)


def check_image_colors(img):
    img_width, img_height = img.size
    boundary = get_boundary(img)

    print('Checking quote colors...')
    location, color = select_region_and_color(img, range=64)
    box = get_box_corners(img, location=location)
    if not check_region_colors(img,
                               box,
                               target_fraction=0.001,
                               verification_range=64):
        return False

    print('Checking lower left colors...')
    lower_left_box = (boundary // 4,
                      img_height - boundary // 4 - boundary,
                      boundary // 4 + img_width // 3,
                      img_height - boundary // 4)
    if not check_region_colors(img,
                               lower_left_box,
                               target_fraction=0.01,
                               verification_range=64):
        return False

    print('Checking lower right colors...')
    lower_right_box = (img_width * 2 // 3 - boundary // 4,
                       img_height - boundary // 4 - boundary,
                       img_width - boundary // 4,
                       img_height - boundary // 4)
    return check_region_colors(img,
                               lower_right_box,
                               target_fraction=0.01,
                               verification_range=64)
