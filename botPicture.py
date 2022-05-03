from botInit import *

mitaoPicture = os.listdir(".\\mitao")
@bcc.receiver("GroupMessage", dispatchers=[
    #来点蜜桃猫
    Kanata([RegexMatch("来点蜜桃猫。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    mitaoPictureNum = random.randint(0, len(mitaoPicture) - 1)
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile(".\\mitao\\" + mitaoPicture[mitaoPictureNum])
    ]))


@bcc.receiver("FriendMessage", dispatchers=[
    #更新蜜桃猫图库
    Kanata([RegexMatch("投稿蜜桃猫：?")])
])
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global mitaoPicture
    mitaoTempPicture = os.listdir(".\\mitao\\temp")
    if(Image in message):
        changeImageList = message.get(Image)
        for j in range(0, len(changeImageList)):
            tempImage = changeImageList[j]
            r = requests.get(tempImage.url)
            tempStr = ".\\mitao\\temp\\" + str(len(mitaoTempPicture)) + "_temp.gif"
            with open(tempStr, "wb") as tempPicture:
                tempPicture.write(r.content)
            """
            img1 = PIL.Image.open(tempStr)
            for i in range(0, len(mitaoPicture)):
                img2 = PIL.Image.open((".\\mitao\\" + mitaoPicture[i]))
                if(cmpHash(aHash(img1), aHash(img2)) > 10):
                    continue
                else:
                    os.remove(tempStr)
                    break
            if(i == len(mitaoPicture) - 1):
                with open(".\\mitao\\" + str(len(mitaoPicture) + ".png"), "wb") as picture:
                    picture.write(r.content)
                os.remove(tempStr)
                mitaoPicture = os.listdir(".\\mitao")
            """
    await app.sendFriendMessage(friend, MessageChain.create([
        Plain(f"OK")
    ]))

EveOneCatPicture = os.listdir(".\\EveOneCat")
@bcc.receiver("GroupMessage", dispatchers=[
    #EveOneCat
    Kanata([RegexMatch("来点猫猫。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    EveOneCatPictureNum = random.randint(0,len(EveOneCatPicture) - 1)
    await app.sendGroupMessage(group, MessageChain.create([
    Image.fromLocalFile(".\\EveOneCat\\" + EveOneCatPicture[EveOneCatPictureNum])
    ]))

@bcc.receiver("FriendMessage")#更新EveOneCat图库
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global EveOneCatPicture
    if(message.hasText("手机投稿猫猫")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                tempStr = ".\\EveOneCat\\" + tempImage.imageId[-43:-7] + ".gif"
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
            ]))
        EveOneCatPicture = os.listdir(".\\EveOneCat")
    elif(message.hasText("电脑投稿猫猫")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                if len(changeImageList) > 1:
                    tempStr = ".\\EveOneCat\\" + tempImage.imageId[-43:-7] + ".gif"
                else:
                    tempStr = ".\\EveOneCat\\" + tempImage.imageId[-41:-5] + ".gif"
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
        ]))
        EveOneCatPicture = os.listdir(".\\EveOneCat")

xiaodouniPicture = os.listdir(".\\xiaodouni")
@bcc.receiver("GroupMessage", dispatchers=[
    #小豆泥
    Kanata([RegexMatch("来点小豆泥。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    xiaodouniPictureNum = random.randint(0,len(xiaodouniPicture) - 1)
    await app.sendGroupMessage(group, MessageChain.create([
    Image.fromLocalFile(".\\xiaodouni\\" + xiaodouniPicture[xiaodouniPictureNum])
    ]))

@bcc.receiver("FriendMessage")#更新小豆泥图库
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global xiaodouniPicture
    if(message.hasText("手机投稿小豆泥")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                tempStr = ".\\xiaodouni\\" + tempImage.imageId[-43:-7] + ".png"
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
            ]))
        xiaodouniPicture = os.listdir(".\\xiaodouni")
    elif(message.hasText("电脑投稿小豆泥")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                if len(changeImageList) > 1:
                    tempStr = ".\\xiaodouni\\" + tempImage.imageId[-43:-7] + ".png"
                else:
                    tempStr = ".\\xiaodouni\\" + tempImage.imageId[-41:-5] + tempImage.imageId[-4:]
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
        ]))
        xiaodouniPicture = os.listdir(".\\xiaodouni")

smPicture = os.listdir(".\\sm")
smpljjPicture = os.listdir('.\\smpljj')
@bcc.receiver("GroupMessage", dispatchers=[
    #sm群友
    Kanata([RegexMatch("^来点群友。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if(group.id == 613739714):
        smPictureNum = random.randint(0, len(smPicture) - 1)
        smpljjPictureNum = random.randint(0, len(smpljjPicture) - 1)
        if member.id == 1938280643:
            await app.sendGroupMessage(group, MessageChain.create([
                Image.fromLocalFile('.\\smpljj\\' + smpljjPicture[smpljjPictureNum])
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                Image.fromLocalFile(".\\sm\\" + smPicture[smPictureNum])
            ]))

@bcc.receiver("FriendMessage")#更新群友图库
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global smPicture
    if(message.hasText("手机投稿群友")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                tempStr = ".\\sm\\" + tempImage.imageId[-43:-7] + ".png"
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
            ]))
        smPicture = os.listdir(".\\sm")
    elif(message.hasText("电脑投稿群友")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                if len(changeImageList) > 1:
                    tempStr = ".\\sm\\" + tempImage.imageId[-43:-7] + ".png"
                else:
                    tempStr = ".\\sm\\" + tempImage.imageId[-41:-5] + ".png"
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
        ]))
        smPicture = os.listdir(".\\sm")

mcddPicture = os.listdir(".\\mcdd")
@bcc.receiver("GroupMessage", dispatchers=[
    #小鳄鱼
    Kanata([RegexMatch("^来点小鳄鱼。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    mcddPictureNum = random.randint(0, len(mcddPicture) - 1)
    await app.sendGroupMessage(group, MessageChain.create([
    Image.fromLocalFile(".\\mcdd\\" + mcddPicture[mcddPictureNum])
    ]))

@bcc.receiver("FriendMessage")#更新小鳄鱼图库
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global mcddPicture
    if(message.hasText("手机投稿小鳄鱼")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                tempStr = ".\\mcdd\\" + tempImage.imageId[-43:-7] + ".png"
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
            ]))
        mcddPicture = os.listdir(".\\mcdd")
    elif(message.hasText("电脑投稿小鳄鱼")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                if len(changeImageList) > 1:
                    tempStr = ".\\mcdd\\" + tempImage.imageId[-43:-7] + ".png"
                else:
                    tempStr = ".\\mcdd\\" + tempImage.imageId[-41:-5] + ".png"
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
        ]))
        mcddPicture = os.listdir(".\\mcdd")

girlfriendsPicture = os.listdir(".\\girlfriends")
@bcc.receiver("GroupMessage", dispatchers=[
    #老婆
    Kanata([RegexMatch("来点老婆。?$")])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if member.id == 1938280643 or group.id == 481015990:
        girlfriendsPictureNum = random.randint(0,len(girlfriendsPicture) - 1)
        await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile(".\\girlfriends\\" + girlfriendsPicture[girlfriendsPictureNum])
        ]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f"这些是jy的，你们不要想了"), Image.fromLocalFile(".\\mitao\\qxyd.gif")
        ]))

@bcc.receiver("FriendMessage")#更新老婆图库
async def friend_message_listener(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global xiaodouniPicture
    if(message.hasText("手机投稿老婆")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                tempStr = ".\\girlfriends\\" + tempImage.imageId[-43:-7] + ".png"
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
            ]))
        xiaodouniPicture = os.listdir(".\\girlfriends")
    elif(message.hasText("电脑投稿老婆")):
        if(Image in message):
            changeImageList = message.get(Image)
            for tempImage in changeImageList:
                r = requests.get(tempImage.url)
                if len(changeImageList) > 1:
                    tempStr = ".\\girlfriends\\" + tempImage.imageId[-43:-7] + ".png"
                else:
                    tempStr = ".\\girlfriends\\" + tempImage.imageId[-41:-5] + tempImage.imageId[-4:]
                with open(tempStr, "wb") as tempPicture:
                    tempPicture.write(r.content)
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"OK")
        ]))
        xiaodouniPicture = os.listdir(".\\girlfriends")

