import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

from context import motivatemebot as mmb

if __name__ == '__main__':
    # img = mmb.get_image('../images/flowers.jpg')
    img = mmb.get_image('../images/elizabeth_lab.jpg')
    # img = mmb.get_image('../images/chris.jpg')
    # img = mmb.get_image('../images/github_page.jpg')
    
    img_width, img_height = img.size

    boundary = int(img_height / 15)
    box_x = boundary
    box_y = boundary
    # box_y = int(img_height / 4)
    box_width = int(img_width - 2 * box_x)
    box_height = int(img_height / 2 - 2 * box_y)
    background_box = (box_x, box_y, box_x + box_width, box_y + box_height)

    cropped_img = img.crop(background_box)

    luminances = []
    print(len(cropped_img.getdata()))
    for (r,g,b) in cropped_img.getdata():
        perceived_luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        luminances.append(perceived_luminance)

    plt.title('Top')
    plt.hist(luminances)
    plt.show()

    light = 0
    dark = 0
    for luminance in luminances:
        if luminance < 64:
            dark += 1
        if luminance > 255 - 64:
            light += 1

    print(light, dark)
    ratio = light / dark
    if ratio >= 1 or dark == 0:
        print(ratio)
        print('choose black')
    else:
        print(1 / ratio)
        print('choose white')

    #####

    boundary = int(img_height / 15)

    box_width = int(img_width - 2 * boundary)
    box_height = int(img_height / 2 - 2 * boundary)

    box_x = boundary
    # box_y = boundary
    box_y = int(img_height / 4 + boundary)

    background_box = (box_x, box_y, box_x + box_width, box_y + box_height)

    cropped_img = img.crop(background_box)

    luminances = []
    print(len(cropped_img.getdata()))
    for (r,g,b) in cropped_img.getdata():
        perceived_luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        luminances.append(perceived_luminance)

    plt.title('Middle')
    plt.hist(luminances)
    plt.show()

    light = 0
    dark = 0
    for luminance in luminances:
        if luminance < 64:
            dark += 1
        if luminance > 255 - 64:
            light += 1

    print(light, dark)
    ratio = light / dark
    if ratio >= 1 or dark == 0:
        print(ratio)
        print('choose black')
    else:
        print(1 / ratio)
        print('choose white')
