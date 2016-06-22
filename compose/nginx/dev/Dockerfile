FROM nginx:latest

MAINTAINER MobyDevTeam

RUN sed -i 's/user  nginx;/user root;/' /etc/nginx/nginx.conf

COPY app.conf /etc/nginx/conf.d/default.conf
