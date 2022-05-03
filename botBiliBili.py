from botInit import *
import yaml

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'}
uid = {}
if os.path.getsize('biliUid.yml') != 0:
    with open('biliUid.yml', 'r', encoding='utf-8') as Alluid:
        uid = yaml.load(Alluid, Loader=yaml.FullLoader)

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^B站关注([1-9]\d*|0)。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global uid
    mid = message.asDisplay()[4:].replace('。', '')
    if mid in uid.keys():
        await app.sendGroupMessage(group, MessageChain.create([Plain('对象已在关注列表中。')]))
    else:
        try:
            name = json.loads(requests.get('http://api.bilibili.com/x/space/acc/info?jsonp=jsonp&mid=' + mid, headers).text)['data']['name']
            uid[mid] = [name, group.id, 0]
            with open('biliUid.yml', 'w', encoding='utf-8') as Alluid:
                yaml.dump(uid, Alluid, allow_unicode=True)
            await app.sendGroupMessage(group, MessageChain.create([Plain('成功关注' + name + '。')]))
        except:
            await app.sendGroupMessage(group, MessageChain.create([Plain('查无此人。')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^B站取关([1-9]\d*|0)。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global uid
    mid = message.asDisplay()[4:].replace('。', '')
    if mid in uid.keys() and uid[mid][1] == group.id:
        name = uid[mid][0]
        uid.pop(mid)
        if len(uid) == 0:
            os.remove('biliUid.yml')
        else:
            with open('biliUid.yml', 'w', encoding='utf-8') as Alluid:
                yaml.dump(uid, Alluid, allow_unicode=True)
        await app.sendGroupMessage(group, MessageChain.create([Plain('取关' + name + '成功。')]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([Plain('关注列表中并无此人。')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查看B站关注列表。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global uid
    result = ''
    count = 1
    for mid in uid.keys():
        if uid[mid][1] == group.id:
            result += str(count) + '.' + uid[mid][0] + ' ' + mid + '\n'
            count += 1
    if result != '':
        await app.sendGroupMessage(group, MessageChain.create([Plain(result[:-1])]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([Plain('暂无关注。')]))

@scheduler.schedule(crontabify("* * * * * 0,30"))
async def something_scheduled():
    global uid
    for mid in uid.keys():
        target = await app.getGroup(uid[mid][1])
        result = json.loads(requests.get("http://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=" + mid, headers).text)
        information = []
        if len(uid[mid]) == 3:
            uid[mid].append(result['data']['cards'][0]['desc']['timestamp'])

        elif uid[mid][3] < result['data']['cards'][0]['desc']['timestamp']:
            uid[mid][3] = result['data']['cards'][0]['desc']['timestamp']
            card = json.loads(result['data']['cards'][0]['card'])

            if result['data']['cards'][0]['desc']['type'] == 1:
                origin = json.loads(card['origin'])
                sendstr = card['user']['uname'] + '转发了' + card['origin_user']['info']['uname'] + '的动态:\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(uid[mid][3])) + '\n' + card['item']['content'] + '\n\n' + '原动态:\n'

                if card['item']['orig_type'] == 2:
                    sendstr += origin['item']['description']
                    information.append(Plain(sendstr))
                    for pic in origin['item']['pictures']:
                        information.append(Image.fromNetworkAddress(pic['img_src']))
                    information.append(Plain('https://t.bilibili.com/' + result['data']['cards'][0]['desc']['dynamic_id_str']))
                    await app.sendGroupMessage(target, MessageChain.create(information))
                
                elif card['item']['orig_type'] == 4:
                    sendstr += origin['item']['content'] + '\nhttps://t.bilibili.com/' + result['data']['cards'][0]['desc']['dynamic_id_str']
                    await app.sendGroupMessage(target, MessageChain.create([Plain(sendstr)]))
                
                elif card['item']['orig_type'] == 8:
                    sendstr += origin['title'] + '\n' + origin['desc']
                    information = [Plain(sendstr), Image.fromNetworkAddress(origin['pic']), Plain('https://t.bilibili.com/' + result['data']['cards'][0]['desc']['dynamic_id_str'])]
                    await app.sendGroupMessage(target, MessageChain.create(information))

                elif card['item']['orig_type'] == 64:
                    sendstr += origin['title'] + '\n' + origin['summary'] + '...\n'
                    information = [Plain(sendstr), Image.fromNetworkAddress(origin['image_urls'][0]), Plain('https://t.bilibili.com/' + result['data']['cards'][0]['desc']['dynamic_id_str'])]
                    await app.sendGroupMessage(target, MessageChain.create(information))

            elif result['data']['cards'][0]['desc']['type'] == 2:
                sendstr = card['user']['name'] + '发布了新动态:\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(uid[mid][3])) + '\n' + card['item']['description']
                information.append(Plain(sendstr))
                for pic in card['item']['pictures']:
                    information.append(Image.fromNetworkAddress(pic['img_src']))
                information.append(Plain('https://t.bilibili.com/' + result['data']['cards'][0]['desc']['dynamic_id_str']))
                await app.sendGroupMessage(target, MessageChain.create(information))

            elif result['data']['cards'][0]['desc']['type'] == 4:
                sendstr = card['user']['uname'] + '发布了新动态:\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(uid[mid][3])) + '\n' + card['item']['content'] + '\nhttps://t.bilibili.com/' + result['data']['cards'][0]['desc']['dynamic_id_str']
                information = [Plain(sendstr)]
                await app.sendGroupMessage(target, MessageChain.create(information))

            elif result['data']['cards'][0]['desc']['type'] == 8:
                sendstr = card['owner']['name'] + result["data"]["cards"][0]["display"]["usr_action_txt"] + ':\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(uid[mid][3])) + '\n' + card['title'] + '\n' + card['desc']
                information = [Plain(sendstr), Image.fromNetworkAddress(card['pic']), Plain('https://t.bilibili.com/' + result['data']['cards'][0]['desc']['dynamic_id_str'])]
                await app.sendGroupMessage(target, MessageChain.create(information))

            elif result['data']['cards'][0]['desc']['type'] == 64:
                sendstr = card['author']['name'] + '发布了新专栏:\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(uid[mid][3])) + '\n' + card['title'] + '\n' + card['summary'] + '...'
                information = [Plain(sendstr), Image.fromNetworkAddress(card['image_urls'][0]), Plain('https://t.bilibili.com/' + result['data']['cards'][0]['desc']['dynamic_id_str'])]
                await app.sendGroupMessage(target, MessageChain.create(information))

        liveroom = json.loads(requests.get('http://api.bilibili.com/x/space/acc/info?jsonp=jsonp&mid=' + mid, headers).text)['data']['live_room']
        if liveroom['liveStatus'] != 0 and uid[mid][2] == 0:
            await app.sendGroupMessage(target, MessageChain.create([Plain(uid[mid][0] + '正在直播' + liveroom['title'] + '\n' + liveroom['url']), Image.fromNetworkAddress(liveroom['cover'])]))
            uid[mid][2] = 1
        elif liveroom['liveStatus'] == 0 and uid[mid][2] == 1:
            uid[mid][2] = 0
        with open('biliUid.yml', 'w', encoding='utf-8') as Alluid:
            yaml.dump(uid, Alluid, allow_unicode=True)