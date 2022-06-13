#!/usr/bin/env python
# -*-coding:utf-8 -*-

try:
    import ujson as json
except Exception:
    import json
from hoshino.typing import CQEvent
from .tool import get_response
from .api import API_KEY

rank = {
    "Unranked": "未排名",
    "Bronze": "青铜",
    "Silver": "白银",
    "Gold": "黄金",
    "Platinum": "白金",
    "Diamond": "钻石",
    "Master": "大师",
    "Apex Predator": "Apex 猎杀者",
}


async def get_player_stats(bot, ev: CQEvent, args):
    if len(args) != 2:
        await bot.send(ev, "请输入正确数量的参数 [名字 平台(PC/PS4/X1)]")
        return
    if args[1] not in ["PC", "PS4", "X1"]:
        await bot.send(ev, "未知平台(PC/PS4/X1)")
        return
    params = {
        "auth": API_KEY,
        "player": args[0],
        "platform": args[1]
    }
    content = await get_response(f"https://api.mozambiquehe.re/bridge", True, params)
    if "Error" in content:
        await bot.send(ev, "请求失败, 未找到用户~")
        return
    global_data = content["global"]
    total_data = content["total"]
    reply = f"""
{global_data["name"]} 的数据 
状态: [{content["realtime"]["currentStateAsText"]}]
等级: {global_data["level"]} ({global_data["toNextLevelPercent"]}%)
大逃杀击杀数: {total_data["kills"]["value"]}
====排位====
大逃杀: {rank.get(global_data["rank"]["rankName"], "未知")} {global_data["rank"]["rankDiv"]}, {global_data["rank"]["rankScore"]} RP
竞技场: {rank.get(global_data["arena"]["rankName"], "未知")} {global_data["arena"]["rankDiv"]}, {global_data["arena"]["rankScore"]} AP
""".strip()
    await bot.send(ev, reply)
