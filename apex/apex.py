#!/usr/bin/env python
# -*-coding:utf-8 -*-
import re
from typing import Dict, Callable
from hoshino import Service
from hoshino.typing import CQEvent
# from hoshino.util import filt_message
from .get_map import get_map, get_future_map
from .get_map_unsafe import get_future_map_unsafe

sv = Service('apex', help_='''
apex 查询当前地图 |->查询当前为哪张地图
apex 查询下张地图 |->查询下张地图
apex 查询轮换地图 [1-5(小时)] |->查询未来的地图以及轮换时间
'''.strip())


trigger_keyword: Dict[str, Callable] = {
    "查询当前地图": get_map,
    "查询轮换地图": get_future_map_unsafe,
    "查询下张地图": get_future_map
}


@sv.on_prefix('apex', only_to_me=True)
async def process_command(bot, ev: CQEvent):
    if not str(ev.message).strip():
        await bot.send(ev, "请输入命令")
        return
    message = str(ev.message).strip()
    command = re.findall(r"(?P<command>\w+) ?", message)
    if command[0] in trigger_keyword:
        try:
            await trigger_keyword[command[0]](bot, ev, command[1:])
        except Exception as e:
            sv.logger.error(f"{e} occur when processing command {message} in apex")