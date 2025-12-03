from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.db import get_db
from app.models import Stock, Ingredient
from app.schemas import SummaryStats, ExpiringItem

router = APIRouter()


@router.get("/summary", response_model=SummaryStats)
def get_summary_stats(db: Session = Depends(get_db)):
    """
    Агрегированная сводка по запасам: общая сумма остатков,
    количество критических позиций, активные рестораны.
    """
    total_amount = db.query(Stock).count()

    critical_count = (
        db.query(Stock)
        .join(Ingredient, Stock.ingredient_id == Ingredient.id)
        .filter(Stock.amount < Ingredient.min_amount)
        .count()
    )

    active_restaurants = db.query(Stock.restaurant_id).distinct().count()

    return SummaryStats(
        total_items=total_amount,
        critical_items=critical_count,
        active_restaurants=active_restaurants
    )


@router.get("/expiring", response_model=list[ExpiringItem])
def get_expiring_items(db: Session = Depends(get_db)):
    """
    Список ингредиентов с истекающим сроком годности в ближайшие 3 дня.
    """
    today = date.today()
    threshold = today + timedelta(days=3)

    rows = (
        db.query(
            Ingredient.name,
            Stock.expiration_date,
            Stock.restaurant_id
        )
        .join(Stock, Stock.ingredient_id == Ingredient.id)
        .filter(Stock.expiration_date <= threshold)
        .all()
    )

    return [
        ExpiringItem(
            name=r[0],
            expiration_date=r[1],
            restaurant_id=r[2]
        )
        for r in rows
    ]
