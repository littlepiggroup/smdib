# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

import utils


class ElectricMeter(object):
    def __init__(self, row):
        # {'序号':'', '设备名称':'', '设备类型':'', '设备品牌':'', '系统组名':'', '安装位置':''}
        self.number = row[0]
        self.name = row[1]
        self.type = row[2]
        self.brand = row[3]
        self.group_name = row[4]
        row_5 = row[5]
        self.location = re.sub(r'[\n\t\r ]*', ' ', row_5)

    def __str__(self):
        return u'{序号: %s, 设备名称:%s, 设备类型: %s, 设备品牌: %s, 系统组名: %s, 安装位置: %s}' % (
            self.number,
            self.name,
            self.type,
            self.brand,
            self.group_name,
            self.location
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

    for d in data:
        for x in d:
            print re.sub(r'[\n\t\r ]*', ' ', x)
    total_pages = utils.get_total_pages(html)
    print total_pages

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