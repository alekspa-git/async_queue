FROM python:3.9

ADD . /async_queue/
WORKDIR /async_queue/

RUN pip --no-cache-dir -q install --upgrade pip
RUN pip --no-cache-dir -q install -r requirements.txt

