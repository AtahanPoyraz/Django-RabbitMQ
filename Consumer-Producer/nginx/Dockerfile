FROM nginx:latest
LABEL maintainer="atahanpoyraz@gmail.com"

COPY ./default.conf /etc/nginx/conf.d/default.conf
EXPOSE 81
EXPOSE 80
EXPOSE 82

CMD ["nginx", "-g", "daemon off;"]