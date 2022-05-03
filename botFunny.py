from botInit import *

# from graia.application.event.mirai import NudgeEvent
@bcc.receiver("GroupMessage", dispatchers=[
    #群聊测试回复hello world
    Kanata([RegexMatch("测试。?$")])
])
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(f"hello {member.name}")
    ]))

@bcc.receiver("GroupMessage", dispatchers=[
    #群聊复读
    Kanata([FullMatch("复读："), RequireParam(name="saying")])
])
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
    saying: MessageChain
):
    if(saying.hasText("jy") or saying.hasText('禁言')):
        await app.sendGroupMessage(group,MessageChain.create([
            Plain(f"给👴🏻爪巴")
        ]))
    elif member.id != 2142364173 and member.id != 1445991555 and member.id != 1105656999 and member.id != 469607882 and member.id != 634959802 and member.id != 1337679228 and member.id != 1376163838 and member.id != 1218464365:
        await app.sendGroupMessage(group, saying)

@bcc.receiver("GroupMessage", dispatchers=[
    #py之父
    Kanata([RegexMatch("python之父。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile(".\\pyf.jpg")
    ]))

@bcc.receiver("GroupMessage", dispatchers=[
    #致敬元老
    Kanata([RegexMatch("bot元老。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(f"卫总！剑歌！(掌声)")
    ]))

@bcc.receiver("MemberJoinEvent")
async def event_class_generator(event: MemberJoinEvent, app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([
        At(event.member.id), Plain(f" 欢迎欢迎!"), Image_LocalFile(".\\huanyin.gif")
    ]))    

'''@bcc.receiver("NudgeEvent")
async def event_class_generator(event: NudgeEvent):
    group = await app.getGroup(event.group_id)
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(f'测试')
    ]))'''

@bcc.receiver("GroupMessage", dispatchers=[
    #历史上的今天
    Kanata([RegexMatch("^历史上的今天。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    with open('.\\历史上的今天.json', 'r', encoding='utf-8') as r:
        content = r.read()
    result = json.loads(content)['result']
    r.close()
    i = random.randint(0, len(result) - 1)
    answer = result[i]['date'] + ' ' + result[i]['title']
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(answer)
    ]))

@bcc.receiver("GroupMessage", dispatchers=[
    #星座今日运势
    Kanata([RegexMatch("^(白羊座|金牛座|双子座|巨蟹座|狮子座|处女座|天秤座|天蝎座|射手座|摩羯座|水瓶座|双鱼座)今日运势。?")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    xingzuo = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
    for i in range(0, len(xingzuo)):
        if(xingzuo[i] == message.asSerializationString()[-7:-4]):
            with open('.\\星座\\' + xingzuo[i] + '今日运势.json') as r:
                content = r.read()
            result = json.loads(content)
            r.close()
            await app.sendGroupMessage(group, MessageChain.create([
                Plain('健康指数:' + result["health"] + '\n'),
                Plain('爱情指数:' + result["love"] + '\n'),
                Plain('财运指数:' + result["money"] + '\n'),
                Plain('工作指数:' + result["work"] + '\n'),
                Plain('综合指数:' + result["all"] + '\n'),
                Plain('幸运数字:' + str(result["number"]) + '\n'),
                Plain('星座速配:' + result["QFriend"] + '\n'),
                Plain('幸运色:' + result["color"] + '\n'),
                Plain('今日概述:' + result["summary"])
            ]))

@bcc.receiver("GroupMessage", dispatchers=[
    #星座本周运势
    Kanata([RegexMatch("^(白羊座|金牛座|双子座|巨蟹座|狮子座|处女座|天秤座|天蝎座|射手座|摩羯座|水瓶座|双鱼座)本周运势。?")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    xingzuo = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
    for i in range(0, len(xingzuo)):
        if(xingzuo[i] == message.asSerializationString()[-7:-4]):
            with open('.\\星座\\' + xingzuo[i] + '本周运势.json') as r:
                content = r.read()
            result = json.loads(content)
            r.close()
            await app.sendGroupMessage(group, MessageChain.create([
                Plain('健康:' + result["health"] + '\n'),
                Plain('工作:' + result["work"] + '\n'),
                Plain('爱情:' + result["love"] + '\n'),
                Plain('财运:' + result["money"])
            ]))

@scheduler.schedule(crontabify("0 * * * *"))
async def something_scheduled():
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    Grouplist = await app.groupList()
    for i in range(0, len(Grouplist)):
        if Grouplist[i].id == 481015990:
            group = Grouplist[i]
    if minute > 50:
        hour = hour + 1
    if hour == 7:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f'good morning!')
        ]))
    if hour == 13:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f'午安')
        ]))
    if hour == 0:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f'晚安'), Image.fromLocalFile('.\\晚安.jpg')
        ]))

@scheduler.schedule(crontabify("5 * * * *"))
async def something_scheduled():
    url = "http://v.juhe.cn/todayOnhistory/queryEvent.php"
    todaydate = str(time.localtime().tm_mon) + '/' + str(time.localtime().tm_mday)
    data = {
        'key': '3ccd67b36fa5f9e5cde2f982e317c541',
        'date': todaydate
    }
    r = requests.get(url, data)
    r = r.json()
    r = json.dumps(r)
    tempStr = '.\\历史上的今天.json'
    today = open(tempStr, 'w', encoding='utf-8')
    today.write(r)
    today.close()

@scheduler.schedule(crontabify("5 * * * *"))
async def something_scheduled():
    url = "http://zhouxunwang.cn/data/?id=17"
    xingzuo = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
    for i in range(0, len(xingzuo)):
        data = {
            'key': 'VuHOrdVvQo7+iJKN9Io0R2jAMgTgsJeZ/pxz6g',
            'consName': xingzuo[i],
            'type': 'today'
        }
        r = requests.get(url, data)
        r = r.json()
        r = json.dumps(r)
        tempStr = '.\\星座\\' + xingzuo[i] + '今日运势.json'
        xinzuojson = open(tempStr, 'w', encoding='utf-8')
        xinzuojson.write(r)
        xinzuojson.close()
    
@scheduler.schedule(crontabify("5 * * * *"))
async def something_scheduled():
    url = "http://zhouxunwang.cn/data/?id=17"
    xingzuo = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
    for i in range(0, len(xingzuo)):
        data = {
            'key': 'VuHOrdVvQo7+iJKN9Io0R2jAMgTgsJeZ/pxz6g',
            'consName': xingzuo[i],
            'type': 'week'
        }
        r = requests.get(url, data)
        r = r.json()
        r = json.dumps(r)
        tempStr = '.\\星座\\' + xingzuo[i] + '本周运势.json'
        xinzuojson = open(tempStr, 'w', encoding='utf-8')
        xinzuojson.write(r)
        xinzuojson.close()

'''@bcc.receiver("GroupMessage", dispatchers=[
    #查询快递物流
    Kanata([RegexMatch("^快递单号[a-zA-Z0-9_]+$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    url = 'https://api.muxiaoguo.cn/api/Kuaidi?express=' + message.asSerializationString()[33:]
    response = requests.get(url)
    print(response.text)'''

@bcc.receiver("GroupMessage", dispatchers=[
    #诗词
    Kanata([RegexMatch("^来点诗词。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    url = 'https://api.muxiaoguo.cn/api/Gushici?api_key=28035643ae6032f3'
    response = requests.get(url)
    #print(response.text)
    result = response.json()
    if result["data"]["Poet"] != 'null':
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(result["data"]["Poetry"] + '\n' + '出自' + '《' + result["data"]["Poem_title"] + '》' + '(' + result["data"]["Poet"] + ')')
        ]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(result["data"]["Poetry"] + '\n' + '出自' + '《' + result["data"]["Poem_title"] + '》')
        ]))

@bcc.receiver("GroupMessage", dispatchers=[
    #成语接龙
    Kanata([RegexMatch("^成语接龙 [\u4E00-\u9FA5]+。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    index = message.asSerializationString().find('成语接龙') + 5
    url = 'https://api.muxiaoguo.cn/api/chengyujielong?api_key=e02b9fddf5adc6d8&word=' + message.asSerializationString()[index:]
    response = requests.get(url)
    #print(response.text)
    result = response.json()
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(result["data"]["name"])
    ]))

flag_chenyu = False
@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch("^开启成语接龙模式。?$")])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if group.id == 162425988:
        global flag_chenyu
        flag_chenyu = True
        await app.sendGroupMessage(group, MessageChain.create([
            Plain('成语接龙模式已开启，发送成语开始接龙。')
        ]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch("^关闭成语接龙模式。?$")])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global flag_chenyu
    flag_chenyu = False
    await app.sendGroupMessage(group, MessageChain.create([
        Plain('成语接龙已关闭。')
    ]))

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if flag_chenyu:
        url = 'https://api.muxiaoguo.cn/api/chengyujielong?api_key=e02b9fddf5adc6d8&word=' + message.asDisplay().replace('。','')
        response = requests.get(url)
        result = response.json()
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(result["data"]["name"])
        ]))

