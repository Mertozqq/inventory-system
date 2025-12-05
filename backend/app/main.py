from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import get_db, init_db
from . import models  # чтобы Base.metadata была подхвачена
from .routers import inventory, restaurants, analytics, operations

app = FastAPI(
    title="Система управления запасами ресторанов",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(inventory.router, prefix="/api")
app.include_router(restaurants.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(operations.router, prefix="/api")


@app.get("/api/ping")
def ping():
    return {"status": "ok"}


# Если хочешь инициализировать БД при старте,
# можно раскомментировать этот код, но для Docker лучше делать это
# через init-скрипт или отдельный вызов:
#
# @app.on_event("startup")
# def on_startup():
#     init_db()
