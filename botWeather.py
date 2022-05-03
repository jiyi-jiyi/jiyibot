from botInit import *
from PIL import ImageDraw
from PIL import ImageFont

@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch('^查询天气[\u4E00-\u9FA5A-Za-z0-9_ ]*。?$')])])
async def group_message_handler(app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain):
    city_name = message.asDisplay()[5:].replace('。', '')
    if city_name == '':
        city_name = '江宁'
    city_code_url = 'https://geoapi.qweather.com/v2/city/lookup?key=d6e655b3ab9d421882b2991a193f12ad&location=' + city_name
    city_code_response = requests.get(city_code_url)
    city_code_response = json.loads(city_code_response.text)
    
    result_str = ''

    city_code = city_code_response['location'][0]['id']

    city_weather_url = 'https://devapi.qweather.com/v7/weather/now?key=d6e655b3ab9d421882b2991a193f12ad&location=' + city_code
    city_weather_response = requests.get(city_weather_url)
    city_weather_response = json.loads(city_weather_response.text)
    result_str = result_str + '实时温度：' + city_weather_response['now']['temp'] + '°C，' + '体感温度：' + city_weather_response['now']['feelsLike'] + '°C，' + city_weather_response['now']['text'] + '\n'
    print(city_weather_response['now']['temp'], city_weather_response['now']['feelsLike'], city_weather_response['now']['text'])

    city_live_url = 'https://devapi.qweather.com/v7/indices/1d?key=d6e655b3ab9d421882b2991a193f12ad&type=0&location=' + city_code
    city_live_response = requests.get(city_live_url)
    city_live_response = json.loads(city_live_response.text)
    if city_live_response['code'] == '200':
        result = city_live_response['daily']
        if len(result) > 4:    
            result_str = result_str + '化妆建议：' + result[0]['text'] + '\n穿衣建议：' + result[10]['text'] + '\n防晒建议：' + result[11]['text'] + '\n晾晒建议：' + result[6]['text'] + '\n运动建议：' + result[15]['text'] + '\n感冒警告：' + result[12]['text']
        else:
            result_str = result_str + '紫外线强度' + result[0]['category'] + '，' + result[1]['category'] + '洗车，' + result[2]['category'] + '去钓鱼，' + result[3]['category'] + '做运动。'
        print(result_str)

    n_num = 1
    picture_str = ''
    txt = pilimage.new('RGB', (500, 100), (255, 255, 255))
    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype("HYNanGongTiJ.ttf",30)
    sum_width = 0
    line_height = 0
    for char in result_str:
        if char != '\n':
            width, height = draw.textsize(char, font)
            sum_width += width
            if sum_width > 450:
                n_num += 1
                sum_width = 0
                picture_str += '\n'
            picture_str += char
            line_height = max(height, line_height)
        else:
            n_num += 1
            sum_width = 0
            picture_str += '\n'

    picture = pilimage.new("RGB", (500, line_height * n_num), (255, 255, 255))
    picture_draw = ImageDraw.Draw(picture)
    picture_draw.text((10, 0), picture_str, font=font, fill="#000000")
    picture.save('.\\tianqi.png')

    await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('.\\tianqi.png')]))