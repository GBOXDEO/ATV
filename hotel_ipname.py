import random
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
from bs4 import BeautifulSoup
from queue import Queue
import threading

lock = threading.Lock()
# 查找所有符合指定格式的网址
infoList = []
urls_y = []
resultslist = []
urls = [
    "http://tonkiang.us/hoteliptv.php?page=25&s=广东"
    ]
# 初始化计数器为0
counter = -1
 
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter

#判断一个数字是单数还是双数可
def is_odd_or_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)  # 10秒后超时
    # 设置脚本执行超时
    driver.set_script_timeout(50)  # 5秒后超时
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    WebDriverWait(driver, 45).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.tables")
            )
    )
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 关闭WebDriver
    driver.quit()
    print(soup)    #方便看看是否有执行啊
