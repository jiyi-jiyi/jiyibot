from botInit import *
from PIL import ImageDraw
from PIL import ImageFont
from base64 import b64encode
from Crypto.Cipher import AES
from bs4 import BeautifulSoup

e = "010001"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"
i = "0hyFaCNAVzOIdoht"

def get_encSecKey():
    return "4022359ea3110bcd034e0160c3b89e5e172fd0110a3cf765d9f366d9fd09840a1f4a4705ac43719fdb8bfeb44d3b92334733061ad10942131184a4dfba0ac9d2cf867b8b6236523c1ca5f44c0d2d82c1c2665a3137a9241c7373539c1aa8e5e9bb9d33dafc764b5d76c2ab34fc94df85e27a934c8a603fa713f2cf38c2b7bbae"

def get_params(data): #data默认是json字符串
    first = enc_params(data,g)
    second = enc_params(first,i)
    return second

def to_16(data):
    pad = 16-len(data)%16
    data +=chr(pad) * pad
    return data

def enc_params(data,key): #加密过程
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'),IV=iv.encode('utf-8'),mode=AES.MODE_CBC) #创建加密器
    bs = aes.encrypt(data.encode('utf-8')) #加密
    return str(b64encode(bs),"utf-8") #转化成字符串

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41'
}



@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^点歌.{1,50}。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    songname = message.asDisplay()[2:].replace('。',' ')
    url = (f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={songname}&type=1&offset=0&total=true&limit=20').replace(' ', '%20')
    getid = str(json.loads(requests.get(url).text)["result"]["songs"][0]["id"])
    await app.sendGroupMessage(group, MessageChain.create([Plain('https://y.music.163.com/m/song/' + getid)]))

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^点歌.{1,50}。?$')])])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    songname = message.asDisplay()[2:].replace('。',' ')
    url = (f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={songname}&type=1&offset=0&total=true&limit=20').replace(' ', '%20')
    getid = str(json.loads(requests.get(url).text)["result"]["songs"][0]["id"])
    await app.sendFriendMessage(friend, MessageChain.create([Plain('https://y.music.163.com/m/song/' + getid)]))

def creatpicture(output: str):
    n_num = 1
    picture_str = ''
    txt = pilimage.new('RGB', (500, 100), (255, 255, 255))
    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype("simkai.ttf",30)
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
    
    picture_draw.text((10, 0), picture_str, font=font, fill="#000000")
    picture.save('.\\song.png')

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查看昵称为.{1,20}的歌单。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    nickname = message.asDisplay().replace("。", "")[5:-3]
    userlist = json.loads(requests.get(f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={nickname}&type=1002&offset=0&total=true&limit=20').text)['result']['userprofiles']
    for user in userlist:
        if user["nickname"] == nickname:
            userId = str(user["userId"])
            break
    data = {"uid":userId, "wordwrap":"7", "offset":"0", "total":"true", "limit":"999", "csrf_token":""}
    url = 'https://music.163.com/weapi/user/playlist?csrf_token='
    result = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)), "encSecKey":get_encSecKey()} ,headers=headers).text)["playlist"]
    output = ''
    selfflag = True
    otherflag = True
    i = 1
    if len(result) != 0:
        for playlist in result:
            if selfflag and str(playlist['userId']) == userId:
                output = output + '自建歌单:\n'
                selfflag = False
            elif otherflag and str(playlist['userId']) != userId:
                output = output + '收藏歌单:\n'
                otherflag = False
                i = 1
            output = output + str(i) + '.' + playlist['name'] + '\n'
            i += 1
        output = output[:-1]
    else:
        output = '此人没有歌单。'
    creatpicture(output)
    await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查看昵称为.{1,20}的关注。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    nickname = message.asDisplay().replace("。", "")[5:-3]
    userlist = json.loads(requests.get(f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={nickname}&type=1002&offset=0&total=true&limit=20').text)['result']['userprofiles']
    for user in userlist:
        if user["nickname"] == nickname:
            userId = str(user["userId"])
            break
    url = f'https://music.163.com/weapi/user/getfollows/{userId}?csrf_token=f100d0ce73e79f11c31436075c29e6aa'
    data = {"uid":userId,"offset":"0","total":"true","limit":"999", "csrf_token":""}
    response = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)),"encSecKey":get_encSecKey()} ,headers=headers).text)["follow"]
    output = ''
    i = 1
    for people in response:
        output = output + str(i) + '.' + people["nickname"] + '\n'
        i += 1
    if output != '':
        creatpicture(output[:-1])
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))
    else:
        creatpicture('此人没有关注。')
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查看昵称为.{1,20}的粉丝。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    nickname = message.asDisplay().replace("。", "")[5:-3]
    userlist = json.loads(requests.get(f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={nickname}&type=1002&offset=0&total=true&limit=20').text)['result']['userprofiles']
    for user in userlist:
        if user["nickname"] == nickname:
            userId = str(user["userId"])
            break
    url = 'https://music.163.com/weapi/user/getfolloweds?csrf_token=f100d0ce73e79f11c31436075c29e6aa'
    data = {"userId":userId,"offset":"0","total":"true","limit":"20","csrf_token":""}
    response = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)),"encSecKey":get_encSecKey()} ,headers=headers).text)["followeds"]
    output = ''
    i = 1
    for people in response:
        output = output + str(i) + '.' + people["nickname"] + '\n'
        i += 1
    if output != '':
        creatpicture(output[:-1])
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))
    else:
        creatpicture('此人没有粉丝。')
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^查看昵称为.{1,20}的歌单。?$')])])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    nickname = message.asDisplay().replace("。", "")[5:-3]
    userlist = json.loads(requests.get(f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={nickname}&type=1002&offset=0&total=true&limit=20').text)['result']['userprofiles']
    for user in userlist:
        if user["nickname"] == nickname:
            userId = str(user["userId"])
            break
    data = {"uid":userId, "wordwrap":"7", "offset":"0", "total":"true", "limit":"999", "csrf_token":""}
    url = 'https://music.163.com/weapi/user/playlist?csrf_token='
    result = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)), "encSecKey":get_encSecKey()} ,headers=headers).text)["playlist"]
    output = ''
    selfflag = True
    otherflag = True
    i = 1
    for playlist in result:
        if selfflag and str(playlist['userId']) == userId:
            output = output + '自建歌单:\n'
            selfflag = False
        elif otherflag and str(playlist['userId']) != userId:
            output = output + '收藏歌单:\n'
            otherflag = False
            i = 1
        output = output + str(i) + '.' + playlist['name'] + '\n'
        i += 1
    creatpicture(output)
    await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile('.\\song.png')]))

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^查看昵称为.{1,20}的关注。?$')])])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    nickname = message.asDisplay().replace("。", "")[5:-3]
    userlist = json.loads(requests.get(f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={nickname}&type=1002&offset=0&total=true&limit=20').text)['result']['userprofiles']
    for user in userlist:
        if user["nickname"] == nickname:
            userId = str(user["userId"])
            break
    url = f'https://music.163.com/weapi/user/getfollows/{userId}?csrf_token=f100d0ce73e79f11c31436075c29e6aa'
    data = {"uid":userId,"offset":"0","total":"true","limit":"999", "csrf_token":""}
    response = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)),"encSecKey":get_encSecKey()} ,headers=headers).text)["follow"]
    output = ''
    i = 1
    for people in response:
        output = output + str(i) + '.' + people["nickname"] + '\n'
        i += 1
    creatpicture(output)
    await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile('.\\song.png')]))

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^查看昵称为.{1,20}的粉丝。?$')])])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    nickname = message.asDisplay().replace("。", "")[5:-3]
    userlist = json.loads(requests.get(f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={nickname}&type=1002&offset=0&total=true&limit=20').text)['result']['userprofiles']
    for user in userlist:
        if user["nickname"] == nickname:
            userId = str(user["userId"])
            break
    url = 'https://music.163.com/weapi/user/getfolloweds?csrf_token=f100d0ce73e79f11c31436075c29e6aa'
    data = {"userId":userId,"offset":"0","total":"true","limit":"20","csrf_token":""}
    response = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)),"encSecKey":get_encSecKey()} ,headers=headers).text)["followeds"]
    output = ''
    i = 1
    for people in response:
        output = output + str(i) + '.' + people["nickname"] + '\n'
        i += 1
    creatpicture(output)
    await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile('.\\song.png')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查看歌手.{1,20}。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    artistname = message.asDisplay()[4:].replace('。',' ')
    url = 'https://music.163.com/weapi/search/suggest/multimatch?csrf_token='
    data = {"s": artistname, "csrf_token": ""}
    artistid = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)),"encSecKey":get_encSecKey()}, headers=headers).text)["result"]["artist"][0]["id"]
    url = 'https://music.163.com/artist/desc?id=' + str(artistid)
    result = BeautifulSoup(requests.get(url).text, 'html.parser').find_all('div', attrs={'class': 'n-artdesc'})[0]
    h = result.find('h2')
    p = result.find('p')
    content = h.text.replace(u'\xa0', '') + ':\n' + p.text
    creatpicture(content)
    await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查看播客.{1,20}。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    djRadiosname = message.asDisplay()[4:].replace('。',' ')
    url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    data = {"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":djRadiosname,"type":"1009","offset":"0","total":"true","limit":"30","csrf_token":""}
    result_str = djRadiosname + '\n'
    try:
        djRadiosid = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)),"encSecKey":get_encSecKey()}, headers=headers).text)['result']['djRadios'][0]['id']
        url = 'https://music.163.com/djradio?id=' + str(djRadiosid)
        result = BeautifulSoup(requests.get(url, headers).text, 'html.parser')
        songList = result.find_all('div', class_ = 'tt f-thide')
        i = 1
        for song in songList:
            result_str += str(i) + '.' + song.a["title"] + '\n'
            i += 1
    except KeyError:
        result_str = '未查询到此播客。。'
    creatpicture(result_str[:-1])
    await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))

