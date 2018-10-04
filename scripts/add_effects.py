import sys
import os
sys.path.append('../')

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import cv2

import motivate_me_bot as mmb

if __name__ == '__main__':
    img = mmb.get_image('../images/lanterns.jpg')
    img_cv = cv2.imread('../images/lanterns.jpg')

    img_blur = img.filter( ImageFilter.GaussianBlur(radius=2) )

    img_blur.show()
