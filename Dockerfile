FROM python:3.6

# File Author / Maintainer
MAINTAINER andeath
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    build-essential\
    tcl\
	python3-pip \
	nginx \
	supervisor \
	sqlite3 && \
	pip3 install -U pip setuptools && \
   rm -rf /var/lib/apt/lists/*
# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

# Install basic applications
#RUN apt-get install -y vim tar git curl nano wget net-tools build-essential telnet openssh-client less netcat nmap
RUN apt-get install curl

# Install python git libraries
#RUN pip install gitdb
#RUN pip install nose
#RUN pip install -U mock
#RUN pip install gitpython

# Install django
RUN pip install django
RUN pip install djangorestframework

# Install redis, celery

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y redis-server \
 && sed 's/^daemonize yes/daemonize no/' -i /etc/redis/redis.conf \
 && sed 's/^bind 127.0.0.1/bind 0.0.0.0/' -i /etc/redis/redis.conf \
 && sed 's/^# unixsocket /unixsocket /' -i /etc/redis/redis.conf \
 && sed 's/^# unixsocketperm 755/unixsocketperm 777/' -i /etc/redis/redis.conf \
 && sed '/^logfile/d' -i /etc/redis/redis.conf \
 && rm -rf /var/lib/apt/lists/*

#RUN service redis-server start &
RUN pip install celery[redis]
RUN pip install django-celery-results


# By default, allow unlimited file sizes, modify it to limit the file sizes
# To have a maximum of 1 MB (Nginx's default) change the line to:
# ENV NGINX_MAX_UPLOAD 1m
ENV NGINX_MAX_UPLOAD 0

# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /app/uwsgi.ini

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /app/static

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# Install Ansible
#
#RUN echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" >>  /etc/apt/sources.list
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
#RUN apt-get update
#RUN apt-get install -y ansible
#RUN pip install ansible

# Install ntc-ansible
#RUN perl -pi -e 's/#inventory/inventory/g' /etc/ansible/ansible.cfg
#RUN perl -pi -e 's/#library/library/g' /etc/ansible/ansible.cfg
#RUN mkdir -p /usr/share/my_modules/
#RUN cd /usr/share/my_modules/ && git clone https://github.com/networktocode/ntc-ansible --recursive
#RUN pip install jtextfsm
#RUN pip install terminal
#RUN 2to3 -w /usr/local/lib/python3.6/site-packages/texttable.py

# Install django-netjsongraph
#RUN pip install django-netjsongraph

# Install dateutils
#RUN pip install python-dateutil

ENTRYPOINT ["/entrypoint.sh"]

# Add django
COPY ./* /django_rest/

WORKDIR /django_rest

RUN pip install -r requirements.txt
#RUN service redis-server start &
#RUN celery -A django_rest &
EXPOSE 80

CMD ["/usr/bin/supervisord"]