As_songlist_url = {'向晚': 'https://music.163.com/djradio?id=959003611', '贝拉': 'https://music.163.com/djradio?id=959475841', 
'珈乐': 'https://music.163.com/djradio?id=959471867', '嘉然': 'https://music.163.com/djradio?id=959370203', 
'乃琳': 'https://music.163.com/djradio?id=959453342', 'as': 'https://music.163.com/djradio?id=959803751'}
@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^(向晚|贝拉|珈乐|嘉然|乃琳|as)翻唱合集。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global As_songlist_url
    As_name = message.asDisplay()[:2]
    result_str = message.asDisplay() + '\n'
    url = As_songlist_url[As_name]
    result = BeautifulSoup(requests.get(url, headers).text, 'html.parser')
    songList = result.find_all('div', class_ = 'tt f-thide')
    i = 1
    for song in songList:
        result_str += str(i) + '.' + song.a["title"] + '\n'
        i += 1
    creatpicture(result_str[:-1])
    await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^听(向晚|贝拉|珈乐|嘉然|乃琳|as)唱歌。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global As_songlist_url
    As_name = message.asDisplay()[1:3]
    result_str = '发送下列歌曲前的数字选择想听的歌哦。' + '\n'
    url = As_songlist_url[As_name]
    result = BeautifulSoup(requests.get(url, headers).text, 'html.parser')
    songList = result.find_all('div', class_ = 'tt f-thide')
    i = 1
    for song in songList:
        result_str += str(i) + '.' + song.a["title"] + '\n'
        i += 1
    creatpicture(result_str[:-1])
    await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))
    nextMessage = await inc.wait(GroupMessageInterrupt(group, member))
    num = nextMessage.messageChain.asDisplay().replace('。', '')
    await app.sendGroupMessage(group, MessageChain.create([Plain('https://music.163.com' + songList[int(num) - 1].a["href"])]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查看.{1,50}歌词。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    songname = message.asDisplay()[2:].replace('。',' ')[:-2]
    url = (f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={songname}&type=1&offset=0&total=true&limit=20').replace(' ', '%20')
    getid = str(json.loads(requests.get(url).text)["result"]["songs"][0]["id"])
    data = {"id":getid,"lv":-1,"tv":-1,"csrf_token":""}
    url = 'https://music.163.com/weapi/song/lyric?csrf_token='
    lyriclist = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)),"encSecKey":get_encSecKey()}, headers=headers).text)["lrc"]["lyric"].splitlines(True)
    lyric = ''
    for item in lyriclist:
        lyric += item[item.find(']') + 1:]
    creatpicture(lyric)
    await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\song.png')]))


