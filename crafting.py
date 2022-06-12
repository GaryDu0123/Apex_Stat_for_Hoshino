#!/usr/bin/env python
# -*-coding:utf-8 -*-
try:
    import ujson as json
except Exception:
    import json
from hoshino.typing import CQEvent
from .tool import get_response
from .crafting_names import crafting_dict, rarity_dict
from .api import API_KEY


async def get_crafting_items(bot, ev: CQEvent, args):
    content = await get_response(f"https://api.mozambiquehe.re/crafting?auth={API_KEY}", True)
    daily_bundle = []
    weekly_bundle = []
    permanent_bundle = []
    ignore_bundle = ['ammo']

    for bundle in content:
        if bundle["bundle"] in ignore_bundle:
            continue
        for items in bundle["bundleContent"]:
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
    await bot.send(ev, reply)
