# -*- coding: utf-8 -*-
import json
import logging
import re
logger = logging.getLogger(__name__)


def find_updated_csrf(soup):
    csrf_tag = soup.find_all("meta", attrs={'name': "_csrf"})
    updated_csrf = csrf_tag[0].attrs['content']
    return updated_csrf


def get_total_pages(html_body):
    matched = re.search(r'postPaging\(.*\)', html_body)
    if matched:
        matched_str = matched.group()
        logger.debug(matched_str)
        paging_info = json.loads(re.search(r'{.*}', matched_str).group())
        logger.info(paging_info)
        total_pages = paging_info['totalPages']
        logger.info(total_pages)

    else:
        logger.error(html_body)
        raise Exception('Not find postPaging string in html.')
    return total_pages
