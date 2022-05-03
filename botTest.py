from botInit import *
from graia.application.interrupts import FriendMessageInterrupt, TempMessageInterrupt
import yaml

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^义诊。?$')])])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    print(message)
    await app.sendFriendMessage(friend, MessageChain.create([
        Plain('本人已阅读上述所有内容，对其告知内容明白无误，同意委托团队处理电脑相关故障事宜\nA.同意\nB.不同意')
    ]))
    
    nextMessage = await inc.wait(FriendMessageInterrupt(friend))
    if nextMessage.messageChain.asDisplay() == 'A':
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain('姓名')
        ]))
        nextMessage = await inc.wait(FriendMessageInterrupt(friend))
        name = nextMessage.messageChain.asDisplay()
        memberInformation = {name :{}}

        await app.sendFriendMessage(friend, MessageChain.create([
            Plain('性别\nA.男\nB.女')
        ]))
        nextMessage = await inc.wait(FriendMessageInterrupt(friend))
        if nextMessage.messageChain.asDisplay() == 'B':
            memberInformation[name]["性别"] = "女"
        else:
            memberInformation[name]["性别"] = "男"

        
        await app.sendFriendMessage(friend, MessageChain.create([Plain('一卡通号')]))
        while True:
            nextMessage = await inc.wait(FriendMessageInterrupt(friend))

            number = nextMessage.messageChain.asDisplay()
            if number.endswith('。'):
                if len(number) == 10:
                    try:
                        memberInformation[name]["一卡通号"] = int(nextMessage.messageChain.asDisplay()[:-1])
                    except ValueError:
                        await app.sendFriendMessage(friend, MessageChain.create([Plain('请输入正确的一卡通号！')]))
                    else:
                        break
                else:
                    await app.sendFriendMessage(friend, MessageChain.create([Plain('请输入正确的一卡通号！')]))
            else:
                if len(number) == 9:
                    try:
                        memberInformation[name]["一卡通号"] = int(nextMessage.messageChain.asDisplay())
                    except:
                        await app.sendFriendMessage(friend, MessageChain.create([Plain('请输入正确的一卡通号！')]))
                    else:
                        break
                else:
                    await app.sendFriendMessage(friend, MessageChain.create([Plain('请输入正确的一卡通号！')]))

        memberInformation[name]["QQ号"] = friend.id
        
        await app.sendFriendMessage(friend, MessageChain.create([Plain('你遇到的问题(注：暂停复杂机型(见服务须知)的换硅脂服务。 更换硬件或进水拆机等服务正常。)')]))
        nextMessage = await inc.wait(FriendMessageInterrupt(friend))
        memberInformation[name]["问题"] = nextMessage.messageChain.asDisplay()

        await app.sendFriendMessage(friend, MessageChain.create([Plain('电脑型号(非必填，输入0跳过)')]))
        nextMessage = await inc.wait(FriendMessageInterrupt(friend))
        if nextMessage.messageChain.asDisplay() != '0':
            memberInformation[name]["机型"] = nextMessage.messageChain.asDisplay()

        memberInformation[name]["预约时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open('memberlist.yml', 'a+', encoding='utf-8') as memberlist:
            yaml.dump(memberInformation, memberlist, allow_unicode=True)
        with open('memberlistall.yml', 'a+', encoding='utf-8') as memberlist:
            yaml.dump(memberInformation, memberlist, allow_unicode=True)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain("已提交，待处理。")
        ]))
    else:
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain('...')
        ]))

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^撤回预约。?$')])])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    with open('memberlist.yml', 'r', encoding='utf-8') as memberlist:
        memberInformation = yaml.load(memberlist, Loader=yaml.FullLoader)
    for name in memberInformation:
        if memberInformation[name]['QQ号'] == friend.id:
            memberInformation.pop(name)
            if len(memberInformation) == 0:
                os.remove('memberlist.yml')
            else:
                with open('memberlist.yml', 'w', encoding='utf-8') as memberlist:
                    yaml.dump(memberInformation, memberlist, allow_unicode=True)
            break

    with open('memberlistall.yml', 'r', encoding='utf-8') as memberlist:
        memberInformation = yaml.load(memberlist, Loader=yaml.FullLoader)
    for name in memberInformation:
        if memberInformation[name]['QQ号'] == friend.id:
            memberInformation.pop(name)
            if len(memberInformation) == 0:
                os.remove('memberlistall.yml')
            else:
                with open('memberlistall.yml', 'w', encoding='utf-8') as memberlist:
                    yaml.dump(memberInformation, memberlist, allow_unicode=True)
            break
    await app.sendFriendMessage(friend, MessageChain.create([Plain('已撤回。')]))


