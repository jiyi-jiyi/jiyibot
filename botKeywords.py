from botInit import *
import yaml
from graia.application.interrupts import FriendMessageInterrupt, TempMessageInterrupt

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^添加提示词#.{1,10}。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    result = message.asDisplay().replace('。', '')
    keyword = result[result.find('#') + 1:]
    record = {keyword: {}}
    record[keyword]['group'] = group.id
    record[keyword]['member'] = member.id
    with open('.\\keywords.yml', 'a+', encoding='utf-8') as keywordslist:
        yaml.dump(record, keywordslist, allow_unicode=True)
    await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain(' 提示词订阅成功。')]))
    
@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    with open('.\\keywords.yml', 'r', encoding='utf-8') as keywordslist:
        keywords = yaml.load(keywordslist, Loader=yaml.FullLoader)
    for words in keywords:
        if message.hasText(words) and keywords[words]['group'] == group.id:
            await app.sendTempMessage(keywords[words]['group'], keywords[words]['member'], MessageChain.create([Plain('提示词' + words + '已出现。\n出现的群号:' + str(group.id) + '\n出现时间:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]))

def show_my_keywords(id: int):
    try:
        with open('.\\keywords.yml', 'r', encoding='utf-8') as keywordslist:
            keywords = yaml.load(keywordslist, Loader=yaml.FullLoader)
        result = ''
        i = 1
        for words in keywords:
            if keywords[words]['member'] == id:
                result += str(i) + '.' + words + '(' + str(keywords[words]['group']) + ')' + '\n'
                i += 1
    except FileNotFoundError:
        result = '您暂时还没有设置任何一个提示词哦。 '
    return result[:-1]

@bcc.receiver('FriendMessage', dispatchers=[Kanata([RegexMatch('^查看我的提示词。?$')])])
async def friend_message_handler(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    result = show_my_keywords(friend.id)
    if len(result) > 0:
        await app.sendFriendMessage(friend, MessageChain.create([Plain(result)]))
    else:
        await app.sendFriendMessage(friend, MessageChain.create([Plain('您暂时还没有设置任何一个提示词哦。')]))

@bcc.receiver('FriendMessage', dispatchers=[Kanata([RegexMatch('^修改我的提示词。?$')])])
async def friend_message_handler(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    result = show_my_keywords(friend.id)
    if len(result) > 0:
        await app.sendFriendMessage(friend, MessageChain.create([Plain(result)]))
        with open('.\\keywords.yml', 'r', encoding='utf-8') as keywordslist:
                keywords = yaml.load(keywordslist, Loader=yaml.FullLoader)
        while True:
            await app.sendFriendMessage(friend, MessageChain.create([Plain('修改指令有:\n1.删除第i个提示词\n2.将第i个提示词更换为...')]))
            nextMessage = await inc.wait(FriendMessageInterrupt(friend))
            messageback = nextMessage.messageChain.asDisplay().replace('。', '')
            if messageback.startswith('删除第') and messageback.endswith('个提示词'):
                index = int(messageback[3:4])
                i = 1
                for words in keywords:
                    if i == index and keywords[words]['member'] == friend.id:
                        keywords.pop(words)
                        if len(keywords) == 0:
                            os.remove('.\\keywords.yml')
                        else:
                            with open('.\\keywords.yml', 'w', encoding='utf-8') as keywordslist:
                                yaml.dump(keywords, keywordslist, allow_unicode=True)
                        result_change = show_my_keywords(friend.id)
                        await app.sendFriendMessage(friend, MessageChain.create([Plain('修改后为:\n' + result_change)]))
                        break
                    elif keywords[words]['member'] == friend.id:
                        i += 1
                break
            elif messageback.startswith('将第'):
                index = int(messageback[2:3])
                i = 1
                keywords_new= {}
                for words in keywords:
                    if keywords[words]['member'] == friend.id:
                        if i == index:
                            keywords_new[messageback[10:]] = {}
                            keywords_new[messageback[10:]]['group'] = keywords[words]['group']
                            keywords_new[messageback[10:]]['member'] = friend.id
                        else:
                            keywords_new[words] = {}
                            keywords_new[words]['group'] = keywords[words]['group']
                            keywords_new[words]['member'] = friend.id
                        i += 1
                    else:
                        keywords_new[words] = {}
                        keywords_new[words]['group'] = keywords[words]['group']
                        keywords_new[words]['member'] = keywords[words]['member']
                with open('.\\keywords.yml', 'w', encoding='utf-8') as keywordslist:
                    yaml.dump(keywords_new, keywordslist, allow_unicode=True)
                result_change = show_my_keywords(friend.id)
                await app.sendFriendMessage(friend, MessageChain.create([Plain('修改后为:\n' + result_change)]))
                break
            else:
                await app.sendFriendMessage(friend, MessageChain.create([Plain('请输入正确的指令!')]))
                continue
    else:
        await app.sendFriendMessage(friend, MessageChain.create([Plain('您暂时还没有设置任何一个提示词哦。')]))