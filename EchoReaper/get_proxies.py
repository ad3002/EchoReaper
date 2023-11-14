#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 14.11.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

import re
from connections import get_connection
from random import shuffle

PROXY_URL = "https://free-proxy-list.net/"

def get_proxies(file_name="proxies.txt"):
    '''Get proxies from file'''
    with open(file_name) as fh:
        proxies = [x.strip() for x in fh if x.strip()]
    shuffle(proxies)
    return proxies

def update_proxies(proxy_url=PROXY_URL, file_name="proxies.txt"):
    '''Get proxies from url and save to file'''
    driver = get_connection(None)
    driver.get(proxy_url)
    data = re.findall("UTC.(.*)</textarea>", driver.page_source, re.S)
    data = data[0].strip().split("\n") if data else []
    driver.close()
    with open(file_name, "w") as fh:
        fh.write("\n".join(data))