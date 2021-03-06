#!/usr/bin/env python
# -*-coding:utf-8 -*-
import json
import os

import aiohttp
from datetime import datetime, timedelta
import PIL
from PIL import Image, ImageDraw
from io import BytesIO


async def get_response(url, force_convert=False, params=None):
    async with aiohttp.request("GET", url, params=params) as rep:
        if not force_convert:
            return await rep.json()
        return json.loads(await rep.read())


def get_time(time_string):
    utc_format = "%Y-%m-%dT%H:%M:%S+0000"
    utc_time = datetime.strptime(time_string, utc_format)
    localtime = utc_time + timedelta(hours=8)
    return str(localtime)


def recalculate_timezone(time_string):
    utc_format = "%Y-%m-%d %H:%M:%S"
    utc_time = datetime.strptime(time_string, utc_format)
    localtime = utc_time + timedelta(hours=8)
    return str(localtime)


# https://zhuanlan.zhihu.com/p/147802147
def circle_corner(img, radii):
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img


async def download_img(url, params=None):
    async with aiohttp.request("GET", url, params=params) as rep:
        return PIL.Image.open(BytesIO(await rep.read()))


def paste_image(bg, icon, vertical_position, horizontal_position):
    r, g, b, a = icon.convert("RGBA").split()
    bg.paste(icon, (horizontal_position, vertical_position), mask=a)


def draw_text_at_center(d, text, vertical_position, horizontal_position, bg_width, font):
    text_width = font.getsize(text)
    # 计算字体位置
    d.text((horizontal_position + int((bg_width - text_width[0]) / 2), vertical_position),
           text, (255, 255, 255, 240), font)


def draw_image_at_center(bg, img, vertical_position, horizontal_position, bg_width):
    img = img.convert("RGBA")
    r, g, b, a = img.split()
    bg.paste(img, ((horizontal_position + int((bg_width - img.size[0]) / 2)), vertical_position), mask=a)


async def open_or_download(path, link):
    if os.path.exists(path):
        return Image.open(path)
    else:
        img = await download_img(link)
        img.save(path)
        return img
