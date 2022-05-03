from re import search
from botInit import *
from graia.application.interrupts import GroupMessageInterrupt, FriendMessageInterrupt, TempMessageInterrupt
from PIL import ImageDraw
from PIL import ImageFont

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^百度搜索(：|:| )[\u4E00-\u9FA5A-Za-z0-9_！·· ？+=@#~]+。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    flag = True
    question = message.asDisplay()[5:]
    if(message.asDisplay()[len(message.asDisplay()) - 1] == '。'):
        question = message.asDisplay()[5:-1]
    
    url = 'https://baike.baidu.com/search/word?word=' + question
    result = search(url)
    content_polysemant_type0 = result.find_all(class_ = 'polysemantList-header')
    content_polysemant_type1 = result.find_all(class_ = 'lemmaWgt-subLemmaListTitle')

    if len(content_polysemant_type0) != 0:
        choice_str = content_polysemant_type0[0].div.text.replace('\n', '')[:-4] + '\n'
        polysemantlist = result.find_all('li', class_ = 'item')
        i = 1
        for item in polysemantlist:
            choice_str += item.text.replace('▪', str(i) + '.') + '\n'
            i +=1
        choice_str = choice_str + '(若选择错误的选项将自动视为选择了第一个)'
        creatpicture(choice_str, 'baikechoice.png')
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('baikechoice.png')]))
        nextMessage = await inc.wait(GroupMessageInterrupt(group, member))
        

        try:
            choice = int(nextMessage.messageChain.asDisplay().replace('。', ''))
            if int(choice) < 1 or int(choice) > len(polysemantlist):
                choice = 1
        except ValueError:
            choice = 1

        try:
            url = 'https://baike.baidu.com' + polysemantlist[choice - 1].a["href"]
            result = search(url)
        except TypeError:
            None
        getMessage(result)
    elif len(content_polysemant_type1) != 0:
        choice_str = content_polysemant_type1[0].text.replace('\n', '') + '\n'
        polysemantlist = result.find_all(class_ = 'list-dot list-dot-paddingleft')
        i = 1
        for item in polysemantlist:
            choice_str += str(i) + '.' + item.text + '\n'
            i += 1
        choice_str = choice_str + '(若选择错误的选项将自动视为选择了第一个)'
        creatpicture(choice_str, 'baikechoice.png')
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('baikechoice.png')]))
        nextMessage = await inc.wait(GroupMessageInterrupt(group, member))
        

        try:
            choice = int(nextMessage.messageChain.asDisplay().replace('。', ''))
            if int(choice) < 1 or int(choice) > len(polysemantlist):
                choice = 1
        except ValueError:
            choice = 1

        try:
            url = 'https://baike.baidu.com' + polysemantlist[choice - 1].div.a["href"]
            result = search(url)
        except TypeError:
            None
        getMessage(result)
    else:
        try:
            getMessage(result)
        except IndexError:
            flag = False
    
    if flag:
        try:
            content_pic = result.find_all(class_ = 'summary-pic')[0].a.img["src"]
            await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('baike.png'), Image.fromNetworkAddress(content_pic)]))
        except IndexError:
            await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('baike.png')]))
    elif question == '五味狗':
        await app.sendGroupMessage(group, MessageChain.create([Plain('没有找到,去搜狗试试呢。')]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([Plain('没有找到。')]))

def getMessage(result: BeautifulSoup):
    contentstring = ''
    content_inf = result.find_all(attrs={'label-module': 'lemmaSummary', 'class': 'lemma-summary'})
    if content_inf[0].text.replace('\n', '') == '':
        content_inf = result.find_all('div', attrs={'label-module': 'para', 'class': 'para'})
    for string in content_inf[0].stripped_strings:
        if string[0] != '[' or string[-1:] != ']':
            contentstring = contentstring + string
    creatpicture(contentstring, 'baike.png')
    return contentstring

def search(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74',
    }
    
    response = requests.get(url, headers=headers)
    result = BeautifulSoup(response.text, 'html.parser')
    return result

def creatpicture(output: str, path: str):
    n_num = 1
    picture_str = ''
    txt = pilimage.new('RGB', (500, 100), (255, 255, 255))
    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype("HYNanGongTiJ.ttf",30)
    sum_width = 0
    line_height = 0
    for char in output:
        if char != '\n':
            width, height = draw.textsize(char, font)
            sum_width += width
            if sum_width > 480:
                n_num += 1
                picture_str += '\n' + char
                sum_width = width
            else:
                picture_str += char
                line_height = max(height, line_height)
        else:
            n_num += 1
            sum_width = 0
            picture_str += '\n'
    picture = pilimage.new("RGB", (500, line_height * n_num), (255, 255, 255))
    picture_draw = ImageDraw.Draw(picture)
    
    picture_draw.text((10, 5), picture_str, font=font, fill="#000000")
    picture.save(path)


@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^百度搜索(：|:| )[\u4E00-\u9FA5A-Za-z0-9_！·· ？+=@#~]+。?$')])])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    flag = True
    question = message.asDisplay()[5:]
    if(message.asDisplay()[len(message.asDisplay()) - 1] == '。'):
        question = message.asDisplay()[5:-1]
    
    url = 'https://baike.baidu.com/search/word?word=' + question
    result = search(url)
    content_polysemant_type0 = result.find_all(class_ = 'polysemantList-header')
    content_polysemant_type1 = result.find_all(class_ = 'lemmaWgt-subLemmaListTitle')

    if len(content_polysemant_type0) != 0:
        choice_str = content_polysemant_type0[0].div.text.replace('\n', '')[:-4] + '\n'
        polysemantlist = result.find_all('li', class_ = 'item')
        i = 1
        for item in polysemantlist:
            choice_str += item.text.replace('▪', str(i) + '.') + '\n'
            i +=1
        choice_str = choice_str + '(若选择错误的选项将自动视为选择了第一个)'
        creatpicture(choice_str, 'baikechoice.png')
        await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile('baikechoice.png')]))
        nextMessage = await inc.wait(FriendMessageInterrupt(friend))
        

        try:
            choice = int(nextMessage.messageChain.asDisplay().replace('。', ''))
            if int(choice) < 1 or int(choice) > len(polysemantlist):
                choice = 1
        except ValueError:
            choice = 1

        try:
            url = 'https://baike.baidu.com' + polysemantlist[choice - 1].a["href"]
            result = search(url)
        except TypeError:
            None
        getMessage(result)
    elif len(content_polysemant_type1) != 0:
        choice_str = content_polysemant_type1[0].text.replace('\n', '') + '\n'
        polysemantlist = result.find_all(class_ = 'list-dot list-dot-paddingleft')
        i = 1
        for item in polysemantlist:
            choice_str += str(i) + '.' + item.text + '\n'
            i += 1
        choice_str = choice_str + '(若选择错误的选项将自动视为选择了第一个)'
        creatpicture(choice_str, 'baikechoice.png')
        await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile('baikechoice.png')]))
        nextMessage = await inc.wait(FriendMessageInterrupt(friend))
        

        try:
            choice = int(nextMessage.messageChain.asDisplay().replace('。', ''))
            if int(choice) < 1 or int(choice) > len(polysemantlist):
                choice = 1
        except ValueError:
            choice = 1

        try:
            url = 'https://baike.baidu.com' + polysemantlist[choice - 1].div.a["href"]
            result = search(url)
        except TypeError:
            None
        getMessage(result)
    else:
        try:
            getMessage(result)
        except IndexError:
            flag = False
    
    if flag:
        try:
            content_pic = result.find_all(class_ = 'summary-pic')[0].a.img["src"]
            await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile('baike.png'), Image.fromNetworkAddress(content_pic)]))
        except IndexError:
            await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile('baike.png')]))
    elif question == '五味狗':
        await app.sendFriendMessage(friend, MessageChain.create([Plain('没有找到,去搜狗试试呢。')]))
    else:
        await app.sendFriendMessage(friend, MessageChain.create([Plain('没有找到。')]))

