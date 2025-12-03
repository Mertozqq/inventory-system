# Этап 1: сборка фронтенда
FROM node:20 AS builder

WORKDIR /app

# Копируем конфиги и entry-файл
COPY package.json vite.config.js index.html ./

# Копируем исходники
COPY src ./src
COPY public ./public

RUN npm install
RUN npm run build

# Этап 2: nginx для статики (если ты им пользуешься)
FROM nginx:1.25-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
