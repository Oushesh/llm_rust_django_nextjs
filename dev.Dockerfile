# syntax=docker/dockerfile:1
FROM python:3.8.9
ARG PORT=8000
LABEL maintainer="oushesh"
ENV PYTHONUNBUFFERED 1

WORKDIR /django_ifc_ai_new
COPY requirements.txt /django_ifc_ai_new/

RUN apt update && \
	apt install build-essential && \
	rm -rf /var/cache/apk/* && \
	pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt

COPY . /django_ifc_ai_new/

RUN chmod a+x /django_ifc_ai_new/dev-docker-entrypoint.sh
ENTRYPOINT ["/django_ifc_ai_new/dev-docker-entrypoint.sh"]