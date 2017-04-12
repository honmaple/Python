#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: himawari8.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-22 22:22:27 (CST)
# Last Update:星期四 2017-3-23 12:25:2 (CST)
#          By:
# Description:
# **************************************************************************
from PIL import Image, ImageOps, ImageDraw
from io import BytesIO
from urllib.request import Request, urlopen
from datetime import datetime, timedelta
import json

SCALE = 2
WIDTH = 1368
HEIGHT = 768


def get_info():
    url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json"
    request = Request(url)
    response = urlopen(request, timeout=10)
    return json.loads(response.read())


def download():
    png = Image.new('RGB', (550 * SCALE, 550 * SCALE))
    # desktop = Image.new('RGB', (WIDTH, HEIGHT))
    desktop = Image.open('/home/jianglin/Pictures/308556.png')
    url_format = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/{}d/{}/{}_{}_{}.png'
    info = get_info()
    # date = datetime.strptime(info['date'], '%Y-%m-%d %H:%M:%S') + timedelta(
    #     hours=-6)
    date = datetime.strptime(info['date'], '%Y-%m-%d %H:%M:%S')
    for x in range(SCALE):
        for y in range(SCALE):
            url = url_format.format(SCALE, 550,
                                    date.strftime("%Y/%m/%d/%H%M%S"), x, y)
            print(url)
            request = Request(url)
            response = urlopen(request, timeout=10)
            img = Image.open(BytesIO(response.read()))
            png.paste(img, (550 * x, 550 * y, 550 * (x + 1), 550 * (y + 1)))
    png = circle(png)
    desktop.paste(png, (160, 160), png)
    desktop.save('/tmp/earth.png', "PNG")
    set_background()


def circle(img):
    width = SCALE * 550
    height = SCALE * 550
    size = (width, height)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((3, 3, width - 3, height - 3), fill=255)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.thumbnail((214, 214), Image.ANTIALIAS)
    return output


def convert():
    # size = (768, 768)
    # mask = Image.new('L', size, 0)
    # draw = ImageDraw.Draw(mask)
    # draw.ellipse((3, 3, 765, 765), fill=255)
    # im = Image.open('/tmp/earth.png')
    # output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    # output.putalpha(mask)
    # output.thumbnail((256, 256), Image.ANTIALIAS)
    # output.save('output.png')
    # output.convert("RGBA")
    output = Image.open('output.png')
    output.thumbnail((214, 214), Image.ANTIALIAS)
    desktop = Image.open('/home/jianglin/Pictures/308556.png')
    desktop.paste(output, (160, 160), output)
    desktop.save('/tmp/earch.png', "PNG")


def set_background():
    import os
    os.system('feh --bg-scale /tmp/earth.png')


if __name__ == '__main__':
    download()
