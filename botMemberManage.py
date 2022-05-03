from graia.application import group
import yaml
from botInit import *

from graia.application.event.mirai import MemberUnmuteEvent
@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, group: Group, app: GraiaMiraiApplication, member: Member):
    if(message.hasText("wqc") or message.hasText('qc') or message.hasText('王翘楚')):
        await app.revokeMessage(message.__root__[0].id)

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, group: Group, app: GraiaMiraiApplication, member: Member):
    if(message.hasText('快撤回') or message.hasText('你在说什么') or message.hasText('？？？')) and message.has(Quote):
        quote_message_id = message.getFirst(Quote).id
        quote_sender_id = message.getFirst(Quote).senderId
        if quote_sender_id == 1218464365:
            await app.revokeMessage(quote_message_id)
            await app.sendGroupMessage(group, MessageChain.create([
                Plain('我说错话了，你也要记得撤回你自己的消息哦'), Face(faceId = 107)
            ]))
        else:
            await app.revokeMessage(quote_message_id)

@bcc.receiver("MemberMuteEvent")
async def event_class_generator(event: MemberMuteEvent):
    if event.member.id == 1218464365: #event.member.id == 1398155950 or event.member.id == 1469798167 or event.member.id == 1747683288 or event.member.id == 1938280643 or 
        try:
            await app.sendGroupMessage(event.member.group, MessageChain.create([
                Plain('解除禁言'), At(event.member.id)
            ]))
        except AccountMuted:
            grouphelp = await app.getGroup(929284777)
            await app.sendGroupMessage(grouphelp, MessageChain.create([
                Plain('跨群解除禁言 ' + str(event.member.group.id) + ' ' + str(event.member.id))
            ]))
    elif event.member.id == 1938280643:
        try:
            await app.unmute(event.member.group.id, event.member.id)
        except PermissionError:
            pass

@bcc.receiver("GroupMessage")
async def group_message_handler(message: MessageChain, group: Group, app: GraiaMiraiApplication, member: Member):
    with open('rootConfig.yml', 'r', encoding='utf-8') as f:
        result = yaml.load(f, Loader=yaml.FullLoader)
    message_real = message.asDisplay().replace('。', '')
    if(message.asDisplay().startswith('禁言') and member.id in result['rootUser']):
        try:
            mute_id = message.getFirst(At).target
            mute_time = re.findall(r'\d+', message.asDisplay())[1]
            mute_time = max(int(mute_time), 1)
            print(message.asDisplay())
            print(mute_time)
            await app.mute(group, mute_id, mute_time * 60)
        except IndexError and PermissionError:
            pass
    elif message.asDisplay().startswith('解除禁言') and member.id in result['rootUser']:
        unmute_id = message.getFirst(At).target
        await app.unmute(group, unmute_id)
    elif message.asDisplay().startswith('禁言我'):
        if message_real.endswith('秒') or message_real.endswith('秒钟'):
            try:
                mute_time = max(int(re.findall(r'\d+', message.asDisplay())[0]), 1)
                await app.mute(group, member.id, mute_time)
            except PermissionError:
                pass
        elif message_real.endswith('分钟'):
            try:
                mute_time = max(int(re.findall(r'\d+', message.asDisplay())[0]), 1)
                await app.mute(group, member.id, mute_time * 60)
            except PermissionError:
                pass
        elif message_real.endswith('小时'):
            try:
                mute_time = max(int(re.findall(r'\d+', message.asDisplay())[0]), 1)
                await app.mute(group, member.id, mute_time * 60 * 60)
            except PermissionError:
                pass
        elif message_real.endswith('天'):
            try:
                mute_time = max(int(re.findall(r'\d+', message.asDisplay())[0]), 1)
                await app.mute(group, member.id, mute_time * 60 * 60 * 24)
            except PermissionError:
                pass

'''@bcc.receiver("MemberUnmuteEvent")
async def event_class_generator(event: MemberUnmuteEvent):
    if event.member.id == 1938280643:
        await app.sendGroupMessage(event.member.group, MessageChain.create([
                Plain('禁言'), At(event.member.id), Plain('30天。')
        ]))'''