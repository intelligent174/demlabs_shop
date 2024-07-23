FROM redis:latest

WORKDIR /redis

COPY ../../redis.conf /usr/local/etc/redis/redis.conf
COPY docker/redis/init.sh ./

RUN chmod +x init.sh
