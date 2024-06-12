# 使用官方的Python基礎映像
FROM python:3.9

# 設置工作目錄
WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget gnupg2 && \
    apt-get install -y chromium

# 複製 Pipfile 和 Pipfile.lock
COPY requirements.txt /app/

# 安裝 pipenv 並安裝依賴包
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 複製項目文件
COPY . /app/

# 暴露端口
EXPOSE 8000

# 默認命令
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "nba_news_crawler.asgi:application"]