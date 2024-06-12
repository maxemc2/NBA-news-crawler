from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/<uuid:news_id>/', views.news_detail, name='news_detail'),
    path('api/news/', views.NewsListAPIView.as_view(), name='news-list-api'),
    path('api/news/<uuid:news_id>/', views.news_detail_api, name='news-detail-api'),
]
