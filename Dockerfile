FROM python:3.6
ENV PATH /usr/local/bin:$PATH
ADD . /code
WOKDIR /CODE
RUN pip3 install -r requirements.txt
CMD scrapy crawl book 