@bcc.receiver("TempMessage", dispatchers=[Kanata([RegexMatch('^义诊。?$')])])
async def temp_message_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    print(message)
    await app.sendTempMessage(group, member, MessageChain.create([Plain('本人已阅读上述所有内容，对其告知内容明白无误，同意委托团队处理电脑相关故障事宜\nA.同意\nB.不同意')]))
    nextMessage = await inc.wait(TempMessageInterrupt(group, member))
    if nextMessage.messageChain.asDisplay() == 'A':
        await app.sendTempMessage(group, member, MessageChain.create([Plain('姓名')]))
        nextMessage = await inc.wait(TempMessageInterrupt(group, member))
        name = nextMessage.messageChain.asDisplay()
        memberInformation = {name :{}}

        await app.sendTempMessage(group, member, MessageChain.create([Plain('性别\nA.男\nB.女')]))
        nextMessage = await inc.wait(TempMessageInterrupt(group, member))
        if nextMessage.messageChain.asDisplay() == 'B':
            memberInformation[name]["性别"] = "女"
        else:
            memberInformation[name]["性别"] = "男"

        await app.sendTempMessage(group, member, MessageChain.create([Plain('一卡通号')]))
        while True:
            nextMessage = await inc.wait(TempMessageInterrupt(group, member))

            number = nextMessage.messageChain.asDisplay()
            if number.endswith('。'):
                if len(number) == 10:
                    try:
                        memberInformation[name]["一卡通号"] = int(nextMessage.messageChain.asDisplay()[:-1])
                    except ValueError:
                        await app.sendTempMessage(group, member, MessageChain.create([Plain('请输入正确的一卡通号！')]))
                    else:
                        break
                else:
                    await app.sendTempMessage(group, member, MessageChain.create([Plain('请输入正确的一卡通号！')]))
            else:
                if len(number) == 9:
                    try:
                        memberInformation[name]["一卡通号"] = int(nextMessage.messageChain.asDisplay())
                    except ValueError:
                        await app.sendTempMessage(group, member, MessageChain.create([Plain('请输入正确的一卡通号！')]))
                    else:
                        break
                else:
                    await app.sendTempMessage(group, member, MessageChain.create([Plain('请输入正确的一卡通号！')]))

        memberInformation[name]["一卡通号"] = int(nextMessage.messageChain.asDisplay())

        memberInformation[name]["QQ号"] = member.id

        await app.sendTempMessage(group, member, MessageChain.create([Plain('你遇到的问题(注：暂停复杂机型(见服务须知)的换硅脂服务。 更换硬件或进水拆机等服务正常。)')]))
        nextMessage = await inc.wait(TempMessageInterrupt(group, member))
        memberInformation[name]["问题"] = nextMessage.messageChain.asDisplay()

        await app.sendTempMessage(group, member, MessageChain.create([Plain('电脑型号(非必填，输入0跳过)')]))
        nextMessage = await inc.wait(TempMessageInterrupt(group, member))
        if nextMessage.messageChain.asDisplay() != '0':
            memberInformation[name]["机型"] = nextMessage.messageChain.asDisplay()
        
        memberInformation[name]["预约时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open('memberlist.yml', 'a+', encoding='utf-8') as memberlist:
            yaml.dump(memberInformation, memberlist, allow_unicode=True)
        with open('memberlistall.yml', 'a+', encoding='utf-8') as memberlist:
            yaml.dump(memberInformation, memberlist, allow_unicode=True)

        await app.sendTempMessage(group, member, MessageChain.create([Plain("已提交，义诊时间请关注https://silicom.gitee.io/#/")]))
    else:
        await app.sendTempMessage(group, member, MessageChain.create([Plain('...')]))

@bcc.receiver("TempMessage", dispatchers=[Kanata([RegexMatch('^撤回预约。?$')])])
async def temp_message_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    with open('memberlist.yml', 'r', encoding='utf-8') as memberlist:
        memberInformation = yaml.load(memberlist, Loader=yaml.FullLoader)
    for name in memberInformation:
        if memberInformation[name]['QQ号'] == member.id:
            memberInformation.pop(name)
            if len(memberInformation) == 0:
                os.remove('memberlist.yml')
            else:
                with open('memberlist.yml', 'w', encoding='utf-8') as memberlist:
                    yaml.dump(memberInformation, memberlist, allow_unicode=True)
            break

    with open('memberlistall.yml', 'r', encoding='utf-8') as memberlist:
        memberInformation = yaml.load(memberlist, Loader=yaml.FullLoader)
    for name in memberInformation:
        if memberInformation[name]['QQ号'] == member.id:
            memberInformation.pop(name)
            if len(memberInformation) == 0:
                os.remove('memberlistall.yml')
            else:
                with open('memberlistall.yml', 'w', encoding='utf-8') as memberlist:
                    yaml.dump(memberInformation, memberlist, allow_unicode=True)
            break
    await app.sendTempMessage(group, member, MessageChain.create([Plain('已撤回。')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^义诊人信息女?。?$')])])
async def group_message_handler(message: MessageChain, group: Group, app: GraiaMiraiApplication, member: Member):
    if group.id == 929284777:
        try:
            with open('memberlist.yml', 'r', encoding='utf-8') as memberlist:
                memberInformation = yaml.load(memberlist, Loader=yaml.FullLoader)
        except FileNotFoundError:
            await app.sendGroupMessage(group, MessageChain.create([Plain('本次义诊信息暂无。')]))
        else:
            count = 1
            if message.hasText('女'):
                girlsInformation = ''
                for name in memberInformation:
                    if memberInformation[name]['性别'] == '女':
                        information = str(count) + '.' + name
                        count = count + 1
                        for item in memberInformation[name]:
                            information = information + ' ' + item + ':' + str(memberInformation[name][item])
                        girlsInformation = girlsInformation + information + '\n'
                girlsInformation = girlsInformation[:-1]
                await app.sendGroupMessage(group, MessageChain.create([Plain(girlsInformation)]))
            else:
                allInformation = ''
                for name in memberInformation:
                    information = str(count) + '.' + name
                    count = count + 1
                    for item in memberInformation[name]:
                        information = information + ' ' + item + ':' + str(memberInformation[name][item])
                    allInformation = allInformation + information + '\n'
                allInformation = allInformation[:-1]
                await app.sendGroupMessage(group, MessageChain.create([Plain(allInformation)]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^重置义诊信息。?$')])])
async def group_message_handler(message: MessageChain, group: Group, app: GraiaMiraiApplication, member: Member):
    if group.id == 929284777:
        if os.path.exists('memberlist.yml'):
            os.remove('memberlist.yml')
            await app.sendGroupMessage(group, MessageChain.create([Plain('义诊信息已重置。')]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain('本来就没有。')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查询义诊真信息。?$')])])
async def group_message_handler(message: MessageChain, group: Group, app: GraiaMiraiApplication, member: Member):
    if group.id == 929284777:
        try:
            with open('memberlist.yml', 'r', encoding='utf-8') as memberlist:
                memberInformation = yaml.load(memberlist, Loader=yaml.FullLoader)
        except FileNotFoundError:
            await app.sendGroupMessage(group, MessageChain.create([Plain('本次义诊信息暂无。')]))
        else:
            for name in memberInformation:
                if memberInformation[name]['性别'] == '女':
                    await app.sendGroupMessage(group, MessageChain.create([Plain('查询真信息 ' + name)]))