'''@bcc.receiver("GroupMessage", dispatchers=[
    #舔狗日记
    Kanata([RegexMatch("^舔狗日记。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, member: Member, group: Group):
    response = requests.get('https://api.muxiaoguo.cn/api/tiangourj?api_key=3c5d2c173ed956d2')
    result = response.json()
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(result["data"]["comment"])
    ]))'''

@bcc.receiver("GroupMessage", dispatchers=[
    #彩虹屁
    Kanata([RegexMatch("^(夸夸.{0,100}。?)|(^彩虹屁。?)$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, member: Member, group: Group):
    response = requests.get('https://api.muxiaoguo.cn/api/caihongpi?api_key=c01de4e0b00d9001')
    result = response.json()
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(result["data"]["comment"])
    ]))

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, member: Member, group: Group):
    if(message.hasText('存储')):
        quote_message_id = message.getFirst(Quote).id
        message_quote =await app.messageFromId(quote_message_id)
        message_quote = message_quote.messageChain
        with open('.\\诗句.txt', 'a+') as poem:
            poem.seek(0,0)
            poemlist = poem.readlines()
            i = len(poemlist) + 1
            poem.write(str(i) + '.' + message_quote.getFirst(Plain).text.replace("\n出自", "——") + '\n')
        await app.sendGroupMessage(group, MessageChain.create([
            Plain('管')
        ]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch("^来个单词。?$")])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    with open('.\\yasidanci.txt', 'r', encoding='utf-8') as words:
        words.seek(0, 0)
        wordslist = words.readlines()
        i = random.randint(0, len(wordslist) - 1)
    word = wordslist[i]
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(word.replace('\n', ''))
    ]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch("^查询单词 [A-Za-z -]+。?$")])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    index = message.asSerializationString().find(' ')
    url = 'http://dict.youdao.com/w/' + message.asSerializationString()[index + 1:]
    response = requests.get(url)
    result = BeautifulSoup(response.text, 'html.parser')
    meaninglist = result.find_all(class_ = 'trans-container')
    meaningstr = ''
    for meaning in meaninglist[0].ul.find_all('li'):
        meaningstr = meaningstr + meaning.string + '\n'
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(meaningstr[:len(meaningstr) - 1])
    ]))

