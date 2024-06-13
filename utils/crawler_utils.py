import requests
from bs4 import BeautifulSoup
import re

def get_focus_news():
    # Target website URL
    url = 'https://tw-nba.udn.com/nba/index'
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    soup = BeautifulSoup(response.content, 'html.parser')
    # Fetch all <a> elements in news list elements
    elements = soup.select('.splide__list a')
    data = {}

    # Store titles and hrefs in the dictionary
    for a_tag in elements:
        title = a_tag.get('title')
        href = a_tag.get('href')
        if title and href:
            data[title] = href

    return data

def fetch_news_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    soup = BeautifulSoup(response.content, 'html.parser')

    # Fetch news title
    title_element = soup.select_one('#story_body_content > h1')
    title = title_element.text if title_element else ""

    # Fetch news content and images
    span_element = soup.select_one('#story_body_content > span')
    content = ""
    images = []
    image_count = 0

    if span_element:
        # Remove all elements with the class 'twitter-tweet'
        for twitter_tweet in span_element.select('.twitter-tweet'):
            twitter_tweet.decompose()

        # Fetch all images and their captions
        figure_elements = span_element.find_all('figure')
        for figure in figure_elements:
            img = figure.find('img')
            img_src = img.get('src') if img else ""
            img_caption = ""
            # Try to find <figcaption> element
            figcaption = figure.find('figcaption')
            if figcaption:
                img_caption = figcaption.text

            # Find <p> element before the image and get the first 10 characters
            following_text = ""
            if image_count > 0:  # Skip the first image
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

        # Fetch all <p> elements and combine as content
        p_elements = span_element.find_all('p', recursive=False)
        content = "\n".join([p.text for p in p_elements])
        content = re.sub(r'\n \n+', '\n', content)

    return {
        'title': title,
        'content': content,
        'images': images
    }

# Test functions
# url = 'https://tw-nba.udn.com/nba/story/122629/8021748?from=udn_ch2000_menu_v2_main_index'
# news_data = fetch_news_data(url)
# print(news_data)

# Test functions
# news = get_focus_news()
# for topic, url in news.items():
#     news_data = fetch_news_data(url)
#     print(news_data)
