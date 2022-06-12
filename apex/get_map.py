#!/usr/bin/env python
# -*-coding:utf-8 -*-
from .tool import get_response, recalculate_timezone
from hoshino.typing import CQEvent
from .api import API_KEY
from .map_names import map_name_dict


# todo https://cdn.apexstats.dev/Bot/Legends/Banners/
# todo https://api.mozambiquehe.re/maprotation
# todo https://apexlegendsapi.com/#query-parameters-5

async def get_map(bot, ev: CQEvent, args):
    rep_json = await get_response(f"https://api.mozambiquehe.re/maprotation?auth={API_KEY}&version=2", True)
    arenas_map_en = rep_json["arenas"]["current"]["map"].lower()  # 竞技场的名字英文
    arenas_map_zh = map_name_dict["arena"][arenas_map_en]  # 竞技场的名字中文
    arenas_remaining = rep_json["arenas"]["current"]["remainingMins"]  # 大逃杀剩余时间

    br_map_en = rep_json["battle_royale"]["current"]["map"].lower()  # 大逃杀的名字英文
    br_map_zh = map_name_dict["br"][br_map_en]  # 大逃杀的名字中文
    br_remaining = rep_json["battle_royale"]["current"]["remainingMins"]  # 大逃杀剩余时间

    content = f"""
当前地图
> 大逃杀: {br_map_zh}
\u23F0剩余时间: {int(br_remaining)}分钟
> 竞技场: {arenas_map_zh}
\u23F0剩余时间: {int(arenas_remaining)}分钟
""".strip()
    await bot.send(ev, content)


async def get_future_map(bot, ev: CQEvent, args):
    rep_json = await get_response(f"https://api.mozambiquehe.re/maprotation?auth={API_KEY}&version=2", True)
    arenas_map_en = rep_json["arenas"]["next"]["map"].lower()  # 竞技场的名字英文
    arenas_map_zh = map_name_dict["arena"][arenas_map_en]  # 竞技场的名字中文
    arenas_start_time = recalculate_timezone(rep_json["arenas"]["next"]["readableDate_start"])

    br_map_en = rep_json["battle_royale"]["next"]["map"].lower()  # 大逃杀的名字英文
    br_map_zh = map_name_dict["br"][br_map_en]  # 大逃杀的名字中文
    br_start_time = recalculate_timezone(rep_json["battle_royale"]["next"]["readableDate_start"])

    content = f"""
地图轮换| 下一张地图是
> 大逃杀: {br_map_zh}
开始时间: {br_start_time}
> 竞技场: {arenas_map_zh}
开始时间: {arenas_start_time}
""".strip()
    await bot.send(ev, content)
