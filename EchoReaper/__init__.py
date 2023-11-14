#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 14.11.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

from .connections import get_connection, get_page_source
from .reaper import get_page_sources

__all__ = ['get_connection', 'get_page_source', 'get_page_sources']