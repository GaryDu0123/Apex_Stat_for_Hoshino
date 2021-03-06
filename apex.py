#!/usr/bin/env python
# -*-coding:utf-8 -*-
import re
from typing import Dict, Callable
from hoshino import Service
from hoshino.typing import CQEvent
from .get_map import get_map, get_future_map
from .get_map_no_api import get_map_unsafe, get_future_map_unsafe
from .crafting import get_crafting_items
from .predator import get_predator_score_line
from .player_stats_query import get_player_stats
from .api import API_KEY

if not API_KEY:
    sv = Service('Apex_Stat', help_='''
apex 查询当前地图 # 查询当前为哪张地图
apex 查询轮换地图 [1-5] # 查询未来1-5小时的地图以及轮换时间
'''.strip())

    trigger_keyword: Dict[str, Callable] = {
        "查询当前地图": get_map_unsafe,
        "查询轮换地图": get_future_map_unsafe,
    }
else:
    sv = Service('apex_stats', help_='''
apex 查询当前地图 # 查询当前为哪张地图
apex 查询下张地图 # 查询下张地图
apex 查询轮换地图 [1-5] # 查询未来1-5小时的地图以及轮换时间
apex 查询制造器 # 查询今日复制器可制造物品
apex 查询猎杀分数线 # 查询成为猎杀的最低分数
apex 查询用户数据 [平台(PC/PS4/X1)] origin用户名 # 查询用户数据
'''.strip())

    trigger_keyword: Dict[str, Callable] = {
        "查询当前地图": get_map,
        "查询轮换地图": get_future_map_unsafe,
        "查询下张地图": get_future_map,
        "查询制造器": get_crafting_items,
        "查询猎杀分数线": get_predator_score_line,
        "查询用户数据": get_player_stats
    }


@sv.on_prefix('apex', only_to_me=True)
async def process_command(bot, ev: CQEvent):
    if not str(ev.message).strip():
        await bot.send(ev, "请输入命令")
        return
    message = str(ev.message).strip()
    command = re.findall(r"(?P<command>\w+) *(?P<args>.*)", message)[0]
    if command[0] in trigger_keyword:
        try:
            await trigger_keyword[command[0]](bot, ev, [command[1]])
        except Exception as e:
            sv.logger.error(f"{e} occur when processing command {message} in apex")