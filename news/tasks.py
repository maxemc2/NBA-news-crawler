from celery import shared_task
from django.utils import timezone
# WebSocket
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

from utils.crawler_utils import get_focus_news, fetch_news_data

@shared_task
def fetch_and_store_news():
    from .models import News, NewsImage, UpdateTime
    
    news_list = get_focus_news()
    created_number = 0
    # channel_layer = get_channel_layer()

    for title, url in news_list.items():
        news_data = fetch_news_data(url)
        print(news_data)
        news, created = News.objects.update_or_create(
            title=title,
            url=url,
            defaults={
                'content': news_data['content'],
                'updated_time': timezone.now()
            }
        )
        if created:
            created_number += 1
            for image in news_data['images']:
                NewsImage.objects.create(
                    news=news,
                    url=image['src'],
                    caption=image['caption'],
                    following_text=image['following_text'],
                )
            
            # Notify WebSocket group
            # async_to_sync(channel_layer.group_send)(
            #     'news_group',
            #     {
            #         'type': 'send_news',
            #         'text': {
            #             'id': news.id,
            #             'title': news_data['title'],
            #             'url': url,
            #             'content': news_data['content'],
            #             'images': [{'url': img['src'], 'caption': img['caption']} for img in news_data['images']]
            #         }
            #     }
            # )
        else:
            # 更新已存在新聞的圖片
            news.images.all().delete()
            for image in news_data['images']:
                NewsImage.objects.create(
                    news=news,
                    url=image['src'],
                    caption=image['caption'],
                    following_text=image['following_text'],
                )

    # Add UpdateTime
    UpdateTime.objects.create(
        updated_time=timezone.now(),
        updated_number=created_number
    )
