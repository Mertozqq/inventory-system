FROM postgres:15-alpine

# Установка пароля и базы данных по умолчанию (можно также через docker-stack.yml)
ENV POSTGRES_USER=inventory
ENV POSTGRES_PASSWORD=inventorypass
ENV POSTGRES_DB=inventorydb

# Если нужно — добавить скрипты инициализации:
# COPY init.sql /docker-entrypoint-initdb.d/
