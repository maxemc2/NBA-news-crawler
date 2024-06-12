from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, re

def get_focus_news():
    # 設定 Chrome 瀏覽器的選項為無頭模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')  # 避免共享內存問題
    chrome_options.binary_location = "/usr/bin/chromium"  # 指定 Chromium 的路徑

    # 設定 Chrome 瀏覽器驅動
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 要抓取的網站 URL
    url = 'https://tw-nba.udn.com/nba/index'

    # 打開頁面
    driver.get(url)

    # 等待頁面加載
    time.sleep(3)  # 根據需要調整等待時間

    # 抓取 XPath 元素
    elements = driver.find_elements(By.XPATH, '//*[@id="splide01-list"]')

    # 初始化字典來存儲結果
    data = {}

    # 遍歷抓取到的元素
    if elements:
        element = elements[0]
        # 獲取所有 <a> 元素
        a_tags = element.find_elements(By.TAG_NAME, 'a')
        
        # 遍歷所有 <a> 元素，將 title 作為 key，href 作為值
        for a_tag in a_tags:
            title = a_tag.get_attribute('title')
            href = a_tag.get_attribute('href')
            if title and href:
                data[title] = href

    # 關閉瀏覽器
    driver.quit()

    return data

def fetch_news_data(url):
    # 設定 Chrome 瀏覽器的選項為無頭模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # 設定 Chrome 瀏覽器驅動
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 打開頁面
    driver.get(url)

    # 等待頁面加載
    time.sleep(3)  # 根據需要調整等待時間

    # 抓取新聞標題
    title_element = driver.find_element(By.XPATH, '//*[@id="story_body_content"]/h1')
    title = title_element.text if title_element else ""

    # 抓取新聞內容和圖片
    span_element = driver.find_element(By.XPATH, '//*[@id="story_body_content"]/span')
    content = ""
    images = []
    image_count = 0

    if span_element:
        # 抓取所有 <p> 元素並合併為內容
        p_elements = span_element.find_elements(By.XPATH, './p')
        content = "\n".join([p.text for p in p_elements])
        content = re.sub(r'\n+', '\n', content)

        # 抓取所有圖片及其描述
        figure_elements = span_element.find_elements(By.XPATH, './figure')
        for figure in figure_elements:
            img = figure.find_element(By.TAG_NAME, 'img')
            img_src = img.get_attribute('src')
            img_caption = ""
            # 嘗試找到 <figcaption> 元素
            figcaption = figure.find_element(By.TAG_NAME, 'figcaption')
            if figcaption:
                img_caption = figcaption.text

            # 查找圖片後面的 <p> 元素，並獲取開頭的 10 個字
            following_text = ""
            if image_count > 0:  # 跳過第一張圖片
                prev_p = figure.find_element(By.XPATH, f'following-sibling::p[normalize-space(text())]')
                following_text = prev_p.text[:10]

            image_count += 1
            images.append({
                'sequence': image_count,
                'src': img_src,
                'caption': img_caption,
                'following_text': following_text,
            })
    # 關閉瀏覽器
    driver.quit()

    return {
        'title': title,
        'content': content,
        'images': images
    }

# 測試函數
# news = get_focus_news()
# for topic, url in news.items():
#     news_data = fetch_news_data(url)
#     print(news_data)