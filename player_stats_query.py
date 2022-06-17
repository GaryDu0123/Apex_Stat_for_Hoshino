#!/usr/bin/env python
# -*-coding:utf-8 -*-
import base64
import os
import re
from io import BytesIO

try:
    import ujson as json
except Exception:
    import json
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from .tool import paste_image, open_or_download, get_response
from hoshino.typing import CQEvent
from .api import API_KEY, IMAGE_MODE

rank = {
    "Unranked": "未排名",
    "Rookie": "菜鸟",
    "Bronze": "青铜",
    "Silver": "白银",
    "Gold": "黄金",
    "Platinum": "白金",
    "Diamond": "钻石",
    "Master": "大师",
    "Apex Predator": "Apex 猎杀者",
}

file_full_path = os.path.dirname(os.path.abspath(__file__))
default_icons = Image.open(f"{file_full_path}/images/icons/bloodhound.png")
default_bg = Image.open(f"{file_full_path}/images/banners/bloodhound.jpg")


async def display_as_image(bot, ev: CQEvent, content):
    # 图片位置
    global_data = content["global"]

    # 玩家选中角色的图片
    try:
        player_icon = (
            await open_or_download(
                f"{file_full_path}/images/icons/{content['legends']['selected']['LegendName'].lower()}.png",
                content['legends']['selected']["ImgAssets"]["icon"])).convert("RGBA")
        player_bg = (await open_or_download(
            f"{file_full_path}/images/banners/{content['legends']['selected']['LegendName'].lower()}.png",
            content['legends']['selected']["ImgAssets"]["banner"])).convert("RGBA")
    except:
        # 查询出错的时候使用默认的图标
        player_icon = default_icons
        player_bg = default_bg

    width = player_bg.size[0]  # 获取宽度
    height = player_bg.size[1]  # 获取高度

    player_bg = player_bg.resize((int(width * (680 / height)), int(height * (680 / height))))
    if player_bg.size[0] > 1400:
        player_bg = player_bg.crop((300, 0, 1300, 680))
    else:
        player_bg = player_bg.crop((0, 0, 1000, 680))
    player_bg = ImageEnhance.Brightness(player_bg).enhance(0.5)

    # 段位图标
    br_rank = f'{global_data["rank"]["rankName"]}{global_data["rank"]["rankDiv"]}'
    ar_rank = f'{global_data["arena"]["rankName"]}{global_data["arena"]["rankDiv"]}'
    br_rank_icon = (await open_or_download(f"{file_full_path}/images/ranks/{br_rank}.png",
                                           global_data["rank"]["rankImg"])).convert("RGBA").resize((120, 120))

    ar_rank_icon = (await open_or_download(f"{file_full_path}/images/ranks/{ar_rank}.png",
                                           global_data["arena"]["rankImg"])).convert("RGBA").resize((120, 120))

    # 等级图标
    level_icon = Image.open(f"{file_full_path}/images/level.png").convert("RGBA").resize((120, 120))

    # 背景层
    image = player_bg  # Image.new('RGBA', (1000, 680), (49, 52, 67, 255))

    # 文字层
    draw = ImageDraw.Draw(image)

    # 字体
    font_big = ImageFont.truetype(f"{file_full_path}/font/OPPOSans-M.ttf", 32)
    font = ImageFont.truetype(f"{file_full_path}/font/OPPOSans-M.ttf", 20)
    # font_small = ImageFont.truetype(f'{file_full_path}/font/OPPOSans-L.ttf', 12)
    font_roboto = ImageFont.truetype(f'{file_full_path}/font/Roboto-Bold-3.ttf', 24)
    font_mono = ImageFont.truetype(f'{file_full_path}/font/JetBrainsMono[wght].ttf', 18)

    # 玩家选中的角色图像
    paste_image(image, player_icon, -48, -100)

    # 玩家名字
    player_name = global_data["name"]
    text_width = font.getsize(player_name)
    draw.text((442 + int((1000 - 442) / 2) - (text_width[0]) / 2, 60), player_name, (255, 255, 255, 240), font_big)

    # 玩家等级
    player_level = str(global_data["level"])
    text_width = font.getsize(player_level)
    lv_a = level_icon.split()[3]
    image.paste(level_icon, (442 + int((1000 - 442) / 4) - int(level_icon.size[0] / 2), 150), mask=lv_a)
    draw.text((442 + int((1000 - 442) / 4) - int((text_width[0]) / 2) - 2, 190), player_level, (255, 255, 255, 240),
              font_roboto)

    # 信息
    draw.text((665, 170), f'Lv:    {player_level}({global_data["toNextLevelPercent"]}%)\n'
                          f'UID:   {global_data["uid"]}\n'
                          f'State: [{content["realtime"]["currentStateAsText"]}]'
              , (255, 255, 255, 240), font_mono)

    rank_icon_v_position = 400
    draw.text((442 + int((1000 - 442) / 4) - (font_big.getsize("大逃杀")[0]) / 2, rank_icon_v_position - 50),
              "大逃杀", (255, 255, 255, 240), font_big)
    draw.text((442 + 3 * int((1000 - 442) / 4) - (font_big.getsize("竞技场")[0]) / 2, rank_icon_v_position - 50),
              "竞技场", (255, 255, 255, 240), font_big)
    br_a = br_rank_icon.split()[3]
    ar_a = ar_rank_icon.split()[3]
    image.paste(br_rank_icon, (442 + int((1000 - 442) / 4) - int(br_rank_icon.size[0] / 2), rank_icon_v_position),
                mask=br_a)
    image.paste(ar_rank_icon, (442 + 3 * int((1000 - 442) / 4) - int(br_rank_icon.size[0] / 2), rank_icon_v_position),
                mask=ar_a)
    br_rank_text = f'{rank.get(global_data["rank"]["rankName"], "Unknown")}{global_data["rank"]["rankDiv"]}'
    ar_rank_text = f'{rank.get(global_data["arena"]["rankName"], "Unknown")}{global_data["arena"]["rankDiv"] if global_data["arena"]["rankName"] != "Unranked" else ""} '
    text_width = font.getsize(br_rank_text)
    draw.text((442 + int((1000 - 442) / 4) - (text_width[0]) / 2, rank_icon_v_position + 120),
              br_rank_text, (255, 255, 255, 240), font)
    text_width = font.getsize(ar_rank_text)
    draw.text((442 + 3 * int((1000 - 442) / 4) - (text_width[0]) / 2, rank_icon_v_position + 120),
              ar_rank_text, (255, 255, 255, 240), font)
    buf = BytesIO()
    image.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    await bot.send(ev, f'''[CQ:image,file={base64_str}]''')


