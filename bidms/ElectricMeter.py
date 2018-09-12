# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

import utils


class ElectricMeter(object):
    def __init__(self, row):
        # 1. 序号
        # 2. 设备名称
        # 3. 设备型号
        # 4. 设备品牌
        # 5. 安装位置
        # 6. 服务区域
        # 7. 当前读数(kw.h)   float()?
        # 8. 智能跳转
        self.number = row[0]
        self.name = row[1]
        self.type = row[2]
        self.brand = row[3]
        self.location = row[4]
        self.service_zone = row[5]
        self.cur_value = row[6]
        self.building = self.location.split('_')[0]

    def __str__(self):
        return u'{序号: %s, 设备名称:%s, 设备类型: %s, 设备品牌: %s, 安装位置: %s, 服务区域: %s, 当前读数: %s,' \
               u'楼名:%s' % (
            self.number,
            self.name,
            self.type,
            self.brand,
            self.location,
            self.service_zone,
            self.cur_value,
            self.building
        )

def electric_meter_data(s):
    url = 'http://xh.shhanqian.com:10002/bid/monitor/measure/showElectricMeterList.htm?equipTypeId=8001'
    r = s.get(url)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', attrs={'class': 'table-one-two-one sortable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols])
    xs = []
    for d in data:
        xs.append(ElectricMeter(map(lambda x: re.sub(r'[\n\t\r ]*', '', x),d)))
        for x in d:
            # print re.sub(r'[\n\t\r ]*', '', x)
            pass
    total_pages = utils.get_total_pages(html)

    for meter in xs:
        print meter
    # print total_pages

    '''
    Request URL: http://xh.shhanqian.com:10002/bid/monitor/measure/showElectricMeterList.htm

    
equipTypeId: 8001
buildId: 
equipStoryqqqqq: 0
equipStory: 0
equipPlaceqqq: 
equipName: 
serviceBuild: 0
equipTypeqqq: 0
equipType: 0
_csrf: f4224554-4c6b-42d7-8c34-450e1993dfee
page: 4
    '''

if __name__ == '__main__':
    pass