FROM python:3.10-alpine as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /app

RUN apk update && apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    jpeg-dev \
    zlib-dev

COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt


WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

RUN apk add --no-cache libpq jpeg zlib bash

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]