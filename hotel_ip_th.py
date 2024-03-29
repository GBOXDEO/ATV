import random
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from queue import Queue
import threading
from concurrent.futures import ThreadPoolExecutor

import time
import os
import re
from bs4 import BeautifulSoup
import requests

lock = threading.Lock()
now_today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
guangdong_text = "东莞中山佛山顺德南海宝安岭南广东广州广视揭西揭阳汕头汕尾江门海豚深圳清远龙岗湛江潮州珠江粤语肇庆茂名韶关南方"
# 查找所有符合指定格式的网址
infoList = []
urls_y = []
resultslist = []
# 线程安全的队列，用于存储下载任务
task_queue = Queue()

def cut_first_chinese_words(text, num=2):
    for i, char in enumerate(text):
        if char >= '\u4e00' and char <= '\u9fa5':
            return text[:i+2]
    return 'xxxxxxxxxxxxxxxxxx'
    
#判断一个数字是单数还是双数可
def is_odd_or_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

urls = [
    "http://27.41.249.1:801",
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
    for i in range(1, 255):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{modified_ip}{port}"
        modified_urls.append(modified_url)
    return modified_urls

def is_url_accessible(url):
    try:
        return url
    except requests.exceptions.RequestException:
        pass
    # return None
    return url
# 初始化计数器为0
counter = -1
 
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
            
sorted_list = set(valid_urls)    # 去重得到唯一的URL列表
resultslist = sorted(sorted_list)

with open("iplist.txt", 'w', encoding='utf-8') as file:
    for iplist in resultslist:
        file.write(iplist + "\n")
        print(iplist)
    file.write(f"{now_today}更新IP组\n")
    file.close()

#多线程并发查询url并获取数据

def worker(thread_url,counter_id):
    try:
        # 创建一个Chrome WebDriver实例
        results = []
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir=selenium{counter_id}")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("blink-settings=imagesEnabled=false")
        driver = webdriver.Chrome(options=chrome_options)
        # 设置页面加载超时
        driver.set_page_load_timeout(90)  # 10秒后超时
     
        # 设置脚本执行超时
        driver.set_script_timeout(80)  # 5秒后超时
        # 使用WebDriver访问网页
        # 取自身线程ID
        if is_odd_or_even(random.randint(1, 200)):
            page_url= f"http://tonkiang.us/9dlist2.php?s={thread_url}"
        else:
            page_url= f"http://foodieguide.com/iptvsearch/alllist.php?s={thread_url}"
        print(page_url)
        driver.get(page_url)  # 将网址替换为你要访问的网页地址
        # 为每个线程创建独立的 WebDriverWait 实例
        WebDriverWait(driver, 75).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tables")
                )
        )
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
            # break
            print("Err-------------------------------------------------------------------------------------------------------")
            result_break = 10 / 0
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
            #print(name)
            urlsp =f"{url_int}"        
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
            name = name.replace("_", "")
            name = name.replace("HD", "")
            name = name.replace("(高清)", "")
            name = name.replace("超清", "")
            name = name.replace("厦门卫视高清", "厦门卫视")
            name = name.replace("吉林卫视高清", "吉林卫视")
            name = name.replace("四川卫视高清", "四川卫视")
            name = name.replace("天津卫视高清", "天津卫视")
            name = name.replace("天津高清", "天津卫视")
            name = name.replace("安徽卫视高清", "安徽卫视")
            name = name.replace("广东卫视高清", "广东卫视")
            name = name.replace("广东高清", "广东卫视")
            name = name.replace("江苏卫视高清", "江苏卫视")
            name = name.replace("河北卫视高清", "河北卫视")
            name = name.replace("浙江卫视高清", "浙江卫视")
            name = name.replace("深圳高清", "深圳卫视")
            name = name.replace("深圳卫视高清", "深圳卫视")
            name = name.replace("湖北卫视高清", "湖北卫视")
            name = name.replace("湖北高清", "湖北卫视")
            name = name.replace("湖南卫视高清", "湖南卫视")
            name = name.replace("湖南高清", "湖南卫视")
            name = name.replace("福建东南卫视高清", "福建东南卫视")
            name = name.replace("辽宁卫视高清", "辽宁卫视")
            name = name.replace("黑龙江卫视高清", "黑龙江卫视")
            name = name.replace("山东教育", "山东教育卫视")
            name = name.replace("山东高清", "山东卫视")
            name = name.replace("广东体育高清", "广东体育卫视")
            name = name.replace("广东珠江高清", "广东珠江卫视")
            name = name.replace("广东高清", "广东卫视")
            name = name.replace("浙江高清", "浙江卫视")
            name = name.replace("深圳高清", "深圳卫视")
            name = name.replace("湖北高清", "湖北卫视")
            name = name.replace("湖南高清", "湖南卫视")
            name = name.replace("江苏高清", "江苏卫视")
            name = name.replace("北京卫视高清", "北京卫视")
            name = name.replace("北京高清", "北京卫视")
            name = name.replace("福建东南卫视", "东南卫视")
            name = name.replace("汕头综合高清", "汕头综合")
            name = name.replace("汕头文旅体育高清", "汕头文旅体育")
            name = name.replace("汕头文旅体育高清", "汕头文旅体育")
            name = name.replace("高清", "")
            name = name.replace("凤凰中文", "凤凰卫视中文")
            name = name.replace("凤凰资讯", "凤凰卫视资讯")
            name = name.replace("凤凰香港", "凤凰香港卫视")
            name = name.replace("本港", "本港卫视")
            name = name.replace("香港明珠", "香港明珠卫视")
            name = name.replace("香港翡翠", "香港翡翠卫视")
            name = name.replace("香港音乐", "香港音乐卫视")
            name = name.replace("高请", "")
            name = name.replace("超", "")
            name = name.replace("汕头二台", "汕头经济生活")
            name = name.replace("汕头二", "汕头经济生活")
            name = name.replace("汕头一台", "汕头综合")
            name = name.replace("汕头一", "汕头综合")
            name = name.replace("汕头三台", "汕头文旅体育")
            name = name.replace("汕头台", "汕头综合")
            name = name.replace("汕头生活", "汕头经济生活")
            name = name.replace("CCTV8电视", "CCTV8")
            name = name.replace("CCTVCCTV", "CCTV")
            if "http" in urlsp:
                # 获取锁
                lock.acquire()
                infoList.append(f"{name},{urlsp}")
                # 释放锁
                lock.release()
        print(f"=========================>>> Thread {thread_url} save ok")
    except Exception as e:
        print(f"=========================>>> Thread {thread_url} caught an exception: {e}")
    finally:
        # 确保线程结束时关闭WebDriver实例
        driver.quit() 
        print(f"=========================>>> Thread {thread_url}  quiting")
        # 标记任务完成
        time.sleep(0)


