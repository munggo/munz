#-*- coding: utf-8 -*-
import asyncio, random
from .base import MzBase

import json, re
from urllib.parse import urlencode
from urllib.request import urlopen
import bs4

class AgreeHandler(MzBase):
    @asyncio.coroutine
    def proc_msg(self, msg):
        text = msg.get('text', '').lower()
        ch = msg['channel']

        if text.endswith('날씨'):
            try:
                local = text.split(' 날씨')[0].split(' ')[-1]
                param = urlencode({'weasearchstr': local})
                with urlopen("http://weather.service.msn.com/data.aspx?culture=ko-KR&weadegreetype=C&src=outlook&%s" % (param)) as response:
                    msn_data = response.read()

                res = bs4.BeautifulSoup(msn_data, 'html.parser')
                temperature = res.current.get('temperature') # 현재 온도
                feelslike = res.current.get('feelslike') # 체감 온도
                skytext = res.current.get('skytext') # 스카이코드
                humidity = res.current.get('humidity') # 습도
                wind = res.current.get('winddisplay') # 바람
                day = res.current.get('day')
                observationpoint = res.current.get('observationpoint')

                today = res.find_all('forecast')[1]
                tm = res.find_all('forecast')[2]

                res = "`%s`\n[현재] %s %s°С(체감 %s°С), 습도 %s%%, 바람 %s" % \
                       (local, skytext, temperature, feelslike, humidity, wind)
                res = res + "\n[오늘] 최고 %s°С, 최저 %s°С, %s" % (today.get('high'), today.get('low'), today.get('skytextday'))
                res = res + "\n[내일] 최고 %s°С, 최저 %s°С, %s" % (tm.get('high'), tm.get('low'), tm.get('skytextday'))
                res = res + "\n지역: %s" % (observationpoint)

                # 미세먼지 추출
                res = res + "\n" + self.micro_dust(local, observationpoint)
            except Exception as e:
                print(e)
                res = "`%s` 지역을 찾을 수 없습니다." % (local)
            yield from self.go_msg(ch, res)

    def micro_dust(self, local, address):
        url = "http://aqicn.org/xservices/search/?jsoncallback=munz&"
        local_list = address.split(' ')
        local_list.append(local)

        pattern = '\d+'

        while True:
            local = local_list.pop()

            param = urlencode({'s': local})
            with urlopen("http://aqicn.org/xservices/search/?jsoncallback=munz&%s" % (param)) as response:
                dust_info = response.read()[5:-2].decode("utf-8")
            dust = json.loads(dust_info)
            if len(dust) > 1:
                break

        url = dust[1]['url'] + '/kr'
        with urlopen(url) as response:
            detail = response.read()
            res = bs4.BeautifulSoup(detail, 'html.parser')
            print(dust[1])
            a = res.find_all('div', attrs={'class': 'aqivalue'})[0]
            result = "초미세먼지(PM2.5) 수치: *%s* %s (수집위치: %s)" % (a.string, a['title'], dust[1]['name'].split('(')[0])
            return result


