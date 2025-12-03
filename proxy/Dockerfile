FROM nginx:1.25-alpine

# Копируем свой конфиг Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Папку /usr/share/nginx/html будет заполнять фронтенд-сервисом при сборке (volume/shared path)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
