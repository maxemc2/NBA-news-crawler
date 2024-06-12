# NBA News Tracker

<p align="left">
  <a href="https://www.djangoproject.com/" alt="django"><img src="https://img.shields.io/badge/django-v4.2.13-blue" /></a>
  <a href="https://www.django-rest-framework.org/" alt="djangorestframework"><img src="https://img.shields.io/badge/djangorestframework-v3.15.1-blue" /></a>
  <a href="https://docs.celeryproject.org/en/stable/" alt="celery"><img src="https://img.shields.io/badge/celery-v5.4.0-yellow" /></a>
  <a href="https://redis.io/" alt="redis"><img src="https://img.shields.io/badge/redis-v5.0.5-green" /></a>
  <a href="https://www.postgresql.org/" alt="postgresql"><img src="https://img.shields.io/badge/postgresql-v13.x.x-purple" /></a>
</p>

### Project Description
This project aims to scrape headline news from the [United Daily News NBA section](http://tw-nba.udn.com/nba/index) and store the retrieved news in PostgreSQL. The front end uses Django REST Framework combined with AJAX to display the headlines list and news detail pages.

## Application Features
- **Scheduled News Crawler**: Scrapes headline news from the United Daily News NBA section.
- **News Storage**: Stores the scraped news in PostgreSQL.
- **Headlines List Page**: Displays a list of recently scraped news.
- **News Detail Page**: Displays the detailed content of the news.

### External API
- **GET /api/news/**: Returns the ten most recent news articles.
- **GET /api/news/<int:pk>/**: Returns the details of a specified news article by ID.

## Installation and Configuration

1. Download the project:
    ```bash
    git clone https://github.com/maxemc2/NBA-news-crawler.git
    cd NBA-news-crawler
    ```

2. Configure the PostgreSQL database settings in `docker-compose.yml` and the corresponding `nba_news_crawler/settings.py`:
    - In the `docker-compose.yml` file:
    ```yaml
    services:
      db:
        image: postgres:latest
        environment:
          POSTGRES_DB: nba_news_db
          POSTGRES_USER: your_user
          POSTGRES_PASSWORD: your_password
        ports:
          - "5432:5432"
    ```
    - In the `nba_news_crawler/settings.py` file:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'nba_news_db',
            'USER': 'your_user',
            'PASSWORD': 'your_password',
            'HOST': 'db',
            'PORT': '5432',
        }
    }
    ```

3. Install Docker and Docker Compose:
    - Docker: [Official Installation Documentation](https://docs.docker.com/get-docker/)
    - Docker Compose: [Official Installation Documentation](https://docs.docker.com/compose/install/)

4. Use `docker-compose` commands to run and stop the application:
    - To run:
    ```bash
    docker-compose up
    ```
    - To stop:
    ```bash
    docker-compose down
    ```

## Package List
- Django==4.2.13
- djangorestframework==3.15.1
- celery==5.4.0
- redis==5.0.5
- psycopg2==2.9.9
- requests==2.32.3

### Overview
- **Django**: Web framework.
- **Django REST Framework**: API framework.
  - **View and API Sharing**: Views are used for both Ajax and API, with the latter converted to JSON via serializers.
- **PostgreSQL**: Database.
- **Celery**: Celery is a distributed task queue that can handle concurrent tasks. When you send a task to Celery, the worker is responsible for pulling and executing these tasks. The beat focuses on scheduling tasks to ensure that periodic tasks are sent on time. The task schedule is set to run every 10 minutes.
- **Redis**: Used to cache frequently used data or query results, with a cache expiry time set to 300 seconds (5 minutes).

### Notes

- **Celery Security**: Celery workers run as the superuser (root). However, it is strongly recommended to run Celery workers as a non-privileged user in a production environment to enhance security.