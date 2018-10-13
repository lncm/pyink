# For python3 semantics
from __future__ import print_function #, division
import epd2in7b
import math
import qrcode
from sys import exit
from PIL import Image, ImageDraw, ImageFont

above = (0,0)
below = (10,244)


qr_test_data = 'LIGHTNING:LNBC1200U1PDHLMCMPP5NVEVN04R0YWXAR7SD2W8VDMNHEP5XW6FDMUW5PLHQRJ6QG9Z8G0QDQJWD6X2CTTYPPXZUNJ0YCQZYS2LNPHNGTG3L2PPJKSZNFNMMHNGSUPU9DKDM0W7KGD0VGN8WHJTFNGCD9Z2NSAKY25YCHNRRXWS9YNE557Z4280PA4EYK8JWTM2NZ3QSPSV6A0Z'

# For python3 and 2 interoperability
try:
    str
except NameError:
    str = basestring


print('Initializing driver')
epd = epd2in7b.EPD()
epd.init()

def main():
    exit('This file is not meant to be run directly.')


def qr(data=qr_test_data):
    """
    Generate QRcode image

    data:    String to encode as QR
    :return: Image object
    """

    uppercase = str.upper(data)

    qrc = qrcode.QRCode(
        version=7,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qrc.add_data(uppercase)
    qrc.make(fit=False)

    img = qrc.make_image(fill_color="black", back_color="white")
    return img


def expand(image, size):
    """
    Expand black and white image to given size and fill with white

    image:      Pillow image instance
    size:       2-tuple (width, height)
    """
    original_format = image.format
    foreground = image.copy()
    foreground.thumbnail((size[0], size[1]), Image.LANCZOS)
    background = Image.new('1', (size[0], size[1]), 255)
    foreground_position = (
        int(math.ceil((size[0] - foreground.size[0]) / 2)),
        int(math.ceil((size[1] - foreground.size[1]) / 2))
    )
    background.paste(foreground, foreground_position)
    background.format = original_format
    return background


def text(img, string, position):
    img = img.convert('RGBA')
    txt = Image.new('RGBA', img.size, (255,255,255,0))
    fnt = ImageFont.truetype('fonts/DejaVuSans.ttf', 20)
    d = ImageDraw.Draw(txt)
    d.text(position, string, font=fnt, fill=(0,0,0,255))

    out = Image.alpha_composite(img, txt)
    return out.convert('1')


def logo(black='png/logo-vertical_black.png', red='png/logo-vertical_red.png'):
    print('Rendering logo')
    black = Image.open(black)
    red = Image.open(red)

    img(black, red)


def img(black, red=None):
    """
    Draw one or two layers to display

    Pass one or two correctly sized black & white images.
    A black and a red layer can be drawn. The images must be 176x264.
    A white background is recommended.

    black:      Pillow image instance
    red:        Pillow image instance
    """
    print('Rendering in progress...')

    # clear frame buffer
    black_fb = [0] * int((epd.width * epd.height / 8))
    red_fb = [0] * int((epd.width * epd.height / 8))


    if red is None:
        # create empty red layer
        red = Image.new('1', (176, 264), 255)

        black_fb = epd.get_frame_buffer(black)
        red_fb = epd.get_frame_buffer(red)

        epd.display_frame(black_fb, red_fb)
    else:
        black_fb = epd.get_frame_buffer(black)
        red_fb = epd.get_frame_buffer(red)

        epd.display_frame(black_fb, red_fb)

    print('Rendering complete')




if __name__ == '__main__':
    main()
