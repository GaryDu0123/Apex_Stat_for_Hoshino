#!/usr/bin/env python
# -*-coding:utf-8 -*-
from .tool import get_response, get_time
from hoshino.typing import CQEvent
from .MapNames import map_name_dict

maximum_query_amount = 5


async def get_map_unsafe(bot, ev: CQEvent, args):
    rep_json = await get_response("https://fn.alphaleagues.com/v2/apex/map/")
    if rep_json["success"] is not True:
        bot.send('地图获取失败')
        return
    arenas_map_en = rep_json["arenas"]["map"].lower()  # 竞技场的名字英文
    arenas_map_zh = map_name_dict["arena"][arenas_map_en]  # 竞技场的名字中文
    arenas_remaining = rep_json["arenas"]["times"]["remaining"]["minutes"]  # 大逃杀剩余时间

    br_map_en = rep_json["br"]["map"].lower()  # 大逃杀的名字英文
    br_map_zh = map_name_dict["br"][br_map_en]  # 大逃杀的名字中文
    br_remaining = rep_json["br"]["times"]["remaining"]["minutes"]  # 大逃杀剩余时间

    content = f"""
当前地图
> 大逃杀: {br_map_zh}
\u23F0剩余时间: {int(br_remaining)}分钟
> 竞技场: {arenas_map_zh}
\u23F0剩余时间: {int(arenas_remaining)}分钟
""".strip()
    await bot.send(ev, content)


async def get_future_map_unsafe(bot, ev: CQEvent, args):
    query_time = 1
    if len(args) != 0:
        temp_time = int(args[0] if args[0].isdigit() else 1)
        query_time = temp_time if 1 <= temp_time <= maximum_query_amount else 1
    rep_json = await get_response(f"https://fn.alphaleagues.com/v2/apex/map/?next={query_time}")
    if rep_json["success"] is not True:
        bot.send('地图获取失败')
        return
    content = """
共查询了{}次结果
大逃杀轮换地图为\n{}
""".format(query_time,
           "\n".join(
               f"{map_name_dict['br'][result['map'].lower()]} {get_time(result['start'])}" for result in rep_json['br']['next'])
           ).strip()
    await bot.send(ev, content)
