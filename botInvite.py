from botInit import *

@bcc.receiver("NewFriendRequestEvent")
async def event_class_generator(event: NewFriendRequestEvent):
    await event.accept()

@bcc.receiver("BotInvitedJoinGroupRequestEvent")
async def event_class_generator(event: BotInvitedJoinGroupRequestEvent):
    await event.accept()
    global group_randomJudge
    global group_waterJudge
    with open('.\\grouprandom.json', 'r') as groupRandom:
        content = groupRandom.read()
    group_randomJudge = json.loads(content)

    with open('.\\groupwater.json', 'r') as groupWater:
        content = groupWater.read()
    group_waterJudge = json.loads(content)

    group_randomJudge[str(event.groupId)] = False
    group_waterJudge[str(event.groupId)] = False

    with open('.\\grouprandom.json', 'w') as groupRandom:
        group_randomJudge_json = json.dumps(group_randomJudge)
        groupRandom.write(group_randomJudge_json)
    with open('.\\groupwater.json', 'w') as groupWater:
        group_waterJudge_json = json.dumps(group_waterJudge)
        groupWater.write(group_waterJudge_json)