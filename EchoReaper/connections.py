#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 14.11.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

def get_chrome_options(proxy=None, advanced=False):
    '''Get Chrome options'''
    chrome_options = Options()
    chrome_options.add_argument('lang=en-US,en')
    chrome_options.add_argument('--disable-gpu')
    if advanced:
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("disable-blink-features=AutomationControlled")
    else:
        chrome_options.add_argument("--headless")
    if proxy:
        chrome_options.add_argument('--proxy-server=%s' % proxy)
    return chrome_options

def get_connection(proxy=None, advanced=False):
    '''Get connection to Chrome'''
    chrome_options = get_chrome_options(proxy, advanced)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    if advanced:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    return driver

def get_page_source(driver, url, minimum_size=0):
    '''Get page source'''
    driver.get(url)
    page_source = driver.page_source
    size = len(page_source)
    if size <= minimum_size:
        raise WebDriverException("Empty file")
    return page_source