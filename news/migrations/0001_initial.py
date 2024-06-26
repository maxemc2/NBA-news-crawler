# Generated by Django 4.2.13 on 2024-06-11 15:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('content', models.TextField()),
                ('updated_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UpdateTime',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('updated_time', models.DateTimeField()),
                ('updated_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='NewsImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('url', models.URLField()),
                ('caption', models.TextField(blank=True, null=True)),
                ('following_text', models.CharField(blank=True, max_length=100, null=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='news.news')),
            ],
        ),
    ]
