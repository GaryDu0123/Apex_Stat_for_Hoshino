#!/usr/bin/env python
# -*-coding:utf-8 -*-
import base64
from io import BytesIO

try:
    import ujson as json
except Exception:
    import json
import os
import math
from collections import defaultdict
from PIL import Image, ImageFont, ImageDraw
from .tool import circle_corner, download_img, draw_text_at_center, draw_image_at_center
from hoshino.typing import CQEvent
from .tool import get_response, paste_image
from .crafting_names import crafting_dict, rarity_dict
from .api import API_KEY, IMAGE_MODE

file_full_path = os.path.dirname(os.path.abspath(__file__))
crafting_materials_icon = Image.open(f"{file_full_path}/images/crafting_materials.png").resize((16, 18))
icon_size = 64



def _image_display_content_converter(content):
    """
    将原本文本转为图形化函数所需的格式
    {
    "count": 3,
    "content": {
        "每日轮换": [
            {
                "name": "重型能量弹匣",
                "cost": 30,
                "name_en": "extended_energy_mag",
                "download_link": "",
                "rarity": "Common"
            }, {
                "name": "动能装填器",
                "cost": 30,
                "name_en": "extended_energy_mag",
                "download_link": "",
                "rarity": "Common"
            }
        ],
        "每周轮换": [
            {
                "name": "重型能量弹匣",
                "cost": 30,
                "name_en": "extended_energy_mag",
                "download_link": "",
                "rarity": "Common"
            }, {
                "name": "动能装填器",
                "cost": 30,
                "name_en": "extended_energy_mag",
                "download_link": "",
                "rarity": "Common"
            }
        ],
        "常驻": [
            {
                "name": "重型能量弹匣",
                "name_en": "extended_energy_mag",
                "download_link": "",
                "cost": 30,
                "rarity": "Common"
            }, {
                "name": "动能装填器",
                "name_en": "extended_energy_mag",
                "download_link": "",
                "cost": 30,
                "rarity": "Common"
            }
        ]
    }
}
    """
    process_dict = {"content": defaultdict(list)}
    for bundle in content:
        # 单独处理子弹
        if bundle['bundle'] == 'ammo':
            process_dict["content"]["常驻"].append({
                "name": "子弹",
                "name_en": "ammo",
                "rarity": "Common",
                "download_link": "https://legion.apexlegendsstatus.com/cache/0f8ac57cbf0db1163f77fcef09f9fb2c.png",
                "cost": 10
            })
            continue
        for items in bundle["bundleContent"]:
            item_name_ch = items['itemType']['name']
            rarity = items['itemType']['rarity']
            if items['itemType']['name'] in crafting_dict:
                item_name_ch = crafting_dict[items['itemType']['name']]
            asset_link = items['itemType']["asset"]
            if bundle['bundleType'] == "daily":
                process_dict["content"]["每日轮换"].append({
                    "name": item_name_ch,
                    "name_en": items['itemType']['name'],
                    "download_link": asset_link,
                    "cost": items["cost"],
                    "rarity": rarity
                })
            elif bundle['bundleType'] == "weekly":
                process_dict["content"]["每周轮换"].append({
                    "name": item_name_ch,
                    "name_en": items['itemType']['name'],
                    "download_link": asset_link,
                    "cost": items["cost"],
                    "rarity": rarity
                })
            elif bundle['bundleType'] == "permanent":
                process_dict["content"]["常驻"].append({
                    "name": item_name_ch,
                    "name_en": items['itemType']['name'],
                    "download_link": asset_link,
                    "cost": items["cost"],
                    "rarity": rarity
                })
    process_dict["count"] = math.ceil(len(process_dict["content"]["常驻"]) / 2) + \
                            math.ceil(len(process_dict["content"]["每周轮换"]) / 2) + \
                            math.ceil(len(process_dict["content"]["每日轮换"]) / 2)
    return process_dict


