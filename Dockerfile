FROM python:3.7
 ENV PYTHONUNBUFFERED 1

ADD requirements.txt /requirements.txt

RUN pip3 install --default-timeout=100 -r requirements.txt

ADD . /sparrow_crawl
WORKDIR /sparrow_crawl


EXPOSE 8001