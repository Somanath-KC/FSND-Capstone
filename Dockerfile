FROM python:3.8.3-alpine3.12

WORKDIR /emagazine

COPY .  /emagazine

RUN pip install --upgrade pip
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

CMD gunicorn src:APP --bind 0.0.0.0:$PORT --reload