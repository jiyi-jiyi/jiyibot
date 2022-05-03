from botInit import *

headers = {
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  + 'Chrome/75.0.3770.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}
total = 0
weiboflag = 1
@scheduler.schedule(crontabify("* * * * * 0"))
async def something_scheduled():
    global total
    global weiboflag
    response = requests.get('https://m.weibo.cn/api/container/getIndex?containerid=1005055357114809', headers=headers)
    result = json.loads(response.text)
    if weiboflag == 1:
        total = result['data']['userInfo']['statuses_count']
        weiboflag = 0
    elif total < result['data']['userInfo']['statuses_count']:
        total = result['data']['userInfo']['statuses_count']
        group = await app.getGroup(1041054936)
        card = json.loads(requests.get('https://m.weibo.cn/api/container/getIndex?containerid=1076035357114809', headers=headers).text)['data']['cards'][0]
        msg = '她发布了新微博:\n' + BeautifulSoup(card['mblog']['text'].replace('<br />', '\n'), features="html.parser").text
        await app.sendGroupMessage(group, MessageChain.create([Plain(msg)]))