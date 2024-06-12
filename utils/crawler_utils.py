import requests
from bs4 import BeautifulSoup
import re

def get_focus_news():
    # 要抓取的網站 URL
    url = 'https://tw-nba.udn.com/nba/index'

    # 發送 GET 請求獲取頁面內容
    response = requests.get(url)
    response.raise_for_status()  # 確保請求成功

    # 解析頁面內容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 抓取新聞列表元素
    elements = soup.select('.splide__list a')

    # 初始化字典來存儲結果
    data = {}

    # 遍歷抓取到的元素
    for a_tag in elements:
        title = a_tag.get('title')
        href = a_tag.get('href')
        if title and href:
            data[title] = href

    return data

def fetch_news_data(url):
    # 發送 GET 請求獲取頁面內容
    response = requests.get(url)
    response.raise_for_status()  # 確保請求成功

    # 解析頁面內容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 抓取新聞標題
    title_element = soup.select_one('#story_body_content > h1')
    title = title_element.text if title_element else ""

    # 抓取新聞內容和圖片
    span_element = soup.select_one('#story_body_content > span')
    content = ""
    images = []
    image_count = 0

    if span_element:
        # 移除所有類別為 twitter-tweet 的元素及其子元素
        for twitter_tweet in span_element.select('.twitter-tweet'):
            twitter_tweet.decompose()

        # 抓取所有圖片及其描述
        figure_elements = span_element.find_all('figure')
        for figure in figure_elements:
            img = figure.find('img')
            img_src = img.get('src') if img else ""
            img_caption = ""
            # 嘗試找到 <figcaption> 元素
            figcaption = figure.find('figcaption')
            if figcaption:
                img_caption = figcaption.text

            # 查找圖片前面的 <p> 元素，並獲取最後的 10 個字
            following_text = ""
            if image_count > 0:  # 跳過第一張圖片
                prev_p = figure.find_previous_sibling('p')
                while prev_p and not prev_p.text.strip():
                    prev_p = prev_p.find_previous_sibling('p')
                if prev_p:
                    following_text = prev_p.text[:10]

            image_count += 1
            images.append({
                'sequence': image_count,
                'src': img_src,
                'following_text': following_text,
                'caption': img_caption
            })
        
        for figure_element in span_element.find_all('figure'):
            figure_element.decompose()

        # 抓取所有 <p> 元素並合併為內容
        p_elements = span_element.find_all('p', recursive=False)
        content = "\n".join([p.text for p in p_elements])
        content = re.sub(r'\n \n+', '\n', content)

    return {
        'title': title,
        'content': content,
        'images': images
    }

# 測試函數
# url = 'https://tw-nba.udn.com/nba/story/122629/8021748?from=udn_ch2000_menu_v2_main_index'
# news_data = fetch_news_data(url)
# print(news_data)

# 測試函數
# news = get_focus_news()
# for topic, url in news.items():
#     news_data = fetch_news_data(url)
#     print(news_data)