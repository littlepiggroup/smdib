# -*- coding: utf-8 -*-


import requests


class Bidms(object):
    def __init__(self, username, password):
        self.session = requests.Session()
        site_url = 'http://xh.shhanqian.com:10002/bid/main.htm'
        import login
        csrf_value = login._get_csrf_token(self.session, site_url)
        login.login(self.session, csrf_value, username, password)

    def get_tong_feng_kong_tiao(self):
        import TongFengKongTiao
        return TongFengKongTiao.tfkt_data(self.session)
