#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 14.11.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

from EchoReaper import iter_page_sources, update_proxies

def test_iter_page_sources():
    '''Test iter_page_sources'''
    for url, page in iter_page_sources(["http://google.com"]):
        assert len(page) > 1000

def test_update_proxies():
    update_proxies()
    for url, page in iter_page_sources(["http://google.com"], use_proxy=True, verbose=True):
        assert len(page) > 10