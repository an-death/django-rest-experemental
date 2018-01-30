#!/bin/bash
set -e
# Get the maximum upload file size for Nginx, default to 0: unlimited
USE_NGINX_MAX_UPLOAD=${NGINX_MAX_UPLOAD:-0}
# Generate Nginx config for maximum upload file size
echo "client_max_body_size $USE_NGINX_MAX_UPLOAD;" > /etc/nginx/conf.d/upload.conf

# Get the URL for static files from the environment variable
USE_STATIC_URL=${STATIC_URL:-'/static'}
# Get the absolute path of the static files from the environment variable
USE_STATIC_PATH=${STATIC_PATH:-'/app/static'}

# Generate Nginx config first part using the environment variables
echo '
server {
    listen  80;
    server_name localhost;
    charset utf-8;

    location / {
#        try_files $uri @app;
	    proxy_connect_timeout       600000;
        proxy_send_timeout          600000;
        proxy_read_timeout          600000;
	    keepalive_timeout 	        600000;
        send_timeout                600000;
#    }
#    location @app {
	uwsgi_read_timeout      7500;
	uwsgi_send_timeout      7500;
	uwsgi_connect_timeout   7500;
        fastcgi_read_timeout 300000;
        include uwsgi_params;
        uwsgi_pass  unix:/django_rest/django_rest/django_rest.sock;
    }
    '"location $USE_STATIC_URL {
        alias $USE_STATIC_PATH;
    }" > /etc/nginx/conf.d/nginx.conf

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
if [[ $STATIC_INDEX == 1 ]] ; then
echo "    location = / {
        index $USE_STATIC_URL/index.html;
    }" >> /etc/nginx/conf.d/nginx.conf
fi
# Finish the Nginx config file
echo "}" >> /etc/nginx/conf.d/nginx.conf

exec "$@"
