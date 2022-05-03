from botInit import *

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if(member.id == 1799771645 and Voice in message):
        tempVoice = message.getFirst(Voice)
        tempStr = '.\\voice\\' + tempVoice.voiceId[-36:]
        r = requests.get(tempVoice.url)
        with open(tempStr, "wb") as voicefile:
            voicefile.write(r.content)

voicelist = os.listdir('.\\voice')
@bcc.receiver("GroupMessage", dispatchers = [
    #语音
    Kanata([RegexMatch("听听。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if(member.id == 1938280643 and group.id == 1041054936):
        i = random.randint(0, len(voicelist) - 1)
        await app.sendGroupMessage(group, MessageChain.create([
            Voice.fromLocalFile(".\\voice\\" + voicelist[i])
        ]))

@bcc.receiver("GroupMessage", dispatchers=[
    Kanata([RegexMatch("早安。?$")])
])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if(member.id == 1938280643 and group.id == 1041054936):
        await app.sendGroupMessage(group, MessageChain.create([
            Voice.fromLocalFile('.\\voice\\A0$JU[AV$_T28W6O44H0C%5.amr')
        ]))

'''@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch("歌。?$")])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create([
        Voice.fromLocalFile('.\\所念皆星河-房东的猫.amr')
    ]))'''