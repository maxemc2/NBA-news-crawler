from django.db import models
import uuid

class UpdateTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    updated_time = models.DateTimeField()
    updated_number = models.IntegerField(default=0)

    def __str__(self):
        return self.updated_time

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    url = models.URLField()
    content = models.TextField()
    updated_time = models.DateTimeField()

    def __str__(self):
        return self.title

class NewsImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    url = models.URLField()
    caption = models.TextField(null=True, blank=True)
    following_text = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return f"Image for {self.news.title}"
