#!/usr/bin/env bash

echo "############################## nginx running with  ${DOMAIN}"

cat <<\EOT >/etc/nginx/conf.d/server.conf.template
upstream api {
    server backend:8000;
}
server {
    listen 8080;
    # server_name ${DOMAIN};
    location ~ ^/(api|help) {
        proxy_pass http://api;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
    }
}
EOT

envsubst '${DOMAIN}' </etc/nginx/conf.d/server.conf.template >/etc/nginx/conf.d/server.conf

nginx -g "daemon off;"