#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
查询猎杀的最低分数
"""

try:
    import ujson as json
except Exception:
    import json

from hoshino.typing import CQEvent
from .tool import get_response
from .api import API_KEY


async def get_predator_score_line(bot, ev: CQEvent, args):
    content = await get_response(f"https://api.mozambiquehe.re/predator?auth={API_KEY}", True)
    rp = content['RP']
    ap = content['AP']
    reply = f"""
====猎杀分数线====
大逃杀
PC:     {rp['PC']['val']}RP
PS4:    {rp['PS4']['val']}RP
Xbox:   {rp['X1']['val']}RP
Switch: {rp['SWITCH']['val']}RP
竞技场
PC:     {ap['PC']['val']}RP
PS4:    {ap['PS4']['val']}RP
Xbox:   {ap['X1']['val']}RP
Switch: {ap['SWITCH']['val']}RP
""".strip()
    await bot.send(ev, reply)