@bcc.receiver("TempMessage", dispatchers=[Kanata([RegexMatch('^百度搜索(：|:| )[\u4E00-\u9FA5A-Za-z0-9_！·· ？+=@#~]+。?$')])])
async def temp_message_listener(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    flag = True
    question = message.asDisplay()[5:]
    if(message.asDisplay()[len(message.asDisplay()) - 1] == '。'):
        question = message.asDisplay()[5:-1]
    
    url = 'https://baike.baidu.com/search/word?word=' + question
    result = search(url)
    content_polysemant_type0 = result.find_all(class_ = 'polysemantList-header')
    content_polysemant_type1 = result.find_all(class_ = 'lemmaWgt-subLemmaListTitle')

    if len(content_polysemant_type0) != 0:
        choice_str = content_polysemant_type0[0].div.text.replace('\n', '')[:-4] + '\n'
        polysemantlist = result.find_all('li', class_ = 'item')
        i = 1
        for item in polysemantlist:
            choice_str += item.text.replace('▪', str(i) + '.') + '\n'
            i +=1
        choice_str = choice_str + '(若选择错误的选项将自动视为选择了第一个)'
        await app.sendTempMessage(group, member, MessageChain.create([Plain(choice_str)]))
        nextMessage = await inc.wait(TempMessageInterrupt(group, member))
        

        try:
            choice = int(nextMessage.messageChain.asDisplay().replace('。', ''))
            if int(choice) < 1 or int(choice) > len(polysemantlist):
                choice = 1
        except ValueError:
            choice = 1

        try:
            url = 'https://baike.baidu.com' + polysemantlist[choice - 1].a["href"]
            result = search(url)
        except TypeError:
            None
        contentstring = getMessage(result)
    elif len(content_polysemant_type1) != 0:
        choice_str = content_polysemant_type1[0].text.replace('\n', '') + '\n'
        polysemantlist = result.find_all(class_ = 'list-dot list-dot-paddingleft')
        i = 1
        for item in polysemantlist:
            choice_str += str(i) + '.' + item.text + '\n'
            i += 1
        choice_str = choice_str + '(若选择错误的选项将自动视为选择了第一个)'
        await app.sendTempMessage(group, member, MessageChain.create([Plain(choice_str)]))
        nextMessage = await inc.wait(TempMessageInterrupt(group, member))
        

        try:
            choice = int(nextMessage.messageChain.asDisplay().replace('。', ''))
            if int(choice) < 1 or int(choice) > len(polysemantlist):
                choice = 1
        except ValueError:
            choice = 1

        try:
            url = 'https://baike.baidu.com' + polysemantlist[choice - 1].div.a["href"]
            result = search(url)
        except TypeError:
            None
        contentstring = getMessage(result)
    else:
        try:
            contentstring = getMessage(result)
        except IndexError:
            flag = False
    
    if flag:
        await app.sendTempMessage(group, member, MessageChain.create([Plain(contentstring)]))
    elif question == '五味狗':
        await app.sendTempMessage(group, member, MessageChain.create([Plain('没有找到,去搜狗试试呢。')]))
    else:
        await app.sendTempMessage(group, member, MessageChain.create([Plain('没有找到。')]))