FROM alpine

RUN apk add --no-cache uwsgi uwsgi-python3 nginx python3 py3-lxml supervisor && \
    pip3 install wsgidav && \
    mkdir /run/nginx /app

COPY *.conf *.ini *.py /app/

VOLUME /data /ssl
EXPOSE 443

WORKDIR /app
CMD ["/usr/bin/supervisord"]
