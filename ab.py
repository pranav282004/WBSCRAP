from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import csv
import time
import mysql.connector
import socket
import re
from tkinter import messagebox
import threading
import requests
from selenium.webdriver.common.by import By
import concurrent.futures
from fake_useragent import UserAgent



def fetching():
    proxies = {
        'http': 'http://gate.smartproxy.com:7000',
        'https': 'http://gate.smartproxy.com:7000',
        'ssl': 'http://gate.smartproxy.com:7000'}
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.headless = False
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(
            f'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id=44596321012&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all')
        print('Fetching Data From Links...')
        time.sleep(40)
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'lxml')
        contentf = soup.find_all('div', class_='x8t9es0 x1uxerd5 xrohxju x108nfp6 xq9mrsl x1h4wwuj x117nqv4 xeuugli')
        driver.quit()
    except:
        driver.quit()



fetching()
   
