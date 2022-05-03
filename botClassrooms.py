from botInit import *
from PIL import ImageDraw
from PIL import ImageFont
import js2py
import requests
import json
from bs4 import BeautifulSoup
import yaml
from requests.models import encode_multipart_formdata
import datetime
from graia.application.interrupts import GroupMessageInterrupt

context = js2py.EvalJs()

with open("./ids-encrypt.js") as f:
    js_content = f.read()

with open('./JLHClassroom.yml', 'r', encoding='utf-8') as file:
    classroomsList = yaml.load(file, Loader=yaml.FullLoader)

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
    picture.save('.\\classroom.png')

def encryptAES(data, salt):
    # 执行整段JS代码
    context.execute(js_content)
    result = context.encryptAES(data, salt)
    print("加密：", result)
    return result

# 登录信息门户，返回登录后的session
def login(cardnum, password):
    ss = requests.Session()
    form = {"username": cardnum}

    #  获取登录页面表单，解析隐藏值
    url = "https://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal"
    res = ss.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    attrs = soup.select('[tabid="01"] input[type="hidden"]')
    for k in attrs:
        if k.has_attr('name'):
            form[k['name']] = k['value']
        elif k.has_attr('id'):
            form[k['id']] = k['value']
    form['password'] = encryptAES(password, form['pwdDefaultEncryptSalt'])
    # 登录认证
    res = ss.post(url, data=form)
    # 登录ehall
    ss.get('http://ehall.seu.edu.cn/login?service=http://ehall.seu.edu.cn/new/index.html')

    res = ss.get('http://ehall.seu.edu.cn/jsonp/userDesktopInfo.json')
    json_res = json.loads(res.text)
    try:
        name = json_res["userName"]
        print(name[0], "** 登陆成功！")
    except Exception:
        print("认证失败！")
        return False

    return ss

ss = login(213193898, 'jiyi040106')
@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查询.{1,20}(今日|本周)使用情况。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global ss
    ss.get("http://ehall.seu.edu.cn/appShow?appId=5788938120742695")
    classroomName = message.asDisplay().replace('。', '')[2:-6]
    classroomNum = classroomsList[classroomName]
    url = 'http://ehall.seu.edu.cn/gsapp/sys/jsjyappseu1/modules/kxjsxxcx/getZyxxList.do'
    today = datetime.datetime.now()
    result = ''
    if message.asDisplay().replace('。', '').endswith('今日使用情况'):
        tomorrow = today + datetime.timedelta(days = 1)
        data = {'JASDM': classroomNum, 'KSRQ': today.strftime('%Y-%m-%d'), 'JSRQ': tomorrow.strftime('%Y-%m-%d')}
        response = ss.post(url, data)
        data = json.loads(response.text)['zyxxList']
        for item in data:
            result += item['time_display'] + ' ' + item['title'] + ' ' + item['MS'] + '\n'
        if result != '':
            creatpicture(result[:-1])
            await app.sendGroupMessage(group, MessageChain.create([Plain(result[:-1])]))
            await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('classroom.png')]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain('本教室今日全天空闲。')]))
    elif message.asDisplay().replace('。', '').endswith('本周使用情况'):
        week = today + datetime.timedelta(days = 7)
        data = {'JASDM': classroomNum, 'KSRQ': today.strftime('%Y-%m-%d'), 'JSRQ': week.strftime('%Y-%m-%d')}
        response = ss.post(url, data)
        data = json.loads(response.text)['zyxxList']
        for item in data:
            result += item['time_display'] + ' ' + item['title'] + ' ' + item['MS'] + '\n'
        if result != '':
            creatpicture(result[:-1])
            await app.sendGroupMessage(group, MessageChain.create([Plain(result[:-1])]))
            await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('classroom.png')]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain('本教室本周全部空闲。')]))

def findclassroom(choice: str):
    classroom = classroomsList.keys()
    result = []
    if choice == '1':
        for room in classroom:
            if room.startswith('教一'):
                result.append(room)
    elif choice == '2':
        for room in classroom:
            if room.startswith('教二'):
                result.append(room)
    elif choice == '3':
        for room in classroom:
            if room.startswith('教三'):
                result.append(room)
    elif choice == '4':
        for room in classroom:
            if room.startswith('教四'):
                result.append(room)
    elif choice == '5':
        for room in classroom:
            if room.startswith('教五'):
                result.append(room)
    elif choice == '6':
        for room in classroom:
            if room.startswith('教六'):
                result.append(room)
    elif choice == '7':
        for room in classroom:
            if room.startswith('教七'):
                result.append(room)
    elif choice == '8':
        for room in classroom:
            if room.startswith('教八'):
                result.append(room)
    return result

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^空教室查询。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global ss
    ss.get("http://ehall.seu.edu.cn/appShow?appId=5788938120742695")
    word = '暂仅支持查询九龙湖教1-8空教室\n输入n查询教n的空教室。'
    creatpicture(word)
    await app.sendGroupMessage(group, MessageChain.create([Plain(word)]))
    await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('classroom.png')]))
    nextMessage = await inc.wait(GroupMessageInterrupt(group, member))
    choice = nextMessage.messageChain.asDisplay().replace('。', '')
    classroom = findclassroom(choice)
    url = 'http://ehall.seu.edu.cn/gsapp/sys/jsjyappseu1/modules/kxjsxxcx/getZyxxList.do'
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days = 1)
    result = 'free      until\n'
    for roomName in classroom:
        classroomNum = classroomsList[roomName]
        data = {'JASDM': classroomNum, 'KSRQ': now.strftime('%Y-%m-%d'), 'JSRQ': tomorrow.strftime('%Y-%m-%d')}
        print(data)
        response = ss.post(url, data)
        data = json.loads(response.text)['zyxxList']
        print(response.text)
        if len(data) != 0:
            for i in range(0, len(data)):
                item = data[i]
                if now.timetuple().tm_hour < int(item['start'][-5:-3]):
                    if i == 0:
                        result += roomName + '  ' + item['start'][-5:] + '\n'
                        break
                    elif now.timetuple().tm_hour > int(data[i - 1]['end'][-5:-3]):
                        result += roomName + '  ' + item['start'][-5:] + '\n'
                        break
                if i == len(data) - 1 and now.timetuple().tm_hour > int(item['end'][-5:-3]):
                    result += roomName + '  ' + '24:00\n'
        else:
            result += roomName + '  ' + '全天空闲\n'
    if result != 'free      until\n':
        creatpicture(result[:-1])
        await app.sendGroupMessage(group, MessageChain.create([Plain(result[:-1])]))
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('classroom.png')]))
    else:
        await app.sendGroupMessage(group, MessageChain.create([Plain('本教学楼没有空闲教室。')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^重新登录。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global ss
    ss = login(213193898, 'jiyi040106')