# QQ音乐
@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^QQ点歌.{1,50}。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    songname = message.asDisplay()[4:].replace('。',' ')
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59'
    }
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?format=json&outCharset=utf-8&w={name}'.format(name=songname)
    response = json.loads(requests.get(url, headers=headers).text)
    await app.sendGroupMessage(group, MessageChain.create([Plain('https://i.y.qq.com/v8/playsong.html?songmid=' + response["data"]["song"]["list"][0]["songmid"])]))

eventsize = 0
eventflag = 1
@scheduler.schedule(crontabify("* * * * * 0,20,40"))
async def something_scheduled():
    global eventflag
    global eventsize
    group = await app.getGroup(1041054936)
    url = 'https://music.163.com/weapi/event/get/1504038215?csrf_token='
    data = {"userId":"1504038215","total":"true","limit":"20","time":"-1","getcounts":"true","csrf_token":""}
    events = json.loads(requests.post(url, data={"params":get_params(json.dumps(data)),"encSecKey":get_encSecKey()}, headers=headers).text)
    if eventflag == 1:
        eventsize = events['size']
        eventflag = 0
    elif events['size'] != eventsize:
        eventsize = events['size']
        result = '她网易云发布了新动态:\n' + json.loads(events['events'][0]['json'])['msg']
        print(events['events'][0]['info']['commentThread']['resourceTitle'][0:4])
        if events['events'][0]['info']['commentThread']['resourceTitle'][0:4] == '分享单曲':
            result += '\n' + events['events'][0]['info']['commentThread']['resourceTitle']
        await app.sendGroupMessage(group, MessageChain.create([Plain(result)]))