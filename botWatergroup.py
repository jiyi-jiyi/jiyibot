from botInit import *

group_randomJudge = {}
group_waterJudge = {}

with open('.\\grouprandom.json', 'r') as groupRandom:
    content = groupRandom.read()
group_randomJudge = json.loads(content)

with open('.\\groupwater.json', 'r') as groupWater:
    content = groupWater.read()
group_waterJudge = json.loads(content)

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^重载复读及水群功能。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if member.id == 1398155950 or member.id == 1938280643:
        global group_randomJudge
        global group_waterJudge
        group_list = await app.groupList()
        for groupinlist in group_list:
            group_randomJudge[str(groupinlist.id)] = False
            group_waterJudge[str(groupinlist.id)] = False
        with open('.\\grouprandom.json', 'w') as groupRandom:
            group_randomJudge_json = json.dumps(group_randomJudge)
            groupRandom.write(group_randomJudge_json)
        with open('.\\groupwater.json', 'w') as groupWater:
            group_waterJudge_json = json.dumps(group_waterJudge)
            groupWater.write(group_waterJudge_json)

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^重新加载文件。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global group_randomJudge
    global group_waterJudge
    with open('.\\grouprandom.json', 'r') as groupRandom:
        content = groupRandom.read()
    group_randomJudge = json.loads(content)

    with open('.\\groupwater.json', 'r') as groupWater:
        content = groupWater.read()
    group_waterJudge = json.loads(content)
    
@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^开启随机复读。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global group_randomJudge
    if member.id == 1398155950 or member.id == 1938280643:
        group_randomJudge[str(group.id)] = True
        with open('.\\grouprandom.json', 'w') as groupRandom:
            group_randomJudge_json = json.dumps(group_randomJudge)
            groupRandom.write(group_randomJudge_json)
        await app.sendGroupMessage(group, MessageChain.create([
            Plain('随机复读已开启。')
        ]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^关闭随机复读。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global group_randomJudge
    if member.id == 1398155950 or member.id == 1938280643:
        group_randomJudge[str(group.id)] = False
        with open('.\\grouprandom.json', 'w') as groupRandom:
            group_randomJudge_json = json.dumps(group_randomJudge)
            groupRandom.write(group_randomJudge_json)
        await app.sendGroupMessage(group, MessageChain.create([
            Plain('随机复读已关闭。')
        ]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^开启水群模式。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global group_waterJudge
    if member.id == 1398155950 or member.id == 1938280643:    
        group_waterJudge[str(group.id)] = True
        with open('.\\groupwater.json', 'w') as groupWater:
            group_waterJudge_json = json.dumps(group_waterJudge)
            groupWater.write(group_waterJudge_json)
        await app.sendGroupMessage(group, MessageChain.create([
            Plain('水群模式已开启。')
        ]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^关闭水群模式。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global group_waterJudge
    if member.id == 1398155950 or member.id == 1938280643:
        group_waterJudge[str(group.id)] = False
        with open('.\\groupwater.json', 'w') as groupWater:
            group_waterJudge_json = json.dumps(group_waterJudge)
            groupWater.write(group_waterJudge_json)
        await app.sendGroupMessage(group, MessageChain.create([
            Plain('水群模式已关闭。')
        ]))

picture = {
    0: '.\\mcdd',
    1: '.\\mitao',
    2: '.\\EveOneCat',
    3: '.\\xiaodouni'
}

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if len(group_randomJudge) != 0 and len(group_waterJudge) != 0:
        if group_waterJudge[str(group.id)]:
            temp = random.randint(0,99)
            if temp < 20:
                await app.sendGroupMessage(group, message.asSendable())
        elif group_randomJudge[str(group.id)]:
            temp = random.randint(0, 99)
            if temp < 1:
                await app.sendGroupMessage(group, message.asSendable())

@scheduler.schedule(crontabify("* * * * *"))
async def something_scheduled():
    if len(group_randomJudge) != 0 and len(group_waterJudge) != 0:
        group_list = await app.groupList()
        for group in group_list:
            if group_waterJudge[str(group.id)]:
                seconds = 0
                while seconds != 20:
                    judge = random.randint(0, 99)
                    if(judge < 5):
                        whichPicture = random.randint(0, 3)
                        randomPicture = os.listdir(picture.get(whichPicture))
                        randomPictureNum = random.randint(0, len(randomPicture) - 1)
                        await app.sendGroupMessage(group, MessageChain.create([
                            Image.fromLocalFile(picture.get(whichPicture) + '\\' + randomPicture[randomPictureNum])
                        ]))
                    seconds = seconds + 1
