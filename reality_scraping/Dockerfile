FROM python:3.9.2
WORKDIR /app
ADD requirements.txt /app
ADD scrapy.cfg /app
RUN pip install pip==22.1.2
RUN pip install -r requirements.txt
RUN mkdir -p /app/reality_scraping
COPY reality_scraping /app/reality_scraping
CMD ["python", "reality_scraping/go_spider.py"]
