#!/usr/bin/env python
# -*-coding:utf-8 -*-
import json
import aiohttp
from datetime import datetime, timedelta


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
