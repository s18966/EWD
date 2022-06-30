FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk add --update --no-cache python3 gcc libc-dev linux-headers\
&& apk add libffi-dev \
&& python3 -m ensurepip && \
pip3 install --no-cache --upgrade pip setuptools

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /usr/src/app/

RUN adduser -D selenium

USER selenium

CMD ["python3", "scrap_for_cloud.py"]