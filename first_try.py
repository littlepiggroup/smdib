# -*- coding: utf-8 -*-

import requests
import logging
import re
import json
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


def get_csrf_token(s, site_url):
    r = s.get(site_url)
    # print r.content
    html_doc = r.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    form = soup.find('form')
    inputs = form.find_all('input', recursive=False)
    csrf_input = inputs[0]
    assert csrf_input.attrs['name'] == '_csrf'
    csrf_value = csrf_input.attrs['value']
    return csrf_value


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def login(s, csrf_value):
    login_url = 'http://xh.shhanqian.com:10002/bid/login'
    form_data = [
        ('username', ''),
        ('password', ''),
        ('_csrf', csrf_value)
    ]
    r = s.post(login_url, data=form_data)
    # print r.content


class TongFengKongTiao(object):
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


def extract_table(html):
    '''

    :param html:
    :return: (updated_csrf, [TongFengKongTiao(), TongFengKongtiao()]
    '''
    logger.debug(html)
    data = []
    soup = BeautifulSoup(html, 'html.parser')
    csrf_tag = soup.find_all("meta", attrs={'name': "_csrf"})
    updated_csrf = csrf_tag[0].attrs['content']

    table = soup.find('table', attrs={'class': 'div_table_tab sortable'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols])
    objs_data = []
    for x in data:
        # print '<<<<<<<<<'
        # logger.debug(y.replace('\n', ' ').replace('\t', ' '))
        # print '>>>>>>>>>

        kong_tiao = TongFengKongTiao(x)
        objs_data.append(kong_tiao)

    logger.info("Updated csrf: %s" % updated_csrf)
    return updated_csrf, objs_data


def tfkt_data(s):
    '''
    通风空调系统
    :return: [ TongFengKongTiao(), TongFengKongTiao(), ... ]
    '''
    url = 'http://xh.shhanqian.com:10002/bid/monitor/ac/monitorAc_search.htm'
    r = s.get(url)
    html_body = r.content
    # Fetch paging info
    matched = re.search(r'postPaging\(.*\)', html_body)
    if matched:
        matched_str = matched.group()
        logger.debug(matched_str)
        paging_info = json.loads(re.search(r'{.*}', matched_str).group())
        logger.info(paging_info)
        total_pages = paging_info['totalPages']
        logger.info(total_pages)

    else:
        raise Exception('Not find postPaging string in html.')
    all_data = []
    updated_csrf, first_page = extract_table(html_body)
    all_data += first_page
    for i in range(2, total_pages + 1):
        logger.info('#### Fetch page: %d ###' % i)
        form_data = [
            ('jstree_text', '--请选择设备类型--'),
            ('equipTypeId', ''),
            ('equipGroupId', ''),
            ('equipGroup', ''),
            ('equipName', ''),
            ('_csrf', updated_csrf),
            ('cbo_build', ''),
            ('cbo_storeyCount', ''),
            ('cbo_equipPlaceCount', ''),
            ('page', str(i)),
            ('sortId', ''),
            ('order', '')
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
            ignore, page = extract_table(html_doc)
            all_data += page

    return all_data


if __name__ == '__main__':
    s = requests.Session()

    site_url = 'http://xh.shhanqian.com:10002/bid/main.htm'
    csrf_value = get_csrf_token(s, site_url)
    print csrf_value
    login(s, csrf_value)
    all_data = tfkt_data(s)

    print len(all_data)
    for data in all_data:
        print data
