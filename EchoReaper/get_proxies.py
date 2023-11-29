#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 14.11.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

import re
from .connections import get_connection
from random import shuffle
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(module)s %(asctime)s %(message)s')

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
    logging.info(f"Proxies saved to {file_name}, proxies: {len(data)}")

class ProxyManager:
    """Proxy manager class for handling proxies."""

    def __init__(self, file_name="proxies.txt", proxy_url="https://free-proxy-list.net/"):
        self.file_name = file_name
        self.proxy_url = proxy_url
        self.proxies = []
        self.banned_proxies = set()
        self.working_proxies = set()
        self.load_proxies()

    def load_proxies(self):
        """Load proxies from a file, shuffle them for random access."""
        if not os.path.isfile(self.file_name):
            logging.error(f"Proxy file not found: {self.file_name}, updating proxies.")
            self.update_proxies()
            return    
        try:
            with open(self.file_name) as fh:
                self.proxies = [x.strip() for x in fh if x.strip()]
            shuffle(self.proxies)
            logging.info(f"Loaded {len(self.proxies)} proxies from {self.file_name}")
        except FileNotFoundError:
            logging.error(f"Proxy file not found: {self.file_name}, updating proxies.")
            self.update_proxies()

    def update_proxies(self):
        """Update the proxy list from the specified URL and save to a file."""
        try:
            driver = get_connection(None)
            driver.get(self.proxy_url)
            data = re.findall("UTC.(.*)</textarea>", driver.page_source, re.S)
            data = data[0].strip().split("\n") if data else []
            driver.close()
            with open(self.file_name, "w") as fh:
                fh.write("\n".join(data))
            logging.info(f"Proxies updated and saved to {self.file_name}, total proxies: {len(data)}")
            self.proxies = data
            shuffle(self.proxies)
        except Exception as e:
            logging.error(f"Failed to update proxies: {e}")

    def get_proxy(self, only_working=False):
        """Get the next available proxy."""
        while self.proxies:
            proxy = self.proxies.pop(0)
            if only_working and self.working_proxies:
                if proxy in self.working_proxies:
                    return proxy
            else:
                if proxy not in self.banned_proxies:
                    return proxy
        # Optionally update proxies here if list is exhausted
        logging.warning("All proxies are banned or exhausted.")
        return None

    def ban_proxy(self, proxy):
        """Ban a proxy that is not functioning correctly."""
        self.banned_proxies.add(proxy)
        logging.info(f"Banned proxy: {proxy}")

    def add_good_proxy(self, proxy):
        """Add a proxy that is functioning correctly."""
        self.working_proxies.add(proxy)
        logging.info(f"Added good proxy: {proxy}")

    def is_exhausted(self):
        """Check if all proxies are exhausted."""
        return not bool(self.proxies)

# Example usage
# proxy_manager = ProxyManager()
# proxy = proxy_manager.get_proxy()
