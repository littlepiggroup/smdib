# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def login(s, csrf_value, username, password):
    login_url = 'http://xh.shhanqian.com:10002/bid/login'
    form_data = [
        ('username', username),
        ('password', password),
        ('_csrf', csrf_value)
    ]
    r = s.post(login_url, data=form_data)
    logger.info("status code for login: %s" % str(r.status_code))

    if '登录' in r.content:
        raise Exception('Login failed. Please check your user name and password!')


def _get_csrf_token(s, site_url):
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
