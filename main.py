'''
Core of Economy System

Copyright (C) 2024  __OopsYouDiedE__

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import sqlite3
import interactions
from interactions.api.events import MemberRemove, MessageCreate
from interactions.ext.paginators import Paginator
from collections import deque
import asyncio
import datetime
from config import DEV_GUILD
from typing import Optional, Union
import tempfile
import os
import asyncio
import csv

import aiofiles
import aiofiles.ospath
import aiofiles.os
import aioshutil
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter

from . import market_manager


class CoreEconomySystem(interactions.Extension):
    module_base: interactions.SlashCommand = interactions.SlashCommand(
        name="work",
        description="签到，赞许和生产！"
    )

    # 所有人指令：签到！
    @module_base.subcommand("daily", sub_cmd_description="打卡签到！")
    async def sell_item(self, ctx: interactions.SlashContext, item: str, num: int, exchange_item: str,
                        exchange_num: int):
        ret_id = market_manager.sell(ctx.user, item, num, exchange_item, exchange_num)
        await ctx.send(f"您已经提交订单，销售{item}*{num}，交换物品为{exchange_item}*{exchange_num}，销售id为\n{ret_id}")

    # 普通人指令：买产品。
    @module_base.subcommand("buy",
                            sub_cmd_description="输入id号，买物品。")
    @interactions.slash_option(
        name="sell_id",
        description="售单id",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    async def command_send_item(self, ctx: interactions.SlashContext,sell_id:str):

        await ctx.send(f"{market_manager.buy(ctx.user, sell_id)}")