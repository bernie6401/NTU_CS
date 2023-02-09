FROM php:fpm

# RUN apt-get update
# RUN apt-get install -y nodejs
# RUN apt-get install -y build-essential openssl openssl-dev* wget curl && \
# wget https://www.python.org/ftp/python/3.7.8/Python-3.7.8.tgz && \
# tar -xvf Python-3.7.8.tgz && \
# cd Python-3.7.8 && \
# ./configure --enable-shared && \
# make  && \
# make test && \
# make install && \
# cd /usr/local/lib/ && \
# cp libpython3.so /usr/lib64/ && \
# cp libpython3.so /usr/lib && \
# cp libpython3.7m.so.1.0 /usr/lib64/ && \
# cp libpython3.7m.so.1.0 /usr/lib/ && \
# cd /usr/lib64 && \
# ln -s libpython3.7m.so.1.0 libpython3.7m.so && \
# cd /usr/lib && \
# ln -s libpython3.7m.so.1.0 libpython3.7m.so

RUN chmod 555 /var/www/html
RUN chown root:root /var/www/html