async def display_as_image(content):
    # 背景
    create_data = _image_display_content_converter(content)
    height = create_data["count"] * 108 + 48 * 3
    width = icon_size * 2 + 100
    image = Image.new('RGBA', (width, height), (49, 52, 67, 255))

    font = ImageFont.truetype(f"{file_full_path}/font/OPPOSans-M.ttf", 20)
    font_small = ImageFont.truetype(f'{file_full_path}/font/OPPOSans-L.ttf', 12)
    draw = ImageDraw.Draw(image)
    vertical_counter = 0
    for name, bundle in create_data['content'].items():
        draw_text_at_center(draw, name, vertical_counter + 8, 0, width, font)
        vertical_counter += 40
        for i in range(0, len(bundle), 2):
            item_img_left = None
            item_img_right = None
            # 检查图片是否在本地存在, 如果本地存在直接使用, 不存在则下载
            if os.path.exists(f"{file_full_path}/images/{bundle[i]['name_en']}_{bundle[i]['rarity']}.png"):
                item_img_left = Image.open(f"{file_full_path}/images/{bundle[i]['name_en']}_{bundle[i]['rarity']}.png").resize(
                    (icon_size, icon_size))
            else:
                item_img_left = await download_img(bundle[i]['download_link'])
                item_img_left = circle_corner(item_img_left.resize((icon_size, icon_size)), 10)
                item_img_left.save(f"{file_full_path}/images/{bundle[i]['name_en']}_{bundle[i]['rarity']}.png")

            if i + 1 < len(bundle):  # 判断右边的物品, 写的挺傻的, 但就先这样了
                if os.path.exists(f"{file_full_path}/images/{bundle[i + 1]['name_en']}_{bundle[i]['rarity']}.png"):
                    item_img_right = Image.open(f"{file_full_path}/images/{bundle[i + 1]['name_en']}_{bundle[i]['rarity']}.png").resize(
                        (icon_size, icon_size))
                else:
                    item_img_right = await download_img(bundle[i + 1]['download_link'])
                    item_img_right = circle_corner(item_img_right.resize((icon_size, icon_size)), 10)
                    item_img_right.save(f"{file_full_path}/images/{bundle[i + 1]['name_en']}_{bundle[i]['rarity']}.png")

            draw_image_at_center(image, item_img_left, vertical_counter, 0, width / 2)
            if item_img_right is not None and i + 1 < len(bundle):
                draw_image_at_center(image, item_img_right, vertical_counter, int(width / 2), width / 2)
            vertical_counter += 64
            draw_text_at_center(draw, bundle[i]["name"], vertical_counter + 4, 0, width / 2, font_small)
            if i + 1 < len(bundle):
                draw_text_at_center(draw, bundle[i + 1]["name"], vertical_counter + 4, int(width / 2), width / 2,
                                    font_small)

            vertical_counter += 20
            paste_image(image, crafting_materials_icon, vertical_counter, 36)
            draw.text((20 + 36, vertical_counter + 1), str(bundle[i]["cost"]), (255, 255, 255, 240), font_small)
            if i + 1 < len(bundle):
                paste_image(image, crafting_materials_icon, vertical_counter, int(width / 2) + 36)
                draw.text((int(width / 2) + 20 + 36, vertical_counter + 1), str(bundle[i + 1]["cost"]),
                          (255, 255, 255, 240), font_small)
            vertical_counter += 24
    buf = BytesIO()
    image.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'''[CQ:image,file={base64_str}]'''
    return msg


def display_as_text(content):
    daily_bundle = []
    weekly_bundle = []
    permanent_bundle = []
    ignore_bundle = ['ammo']

    for bundle in content:
        if bundle["bundle"] in ignore_bundle:
            continue
        for items in bundle["bundleContent"]:
            item_name_ch = items['itemType']['name']
            if items['itemType']['name'] in crafting_dict:
                item_name_ch = crafting_dict[items['itemType']['name']]
            rarity_ch = rarity_dict[items['itemType']['rarity']]
            if bundle['bundleType'] == "daily":
                daily_bundle.append([item_name_ch, rarity_ch, items['cost']])
            elif bundle['bundleType'] == "weekly":
                weekly_bundle.append([item_name_ch, rarity_ch, items['cost']])
            elif bundle['bundleType'] == "permanent":
                permanent_bundle.append([item_name_ch, rarity_ch, items['cost']])
    reply = """今日复制器可制造物品为
====每日轮换====
{}
====每周轮换====
{}
====常驻====
{}    
    """.format(
        "\n".join([f"{data[1]} {data[0]} C: {data[2]}" for data in daily_bundle]),
        "\n".join([f"{data[1]} {data[0]} C: {data[2]}" for data in weekly_bundle]),
        "\n".join([f"{data[1]} {data[0]} C: {data[2]}" for data in permanent_bundle])
    )
    return reply


async def get_crafting_items(bot, ev: CQEvent, args):
    content = await get_response(f"https://api.mozambiquehe.re/crafting?auth={API_KEY}", True)
    if IMAGE_MODE:
        await bot.send(ev, await display_as_image(content))
    else:
        await bot.send(ev, display_as_text(content))
