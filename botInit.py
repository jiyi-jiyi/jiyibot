from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio

from graia.application.message.elements.internal import ShadowImage, Image_LocalFile, Plain, At, Voice, Image, Quote, Face
from graia.application.friend import Friend

from graia.application.group import Group, Member
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch, RegexMatch, OptionalParam, RequireParam
from graia.application.event.mirai import NewFriendRequestEvent, BotInvitedJoinGroupRequestEvent, MemberJoinEvent, MemberMuteEvent
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify
from graia.application.exceptions import AccountMuted
from graia.broadcast.interrupt import InterruptControl
from graia.application.interrupts import FriendMessageInterrupt, TempMessageInterrupt, GroupMessageInterrupt

import os
import random

import schedule
import aiohttp
import cv2
import numpy as np
from PIL import Image as pilimage
import requests
import time
import json
from bs4 import BeautifulSoup
import re

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
inc = InterruptControl(bcc)
scheduler = GraiaScheduler(
    loop, bcc
)

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="INITKEYAqNRjdB4", # 填入 authKey
        account=1218464365, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    index = message.asSerializationString().find(']',message.asSerializationString().find(']') + 1)
    if (message.has(At)) and (message.getFirst(At).target == 1218464365) and (message.asSerializationString()[index + 2:] == '功能表' or message.asSerializationString()[index + 2:] == '功能表。'):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("1.复读：+xxx\n2.历史上的今天\n3.xx座今日/本周运势\n4.来点诗词/来点蜜桃猫/猫猫/小豆泥/漂亮姐姐/吃的/动物/自然\n5.成语接龙+\'成语\'\n6.来个单词\n7.查询单词 待查单词\n8.@bot+建议(:|：| )+xxx提建议\n支持猫猫和小豆泥投稿,具体见私聊版功能表…")
        ]))

@bcc.receiver("FriendMessage", dispatchers=[
    Kanata([RegexMatch("^功能表。?$")])
])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    await app.sendFriendMessage(friend, MessageChain.create([
        Plain("1.复读：+xxx\n2.历史上的今天\n3.xx座今日/本周运势\n4.来点诗词/来点蜜桃猫/猫猫/小豆泥/漂亮姐姐/吃的/动物/自然\n5.成语接龙+\'成语\'\n6.@bot+建议(:|：| )+xxx提建议\n7.投稿格式:\"手机/电脑投稿+猫猫/小豆泥+图片*n(文字图片要在一条消息中发完)\"")
    ]))

@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([RegexMatch('^来点自我介绍。?$')])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create([
        Plain('我是jy做的一个bot,发送\'功能表\'查看bot功能。')
    ]))