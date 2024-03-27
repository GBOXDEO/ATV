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
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B1%9F%E8%8B%8F",
    "http://tonkiang.us/hoteliptv.php?page=2&s=%E6%B1%9F%E8%8B%8F",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E9%A6%99%E6%B8%AF",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E9%9D%92%E6%B5%B7",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E7%94%98%E8%82%83",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E9%99%95%E8%A5%BF",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E4%BA%91%E5%8D%97",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E8%B4%B5%E5%B7%9E",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%9B%9B%E5%B7%9D",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B5%B7%E5%8D%97",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%B9%BF%E4%B8%9C",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B9%96%E5%8D%97",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B9%96%E5%8C%97",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B2%B3%E5%8D%97",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%B1%B1%E4%B8%9C",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B1%9F%E8%A5%BF",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E7%A6%8F%E5%BB%BA",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%AE%89%E5%BE%BD",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B5%99%E6%B1%9F",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E9%BB%91%E9%BE%99%E6%B1%9F",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%90%89%E6%9E%97",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E8%BE%BD%E5%AE%81",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%B1%B1%E8%A5%BF",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B2%B3%E5%8C%97",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E4%B8%8A%E6%B5%B7",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E4%B8%9C%E6%B5%B7%E6%96%B0%E9%97%BB",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%8D%97%E4%BA%AC",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%93%8D%E6%B0%B4",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%AE%BF%E8%BF%81",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%B8%B8%E5%B7%9E",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%BE%90%E5%B7%9E",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B1%9F%E8%8B%8F%E4%BD%93%E8%82%B2",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B2%9B%E5%8E%BF",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B3%97%E6%B4%AA",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B3%B0%E5%B7%9E",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B7%AE%E5%AE%89",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E7%9D%A2%E5%AE%81",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E8%B5%A3%E6%A6%86",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E8%BF%9E%E4%BA%91",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E9%AB%98%E6%B7%B3"
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
        driver.set_page_load_timeout(90)  # 10秒后超时
        # 设置脚本执行超时
        driver.set_script_timeout(80)  # 5秒后超时
        # 使用WebDriver访问网页
        driver.get(url)  # 将网址替换为你要访问的网页地址
        WebDriverWait(driver, 75).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tables")
                )
        )
        time.sleep(20)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    
        # 关闭WebDriver
        driver.quit()
        tables_div = soup.find("div", class_="tables")
        results = (
            tables_div.find_all("div", class_="result")
            if tables_div
            else []
        )
        if not any(
            result.find("div", class_="channel") for result in results
        ):
            #break
            print("Err-------------------------------------------------------------------------------------------------------")
        for result in results:
            # print("============================================================================================================")
            # print(result)
            html_txt = f"{result}"
            # print(html_txt)
            if "result" in html_txt:
                m3u8_div = result.find("a")
                if m3u8_div:
                    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
                    urls_all = re.findall(pattern, m3u8_div.get('href'))
                    # print(urls_all)
                    if len(urls_all) > 0:
                        ip = urls_all[0]
                        italic_tags = soup.find_all('i')
                        # 尝试获取第二个<i>标签
                        if len(italic_tags) > 1:
                            second_italic_tag = italic_tags[1]  # 索引从0开始，所以第二个标签的索引是1
                            url_name = second_italic_tag.text
                            name_html_txt = f"{url_name}"
                            if "移动" in html_txt:
                                ipname = '移动'
                            elif "联通" in html_txt:
                                ipname = '联通'
                            elif "电信" in html_txt:
                                ipname = '电信'
                            else:
                                ipname ='其他'
                            resultslist.append(f"{ipname},{ip}")
    except:
        print(f"=========================>>> Thread {url} error")
        
resultslist = set(resultslist)    # 去重得到唯一的URL列表

with open("iplist.txt", 'w', encoding='utf-8') as file:
    for iplist in resultslist:
        file.write(iplist + "\n")
        print(iplist)
    file.close()
sorted_list = sorted(resultslist)

def worker(thread_url,counter_id):
    try:
        # 创建一个Chrome WebDriver实例
        results = []
        #分离出运营商和IP
        in_name,in_url = thread_url.split(',')
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir=selenium{counter_id}")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("blink-settings=imagesEnabled=false")
        driver = webdriver.Chrome(options=chrome_options)
        # 设置页面加载超时
        driver.set_page_load_timeout(60)  # 10秒后超时
     
        # 设置脚本执行超时
        driver.set_script_timeout(50)  # 5秒后超时
        # 使用WebDriver访问网页
        if is_odd_or_even(random.randint(1, 200)):
            page_url= f"http://tonkiang.us/9dlist2.php?s={in_url}"
        else:
            page_url= f"http://foodieguide.com/iptvsearch/alllist.php?s={in_url}"
        
        print(page_url)
        driver.get(page_url)  # 将网址替换为你要访问的网页地址
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tables")
                )
        )
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
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
            name = name.replace("HD", "高清")
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
            name = name.replace("内蒙卫视", "内蒙古卫视")
            name = name.replace("CCTVCCTV", "CCTV")
            if "http" in urlsp:
                # 获取锁
                lock.acquire()
                infoList.append(f"{name}_{in_name},{urlsp}")
                # 释放锁
                lock.release()
        print(f"=========================>>> Thread {in_url} save ok")
    except Exception as e:
        print(f"=========================>>> Thread {in_url} caught an exception: {e}")
    finally:
        # 确保线程结束时关闭WebDriver实例
        driver.quit() 
        print(f"=========================>>> Thread {in_url}  quiting")
        # 标记任务完成
        time.sleep(0)

# 创建一个线程池，限制最大线程数为3
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # 提交任务到线程池，并传入参数
    counter = increment_counter()
    for i in sorted_list:  # 假设有5个任务需要执行
        executor.submit(worker, i ,counter)

infoList = set(infoList)  # 去重得到唯一的URL列表
infoList = sorted(infoList)

with open("myitv.txt", 'w', encoding='utf-8') as file:
    for info in infoList:
        file.write(info + "\n")
        print(info)
    file.close()
