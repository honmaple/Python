#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: himawari8.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-22 22:22:27 (CST)
# Last Update:星期三 2017-3-22 22:22:38 (CST)
#          By:
# Description:
# **************************************************************************
from PIL import Image
from io import BytesIO
from urllib.request import Request, urlopen
from datetime import datetime, timedelta
import json

SCALE = 4
WIDTH = 1368
HEIGHT = 738


def get_info():
    url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json"
    request = Request(url)
    response = urlopen(request, timeout=10)
    return json.loads(response.read())


def download():
    png = Image.new('RGB', (550 * SCALE, 550 * SCALE))
    desktop = Image.new('RGB', (WIDTH, HEIGHT))
    # desktop = Image.open('/home/jianglin/Pictures/308556.jpg')
    url_format = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/{}d/{}/{}_{}_{}.png'
    info = get_info()
    date = datetime.strptime(info['date'], '%Y-%m-%d %H:%M:%S') + timedelta(
        hours=-4)
    for x in range(SCALE):
        for y in range(SCALE):
            url = url_format.format(SCALE, 550,
                                    date.strftime("%Y/%m/%d/%H%M%S"), x, y)
            print(url)
            request = Request(url)
            response = urlopen(request, timeout=10)
            img = Image.open(BytesIO(response.read()))
            png.paste(img, (550 * x, 550 * y, 550 * (x + 1), 550 * (y + 1)))
    png.thumbnail((HEIGHT, HEIGHT), Image.ANTIALIAS)
    desktop.paste(png, ((WIDTH - HEIGHT) // 2, 0))
    desktop.save('/tmp/earth.png', "PNG")


if __name__ == '__main__':
    download()
