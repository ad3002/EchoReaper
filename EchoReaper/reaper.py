#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 14.11.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

from math import log
import random
from .connections import get_connection, get_page_source
from .get_proxies import get_proxies
import logging
from selenium.common.exceptions import WebDriverException

logging.basicConfig(level=logging.INFO)

def get_page_sources(urls, verbose=False, use_proxy=False, def_proxy=None, minimum_size=0):
    '''Get page source
    
    Args:
        urls (list): list of urls
        verbose (bool): verbose mode [False]
        use_proxy (bool): use proxy [False]
        def_proxy (str): proxy [None]
        minimum_size (int): minimum size of page source [0]

    Yields:
        (str, str): url, page source
    '''

    proxies = get_proxies() if use_proxy and def_proxy is None else []
    proxy = random.choice(proxies) if proxies else def_proxy

    if verbose:
        logging.info(f"Proxy set to: {proxy}")

    driver = get_connection(proxy)
    banned_proxies = set()
    logging.info(f"Total tasks: {len(urls)}")
    task_id = 0
    proxies2errors = {proxy: 0}

    while urls:
        url = urls.pop(0)
        attempts = 0
        while proxies:
            try:
                if verbose:
                    logging.info(f"Attempting to download: {url}")
                page_source = get_page_source(driver, url, minimum_size=minimum_size)
                yield url, page_source
                break
            except WebDriverException as e:
                proxies2errors[proxy] += 1
                if str(e) == "Empty file" and proxies2errors[proxy] > 5:
                    banned_proxies.add(proxy)
                    proxies = [p for p in proxies if p not in banned_proxies]
                    logging.info(f"Banned proxies count: {len(banned_proxies)}. Remaining proxies: {len(proxies)}")
                if verbose:
                    logging.error(f"Error: {e}. Attempt number: {attempts}")
                driver.close()
                proxy = random.choice(proxies)
                if verbose:
                    logging.info(f"Switched to proxy: {proxy}")
                driver = get_connection(proxy)
                attempts += 1
        task_id += 1
    if not proxies:
        logging.error("All proxies are banned")
        logging.error(f"Remaining not completed tasks: {len(urls)}")
    driver.close()