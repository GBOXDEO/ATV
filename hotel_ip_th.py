import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from concurrent.futures import ThreadPoolExecutor

import time
import os
import re
from bs4 import BeautifulSoup
import requests

# 查找所有符合指定格式的网址
infoList = []
urls_y = []
resultslist = []
urls = [
    "http://27.41.249.1:801",
    "http://27.41.248.1:801",
    "http://183.239.193.1:2223",
    "http://183.17.224.1:8888",
    "http://183.238.248.1:9000"
    ]

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = ""
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{modified_ip}{port}"
        modified_urls.append(modified_url)
    return modified_urls

def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.4)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    # return None
    return url
# 初始化计数器为0
counter = 0
 
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter

valid_urls = []
#   多线程获取可用url
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for ipv in urls:
        url = ipv.strip()
        modified_urls = modify_urls(url)
        for modified_url in modified_urls:
            futures.append(executor.submit(is_url_accessible, modified_url))

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            valid_urls.append(result)

resultslist = set(valid_urls)    # 去重得到唯一的URL列表
with open("iplist.txt", 'w', encoding='utf-8') as file:
    for iplist in resultslist:
        file.write(iplist + "\n")
        print(iplist)
    file.close()
    
sorted_list = sorted(resultslist)
#多线程并发查询url并获取数据

 
def open_url(ipv):
    try:
        # 创建一个Chrome WebDriver实例
        results = []
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("blink-settings=imagesEnabled=false")
        driver = webdriver.Chrome(options=chrome_options)
        # 设置页面加载超时
        driver.set_page_load_timeout(15)  # 10秒后超时
 
        # 设置脚本执行超时
        driver.set_script_timeout(10)  # 5秒后超时
        # 使用WebDriver访问网页
        page_url= f"http://foodieguide.com/iptvsearch/alllist.php?s={ipv}"
        print(page_url)
        driver.get(page_url)  # 将网址替换为你要访问的网页地址
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tables")
                )
        )
        time.sleep(15)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # 关闭WebDriver
        # driver.quit()
        tables_div = soup.find("div", class_="tables")
        results = (
            tables_div.find_all("div", class_="result")
            if tables_div
            else []
        )
        if not any(
            result.find("div", class_="m3u8") for result in results
        ):
            #break
            print("Err-------------------------------------------------------------------------------------------------------")
        for result in results:
            #print(result)
            m3u8_div = result.find("div", class_="m3u8")
            url_int = m3u8_div.text.strip() if m3u8_div else None
            #取频道名称
            m3u8_name_div = result.find("div", class_="channel")
            url_name = m3u8_name_div.text.strip() if m3u8_div else None
            #－－－－－
            #print("-------------------------------------------------------------------------------------------------------")
            name =f"{url_name}"
            if len(name) == 0:
                name = "Err画中画"
            #print(name)
            urlsp =f"{url_int}"
            if len(urlsp) == 0:
                urlsp = "rtp://127.0.0.1"             
            print(f"{url_name}\t{url_int}")
            #print("-------------------------------------------------------------------------------------------------------")
            urlsp = urlsp.replace("http://67.211.73.118:9901", "")
            name = name.replace("cctv", "CCTV")
            name = name.replace("中央", "CCTV")
            name = name.replace("央视", "CCTV")
            name = name.replace("高清", "")
            name = name.replace("超高", "")
            name = name.replace("HD", "")
            name = name.replace("标清", "")
            name = name.replace("频道", "")
            name = name.replace("-", "")
            name = name.replace(" ", "")
            name = name.replace("PLUS", "+")
            name = name.replace("＋", "+")
            name = name.replace("(", "")
            name = name.replace(")", "")
            name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
            name = name.replace("CCTV1综合", "CCTV1")
            name = name.replace("CCTV2财经", "CCTV2")
            name = name.replace("CCTV3综艺", "CCTV3")
            name = name.replace("CCTV4国际", "CCTV4")
            name = name.replace("CCTV4中文国际", "CCTV4")
            name = name.replace("CCTV4欧洲", "CCTV4")
            name = name.replace("CCTV5体育", "CCTV5")
            name = name.replace("CCTV6电影", "CCTV6")
            name = name.replace("CCTV7军事", "CCTV7")
            name = name.replace("CCTV7军农", "CCTV7")
            name = name.replace("CCTV7农业", "CCTV7")
            name = name.replace("CCTV7国防军事", "CCTV7")
            name = name.replace("CCTV8电视剧", "CCTV8")
            name = name.replace("CCTV9记录", "CCTV9")
            name = name.replace("CCTV9纪录", "CCTV9")
            name = name.replace("CCTV10科教", "CCTV10")
            name = name.replace("CCTV11戏曲", "CCTV11")
            name = name.replace("CCTV12社会与法", "CCTV12")
            name = name.replace("CCTV13新闻", "CCTV13")
            name = name.replace("CCTV新闻", "CCTV13")
            name = name.replace("CCTV14少儿", "CCTV14")
            name = name.replace("CCTV15音乐", "CCTV15")
            name = name.replace("CCTV16奥林匹克", "CCTV16")
            name = name.replace("CCTV17农业农村", "CCTV17")
            name = name.replace("CCTV17农业", "CCTV17")
            name = name.replace("CCTV5+体育赛视", "CCTV5+")
            name = name.replace("CCTV5+体育赛事", "CCTV5+")
            name = name.replace("CCTV5+体育", "CCTV5+")
            name = name.replace("CMIPTV", "")
            name = name.replace("台", "")
            name = name.replace("内蒙卫视", "内蒙古卫视")
            infoList.append(f"{name},{urlsp}")
    except:
        continue
    
    driver.quit()  # 关闭浏览器
 
max_workers = 15  # 你想要限制的线程数量
 
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(open_url, sorted_list)

infoList = set(infoList)  # 去重得到唯一的URL列表
infoList = sorted(infoList)

with open("myitv.txt", 'w', encoding='utf-8') as file:
    for info in infoList:
        file.write(info + "\n")
        print(info)
    file.close()
