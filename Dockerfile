FROM tiangolo/uwsgi-nginx-flask:python3.6
# File Author / Maintainer
MAINTAINER andeath

# By default, allow unlimited file sizes, modify it to limit the file sizes
# To have a maximum of 1 MB (Nginx's default) change the line to:
# ENV NGINX_MAX_UPLOAD 1m
ENV NGINX_MAX_UPLOAD 0

# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /django_rest/uwsgi.ini

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /django_rest/static
ENV DEBUG True
# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

ENV REDIS_HOST 172.17.0.1

# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Add app
COPY . /django_rest
WORKDIR /django_rest
RUN pip install -r requirements.txt

CMD ["/usr/bin/celery -A django_rest worker -l DEBUG --pool=solo -B &"]
CMD ["/usr/bin/supervisord"]
