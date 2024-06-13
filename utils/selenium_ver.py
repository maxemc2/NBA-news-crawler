from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, re

def get_focus_news():
    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = "/usr/bin/chromium"

    # Set up Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = 'https://tw-nba.udn.com/nba/index'
    driver.get(url)
    time.sleep(3)

    elements = driver.find_elements(By.XPATH, '//*[@id="splide01-list"]')
    data = {}

    if elements:
        element = elements[0]
        # Get all <a> elements
        a_tags = element.find_elements(By.TAG_NAME, 'a')
        
        # Store titles and hrefs in the dictionary
        for a_tag in a_tags:
            title = a_tag.get_attribute('title')
            href = a_tag.get_attribute('href')
            if title and href:
                data[title] = href

    driver.quit()

    return data

def fetch_news_data(url):
    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # Set up Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(3)

    # Fetch news title
    title_element = driver.find_element(By.XPATH, '//*[@id="story_body_content"]/h1')
    title = title_element.text if title_element else ""

    # Fetch news content and images
    span_element = driver.find_element(By.XPATH, '//*[@id="story_body_content"]/span')
    content = ""
    images = []
    image_count = 0

    if span_element:
        # Get all <p> elements and combine as content
        p_elements = span_element.find_elements(By.XPATH, './p')
        content = "\n".join([p.text for p in p_elements])
        content = re.sub(r'\n+', '\n', content)

        # Get all images and their captions
        figure_elements = span_element.find_elements(By.XPATH, './figure')
        for figure in figure_elements:
            img = figure.find_element(By.TAG_NAME, 'img')
            img_src = img.get_attribute('src')
            img_caption = ""
            # Try to find <figcaption> element
            figcaption = figure.find_element(By.TAG_NAME, 'figcaption')
            if figcaption:
                img_caption = figcaption.text

            # Find <p> element after image and get the first 10 characters
            following_text = ""
            if image_count > 0:  # Skip the first image
                prev_p = figure.find_element(By.XPATH, f'following-sibling::p[normalize-space(text())]')
                following_text = prev_p.text[:10]

            image_count += 1
            images.append({
                'sequence': image_count,
                'src': img_src,
                'caption': img_caption,
                'following_text': following_text,
            })
    driver.quit()

    return {
        'title': title,
        'content': content,
        'images': images
    }

# Test functions
# news = get_focus_news()
# for topic, url in news.items():
#     news_data = fetch_news_data(url)
#     print(news_data)