zyflag = True
@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch("^开启查询单词模式。?$")])])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global zyflag
    if friend.id == 1137246791:
        zyflag = True

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch("^关闭查询单词模式。?$")])])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global zyflag
    if friend.id == 1137246791:
        zyflag = False

@bcc.receiver("FriendMessage")
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    if friend.id == 1137246791 and zyflag:
        url = 'http://dict.youdao.com/w/' + message.asDisplay()
        response = requests.get(url)
        result = BeautifulSoup(response.text, 'html.parser')
        meaninglist = result.find_all(class_ = 'trans-container')
        meaningstr = ''
        for meaning in meaninglist[0].ul.find_all('li'):
            meaningstr = meaningstr + meaning.string + '\n'
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(meaningstr[:len(meaningstr) - 1])
        ]))

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if message.hasText('精选夸夸') and (member.id == 1938280643 or member.id == 1398155950 or member.id == 873027661 or member.id == 445616983) and message.has(Quote):
        try:
            with open('.\\精选夸夸.json', 'r', encoding='utf-8') as kuakua:
                content = kuakua.read()
            kuakua = json.loads(content)
        except json.decoder.JSONDecodeError:
            kuakua = {}
        quote_message_id = message.getFirst(Quote).id
        quote_message = await app.messageFromId(quote_message_id)
        if quote_message.sender.id == 1218464365:
            kuakua[str(len(kuakua))] = quote_message.messageChain.__root__[1].text
        with open('.\\精选夸夸.json', 'w', encoding='utf-8') as kuakuawrite:
            kuakuawrite.write(json.dumps(kuakua))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^精选夸夸。?$')])])
async def group_message_handler(message: MessageChain, member: Member, app: GraiaMiraiApplication, group: Group):
    with open('.\\精选夸夸.json', 'r', encoding='utf-8') as kuakua:
        content = kuakua.read()
    kuakua = json.loads(content)
    temp = random.randint(0, len(kuakua) - 1)
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(kuakua[str(temp)])
    ]))

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if message.hasText('每日破防') and (member.id == 1938280643 or member.id == 1398155950 or member.id == 873027661 or member.id == 445616983) and message.has(Quote):
        try:
            with open('.\\每日破防.json', 'r', encoding='utf-8') as pofang:
                content = pofang.read()
            pofang = json.loads(content)
        except json.decoder.JSONDecodeError:
            pofang = {}
        quote_message_id = message.getFirst(Quote).id
        quote_message = await app.messageFromId(quote_message_id)
        if quote_message.sender.id == 1218464365:
            pofang[str(len(pofang))] = quote_message.messageChain.__root__[1].text
        with open('.\\每日破防.json', 'w', encoding='utf-8') as pofangwrite:
            pofangwrite.write(json.dumps(pofang))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^每日破防。?$')])])
async def group_message_handler(message: MessageChain, member: Member, app: GraiaMiraiApplication, group: Group):
    with open('.\\每日破防.json', 'r', encoding='utf-8') as pofang:
        content = pofang.read()
    pofang = json.loads(content)
    temp = random.randint(0, len(pofang) - 1)
    await app.sendGroupMessage(group, MessageChain.create([
        Plain(pofang[str(temp)])
    ]))

'''@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^拍拍我。?$')])])
async def group_message_handler(message: MessageChain, member: Member, app: GraiaMiraiApplication, group: Group):
    await app.nudge(member)

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group):
    if message.has(At) and (message.asDisplay().startswith('拍拍') or message.asDisplay().startswith('揉揉') or message.asDisplay().startswith('亲亲') or message.asDisplay().startswith('摸摸') or message.asDisplay().startswith('捏捏')):
        memberList = message.get(At)
        for i in memberList:
            member = await app.getMember(group.id, i.target)
            await app.nudge(member)'''