@bcc.receiver("GroupMessage", dispatchers=[
    #群聊发图
    Kanata([RegexMatch("来张logo。?$")])
])
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member
):
    await app.sendGroupMessage(group, MessageChain.create([
    Image_LocalFile(".\\jybao.jpg")
    ]))

@bcc.receiver("GroupMessage", dispatchers=[
    #pljj
    Kanata([RegexMatch("^来点漂亮姐姐。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    url = 'https://api.muxiaoguo.cn/api/meinvtu?api_key=461b9f2893b22e6e&num=5'
    judge = True
    while judge:
        response = requests.get(url)
        result = response.json()
        if result["msg"] == 'success':
            imgurl = result["data"][0]["imgurl"]
            break
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromNetworkAddress(imgurl)
    ]))

sqggPicture = os.listdir('.\\sg')
@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch("^来点帅气哥哥。?$")])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    sqggPictureNum = random.randint(0, len(sqggPicture) - 1)
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile(".\\sg\\" + sqggPicture[sqggPictureNum])
    ]))

animalspicturenum = random.randint(0,500)
@bcc.receiver("GroupMessage", dispatchers=[
    #animals
    Kanata([RegexMatch("^来点动物。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global animalspicturenum
    page = int(animalspicturenum / 10) + 1
    url = 'https://unsplash.com/napi/topics/animals/photos?page=' + str(page) + '&per_page=10'
    num = animalspicturenum % 10
    animalspicturenum = animalspicturenum + 1
    response = requests.get(url)
    r = response.json()
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromNetworkAddress(r[num]["urls"]["full"])
    ]))

foodspicturenum = random.randint(0,500)
@bcc.receiver("GroupMessage", dispatchers=[
    #foods
    Kanata([RegexMatch("^来点吃的。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global foodspicturenum
    page = int(foodspicturenum / 10) + 1
    url = 'https://unsplash.com/napi/topics/food-drink/photos?page=' + str(page) + '&per_page=10'
    num = foodspicturenum % 10
    foodspicturenum = foodspicturenum + 1
    response = requests.get(url)
    r = response.json()
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromNetworkAddress(r[num]["urls"]["full"])
    ]))

naturepicturenum = random.randint(0,500)
@bcc.receiver("GroupMessage", dispatchers=[
    #nature
    Kanata([RegexMatch("^来点自然。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global naturepicturenum
    page = int(naturepicturenum / 10) + 1
    url = 'https://unsplash.com/napi/topics/nature/photos?page=' + str(page) + '&per_page=10'
    num = naturepicturenum % 10
    naturepicturenum = naturepicturenum + 1
    response = requests.get(url)
    r = response.json()
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromNetworkAddress(r[num]["urls"]["full"])
    ]))

@bcc.receiver("GroupMessage", dispatchers=[
    #猫猫
    Kanata([RegexMatch("^来点猫。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    url = 'https://api.thecatapi.com/v1/images/search'
    pictureurl = requests.get(url)
    indexfont = pictureurl.text.find('url')
    indexback = pictureurl.text.find('width')
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromNetworkAddress(pictureurl.text[indexfont + 6:indexback - 3])
    ]))