async def get_player_stats(bot, ev: CQEvent, args):
    if len(args) != 1:
        await bot.send(ev, "请输入正确数量的参数 [平台(PC/PS4/X1) Origin用户名]")
        return
    commands = re.match("(?P<platform>(PC|PS4|X1))? *(?P<player>.+)", args[0], flags=re.I).groupdict()

    # if platform.group("platform") not in ["PC", "PS4", "X1"]:
    #     await bot.send(ev, "未知平台(PC/PS4/X1)")
    #     return
    params = {
        "auth": API_KEY,
        "player": commands['player'],
        "platform": "PC" if commands['platform'] is None else commands['platform'].upper()
    }
    content = await get_response(f"https://api.mozambiquehe.re/bridge", True, params)
    if "Error" in content:
        await bot.send(ev, f"请求失败, 未找到用户{commands['player']}~ 请确认平台以及用户名~")
        return
    if not IMAGE_MODE:
        global_data = content["global"]
        reply = f"""
    {global_data["name"]} 的数据 
    状态: [{content["realtime"]["currentStateAsText"]}]
    等级: {global_data["level"]} ({global_data["toNextLevelPercent"]}%)
    ====排位====
    大逃杀: {rank.get(global_data["rank"]["rankName"], "未知")}{global_data["rank"]["rankDiv"]} | {global_data["rank"]["rankScore"]} RP
    竞技场: {rank.get(global_data["arena"]["rankName"], "未知")}{global_data["arena"]["rankDiv"]} | {global_data["arena"]["rankScore"]} AP
    """.strip()
        await bot.send(ev, reply)
    else:
        await display_as_image(bot, ev, content)
