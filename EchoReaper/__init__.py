#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 14.11.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

from .connections import get_connection, get_page_source
from .get_proxies import get_proxies, update_proxies
from .reaper import iter_page_sources

__version__ = "1.0.2"

__all__ = ['get_connection', 
           'get_page_source', 
           'iter_page_sources',
           'get_proxies',
           'update_proxies']