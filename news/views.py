from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import News, UpdateTime
from .serializers import NewsSerializer

def index(request):
    # Attempt to get the latest news from cache
    latest_news = cache.get('latest_news')

    if not latest_news:
        latest_news = News.objects.order_by('-updated_time')[:10]
        # Store the news in cache for 5 minutes
        cache.set('latest_news', latest_news, timeout=300)

    # Attempt to get the latest update time from cache
    latest_update = cache.get('latest_update')

    if not latest_update:
        latest_update = UpdateTime.objects.order_by('-updated_time').first()
        # Store the latest update time in cache for 5 minutes
        cache.set('latest_update', latest_update, timeout=300)

    context = {
        'latest_news': latest_news,
        'latest_update': latest_update
    }
    return render(request, 'index.html', context)

def news_detail(request, news_id):
    cache_key = f'news_{news_id}'
    news = cache.get(cache_key)

    if not news:
        news = get_object_or_404(News, id=news_id)
        # Store the news in cache for 5 minutes
        cache.set(cache_key, news, timeout=300)

    images = news.images.all()
    content_paragraphs = news.content.split('\n')

    # Attempt to get the latest update time from cache
    latest_update = cache.get('latest_update')

    if not latest_update:
        latest_update = UpdateTime.objects.order_by('-updated_time').first()
        # Store the latest update time in cache for 5 minutes
        cache.set('latest_update', latest_update, timeout=300)

    context = {
        'news': news,
        'images': images,
        'content_paragraphs': content_paragraphs,
        'latest_update': latest_update
    }
    return render(request, 'news_detail.html', context)

# Retrieve the latest ten news
class NewsListAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        # Attempt to get the latest news from cache
        latest_news = cache.get('latest_news')

        if not latest_news:
            latest_news = News.objects.order_by('-updated_time')[:10]
            # Store the news in cache for 5 minutes
            cache.set('latest_news', latest_news, timeout=300)

        return latest_news

# Retrieve details of a specific news by ID
@api_view(['GET'])
def news_detail_api(request, news_id):
    cache_key = f'news_{news_id}'
    news_data = cache.get(cache_key)

    if not news_data:
        news = get_object_or_404(News, id=news_id)
        images = news.images.all()
        content_paragraphs = news.content.split('\n')

        news_data = NewsSerializer(news).data
        images_data = [image.url for image in images]

        news_data['images'] = images_data
        news_data['content_paragraphs'] = content_paragraphs
        # Store the news details in cache for 5 minutes
        cache.set(cache_key, news_data, timeout=300)

    return Response(news_data)
