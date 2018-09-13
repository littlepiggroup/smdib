# -*- coding: utf-8 -*-

import re
import logging

from bs4 import BeautifulSoup

import utils

logger = logging.getLogger(__name__)


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
        if row[6] is None or len(row[6]) == 0:
            self.cur_value = None
        else:
            self.cur_value = float(row[6].replace(",", ""))
        self.building = self.location.split('_')[0]

    def __str__(self):
        return u'{序号: %s, 设备名称:%s, 设备类型: %s, 设备品牌: %s, 安装位置: %s, 服务区域: %s, 当前读数: %s,' \
               u'楼名:%s}' % (
                   self.number,
                   self.name,
                   self.type,
                   self.brand,
                   self.location,
                   self.service_zone,
                   str(self.cur_value),
                   self.building
               )


@utils.my_timer
def electric_meter_data(s, csrf):
    url = 'http://xh.shhanqian.com:10002/bid/monitor/measure/showElectricMeterList.htm?equipTypeId=8001'
    r = s.get(url)
    html = r.content
    all_data = []

    total_pages = utils.get_total_pages(html)

    updated_csrf, first_page = parse_table(html)
    all_data += first_page

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
    for i in range(2, total_pages + 1):
        logger.info('#### Fetch page: %d ###' % i)
        form_data = [
            ('equipTypeId', '8001'),
            ('buildId', ''),
            ('equipStoryqqqqq', '0'),
            ('equipStory', ''),
            ('equipPlaceqqq', ''),
            ('equipName', ''),
            ('serviceBuild', '0'),
            ('equipTypeqqq', '0'),
            ('equipType', '0'),
            ('_csrf', updated_csrf),
            ('page', str(i))
        ]
        logger.debug(form_data)
        r = s.post(url, data=form_data)
        logger.debug(r.request.body)
        html_doc = r.content
        if r.status_code == 403:
            logger.error("Auth failed.")
            raise Exception("Auth failed")
        else:
            logger.debug(html_doc)
            ignore, page = parse_table(html_doc)
            all_data += page
    return all_data


@utils.my_timer
def hello():
    print 'Hello'
    import time
    time.sleep(10)


def parse_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    updated_csrf = utils.find_updated_csrf(soup)
    table = soup.find('table', attrs={'class': 'table-one-two-one sortable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols])
    objs_data = []
    for d in data:
        objs_data.append(ElectricMeter(map(lambda x: re.sub(r'[\n\t\r ]*', '', x), d)))
    return updated_csrf, objs_data


if __name__ == '__main__':
    hello()
