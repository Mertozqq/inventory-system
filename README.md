# Система управления запасами для ресторанов

Веб-приложение для контроля остатков ингредиентов в сети ресторанов. Поддерживает аналитические отчеты, мониторинг сроков годности, отображение складских запасов по каждому ресторану.

## Технологии

- Backend: FastAPI + SQLAlchemy
- База данных: PostgreSQL (по умолчанию) или SQLite
- Frontend: Vue 3 + Vite
- Прокси-сервер: Nginx
- Контейнеризация: Docker + Docker Swarm
- CI: GitHub Actions

## Структура проекта

```
├── backend/           # Приложение FastAPI
│   └── app/
├── frontend/          # Клиентская часть на Vue
├── proxy/             # Конфигурация Nginx
├── db/                # Инициализация базы PostgreSQL
├── docker-stack.yml   # Описание стеков для Swarm
├── .env               # Переменные окружения
```

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/yourname/inventory-system.git
cd inventory-system
```

### 2. Запуск в Docker Swarm

```bash
docker swarm init
docker stack deploy -c docker-stack.yml inventory
```

### 3. Открыть в браузере

- Frontend: http://localhost
- Backend API: http://localhost/api

## Основные маршруты API

| Метод | Путь                         | Назначение                               |
|-------|------------------------------|------------------------------------------|
| GET   | /api/analytics/summary       | Сводная информация по запасам            |
| GET   | /api/analytics/expiring      | Продукты с истекающим сроком годности    |
| GET   | /api/inventory/{id}          | Запасы по конкретному ресторану          |
| GET   | /api/restaurants             | Список всех ресторанов                   |

## CI

GitHub Actions проверяет:

- Импорт и сборку backend (FastAPI)
- Сборку frontend (Vite)
- Сборку всех Docker-образов

## Переменные окружения

```env
DATABASE_URL=postgresql://inventory:inventorypass@db:5432/inventorydb
```

## Автор

Проект реализован в рамках курсовой работы.