# 创建一个线程池，限制最大线程数为3
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # 提交任务到线程池，并传入参数
    counter = increment_counter()
    for i in sorted_list:  # 假设有5个任务需要执行
        executor.submit(worker, i ,counter)

# 对频道进行排序
infoList = set(infoList)  # 去重得到唯一的URL列表
infoList = sorted(infoList)

with open("myitv.txt", 'w', encoding='utf-8') as file:
    for info in infoList:
        file.write(info + "\n")
        print(info)
    file.close()

result_counter = 8  # 每个频道需要的个数
with open("cctv.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  央视频道  】,#genre#\n')
    for info in infoList:
        channel_name, channel_url = info.split(',')
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.close()
    
with open("weishi.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  卫视频道  】,#genre#\n')
    for info in infoList:
        channel_name, channel_url = info.split(',')
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.close()

with open("ktpd.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  卡通频道  】,#genre#\n')
    for info in infoList:
        channel_name, channel_url = info.split(',')
        if '卡通' in channel_name or '动漫' in channel_name or '动画' in channel_name or '少儿' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.close()

with open("ysyl.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  影视频道  】,#genre#\n')
    for info in infoList:
        channel_name, channel_url = info.split(',')
        if '电影' in channel_name or '影院' in channel_name or '剧场' in channel_name or '影视' in channel_name or '戏曲' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.close()

with open("qita.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  广东频道  】,#genre#\n')
    for info in infoList:
        channel_name, channel_url = info.split(',')
        if '卫视' not in channel_name and 'CCTV' not in channel_name and '测试' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '剧场' not in channel_name and '影视' not in channel_name and '卡通' not in channel_name and '动漫' not in channel_name and '动画' not in channel_name and '少儿' not in channel_name:
            if cut_first_chinese_words(channel_name) in guangdong_text:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= result_counter:
                        continue
                    else:
                        file.write(f"{channel_name},{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] = 1
    # 写入其他频道
    channel_counters = {}
    file.write('【  其他频道  】,#genre#\n')
    for info in infoList:
        channel_name, channel_url = info.split(',')
        if '戏曲' not in channel_name and '卫视' not in channel_name and 'CCTV' not in channel_name and '测试' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '剧场' not in channel_name and '影视' not in channel_name and '卡通' not in channel_name and '动漫' not in channel_name and '动画' not in channel_name and '少儿' not in channel_name:
            if cut_first_chinese_words(channel_name) not in guangdong_text:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= result_counter:
                        continue
                    else:
                        file.write(f"{channel_name},{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] = 1
    file.close()                

# 合并文件内容
file_contents = []
file_paths = ["cctv.txt", "weishi.txt", "ktpd.txt", "ysyl.txt","xiangang.txt", "qita.txt", "IPV6.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
        file.close()

# print(f"{now_today}合并文件完成")

# 写入合并后的文件
with open("itvlist.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
    output.close()
