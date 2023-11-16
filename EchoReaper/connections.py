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
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import threading


class EmptyFileException(Exception):
    pass


def get_chrome_options(proxy=None, advanced=False):
    '''Get Chrome options'''
    chrome_options = Options()
    chrome_options.add_argument('lang=en-US,en')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if advanced:
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("disable-blink-features=AutomationControlled")
    if proxy:
        chrome_options.add_argument('--proxy-server=%s' % proxy)
    return chrome_options

def get_connection_selenium(proxy=None, advanced=False):
    '''Get connection to Chrome'''
    chrome_options = get_chrome_options(proxy, advanced)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    if advanced:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    return driver

def get_connection(proxy=None, advanced=False, incognito=True, headless=True):
    driver = Driver(uc=True, 
                    incognito=incognito,
                    headless=headless,
                    proxy=proxy,
                    )
    return driver


def run_with_timeout(func, args=(), kwargs={}, timeout=5):
    def wrapper():
        try:
            func(*args, **kwargs)
        except Exception as e:
            raise e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise TimeoutException(f"Function {func.__name__} exceeded the time limit of {timeout} seconds")


def get_page_source(driver, url, minimum_size=0, timeout=15):
    '''Get page source'''
    driver.set_page_load_timeout(timeout)
    driver.set_script_timeout(timeout)
    run_with_timeout(driver.get, args=(url,), timeout=timeout)
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    except TimeoutException:
        print("Timed out waiting for page to load")
        raise EmptyFileException("Empty file")
    page_source = driver.page_source
    size = len(page_source)
    if size <= minimum_size:
        raise EmptyFileException("Empty file")
    return page_source