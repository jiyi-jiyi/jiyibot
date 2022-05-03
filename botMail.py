from botInit import *
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
from PIL import ImageDraw
from PIL import ImageFont

my_sender = '1938280643@qq.com'  # 填写发信人的邮箱账号
my_pass = 'hpntunzozjvnbbfh'  # 发件人邮箱授权码
my_user = '@qq.com'  # 收件人邮箱账号
memberlist = {}
try:
    with open('memberlist.json', 'r') as inf:
        memberlist = json.loads(inf.read())
except FileNotFoundError:
    None

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^订阅.{1,20}每日天气。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global memberlist
    cityname = message.asDisplay().replace('。', '')[2:-4]
    for i in range(0, len(memberlist)):
        if memberlist[str(i)][0] == str(member.id) and memberlist[str(i)][1] == cityname:
            await app.sendGroupMessage(group, MessageChain.create([Plain('已有此纪录。')]))
    else:
        memberlist[str(len(memberlist))] = [str(member.id), cityname]
        with open('memberlist.json', 'w') as inf:
            inf.write(json.dumps(memberlist))
        await app.sendGroupMessage(group, MessageChain.create([Plain('订阅成功。')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查看我的订阅。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global memberlist
    j = 1
    result = ''
    for i in range(0, len(memberlist)):
        if memberlist[str(i)][0] == str(member.id):
            result += str(j) + '.' + memberlist[str(i)][1] + '\n'
            j += 1
    if result != '':
        creatpicture(result[:-1])
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\订阅.png')]))
    else:
        creatpicture('您暂时还没有任何订阅。')
        await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\订阅.png')]))

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^删除.{1,20}的订阅。?$')])])
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    global memberlist
    city_name = message.asDisplay().replace('。', '')[2:-3]
    index = len(memberlist) - 1
    print(memberlist)
    for i in range(0, len(memberlist)):
        if memberlist[str(i)][0] == str(member.id) and memberlist[str(i)][1] == city_name:
            if i == index:
                del memberlist[str(i)]
                break
            else:
                memberlist[str(i)][0] = memberlist[str(index)][0]
                memberlist[str(i)][1] = memberlist[str(index)][1]
                del memberlist[str(index)]
                break
    if len(memberlist) != 0:
        with open('memberlist.json', 'w') as inf:
            inf.write(json.dumps(memberlist))
    else:
        os.remove('memberlist.json')
    await app.sendGroupMessage(group, MessageChain.create([Plain('删除成功。')]))

@scheduler.schedule(crontabify("30 6 * * *"))
async def something_scheduled():
    global memberlist
    for i in range(0, len(memberlist)):
        my_user = memberlist[str(i)][0] + '@qq.com'
        message = memberlist[str(i)][1] + '天气:\n' + getInf(memberlist[str(i)][1])
        sendMail(my_sender, my_pass, my_user, message)

def sendMail(my_sender: str, my_pass: str, my_user: str, message: str):
    msg = MIMEText(message, 'plain', 'utf-8')  # 填写邮件内容
    msg['From'] = formataddr(["jiyi", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["今日天气", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = "今日天气"  # 邮件的主题，也可以说是标
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
    server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接

def getInf(city_name: str):
    city_code_url = 'https://geoapi.qweather.com/v2/city/lookup?key=d6e655b3ab9d421882b2991a193f12ad&location=' + city_name
    city_code_response = requests.get(city_code_url)
    city_code_response = json.loads(city_code_response.text)
    
    result_str = ''

    city_code = city_code_response['location'][0]['id']

    city_weather_url = 'https://devapi.qweather.com/v7/weather/now?key=d6e655b3ab9d421882b2991a193f12ad&location=' + city_code
    city_weather_response = requests.get(city_weather_url)
    city_weather_response = json.loads(city_weather_response.text)
    result_str = result_str + '实时温度：' + city_weather_response['now']['temp'] + '°C，' + '体感温度：' + city_weather_response['now']['feelsLike'] + '°C，' + city_weather_response['now']['text'] + '\n'

    city_live_url = 'https://devapi.qweather.com/v7/indices/1d?key=d6e655b3ab9d421882b2991a193f12ad&type=0&location=' + city_code
    city_live_response = requests.get(city_live_url)
    city_live_response = json.loads(city_live_response.text)
    if city_live_response['code'] == '200':
        result = city_live_response['daily']
        if len(result) > 4:    
            result_str = result_str + '化妆建议：' + result[0]['text'] + '\n穿衣建议：' + result[10]['text'] + '\n防晒建议：' + result[11]['text'] + '\n晾晒建议：' + result[6]['text'] + '\n运动建议：' + result[15]['text'] + '\n感冒警告：' + result[12]['text']
        else:
            result_str = result_str + '紫外线强度' + result[0]['category'] + '，' + result[1]['category'] + '洗车，' + result[2]['category'] + '去钓鱼，' + result[3]['category'] + '做运动。'
        return result_str

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
    picture.save('.\\订阅.png')

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^订阅.{1,20}每日天气。?$')])])
async def friend_message_handler(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global memberlist
    cityname = message.asDisplay().replace('。', '')[2:-4]
    for i in range(0, len(memberlist)):
        if memberlist[str(i)][0] == str(friend.id) and memberlist[str(i)][1] == cityname:
            await app.sendFriendMessage(friend, MessageChain.create([Plain('已有此纪录。')]))
    else:
        memberlist[str(len(memberlist))] = [str(friend.id), cityname]
        with open('memberlist.json', 'w') as inf:
            inf.write(json.dumps(memberlist))
        await app.sendFriendMessage(friend, MessageChain.create([Plain('订阅成功。')]))

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^查看我的订阅。?$')])])
async def friend_message_handler(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global memberlist
    j = 1
    result = ''
    for i in range(0, len(memberlist)):
        if memberlist[str(i)][0] == str(friend.id):
            result += str(j) + '.' + memberlist[str(i)][1] + '\n'
            j += 1
    if result != '':
        creatpicture(result[:-1])
        await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile('.\\订阅.png')]))
    else:
        creatpicture('您暂时还没有任何订阅。')
        await app.sendFriendMessage(friend, MessageChain.create([Image.fromLocalFile('.\\订阅.png')]))

@bcc.receiver("FriendMessage", dispatchers=[Kanata([RegexMatch('^删除.{1,20}的订阅。?$')])])
async def friend_message_handler(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    global memberlist
    city_name = message.asDisplay().replace('。', '')[2:-3]
    index = len(memberlist) - 1
    print(memberlist)
    for i in range(0, len(memberlist)):
        if memberlist[str(i)][0] == str(friend.id) and memberlist[str(i)][1] == city_name:
            if i == index:
                del memberlist[str(i)]
                break
            else:
                memberlist[str(i)][0] = memberlist[str(index)][0]
                memberlist[str(i)][1] = memberlist[str(index)][1]
                del memberlist[str(index)]
                break
    if len(memberlist) != 0:
        with open('memberlist.json', 'w') as inf:
            inf.write(json.dumps(memberlist))
    else:
        os.remove('memberlist.json')
    await app.sendFriendMessage(friend, MessageChain.create([Plain('删除成功。')]))