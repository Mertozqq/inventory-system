from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models import Restaurant, Ingredient, Stock

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("/ping")
def ping():
    return {"status": "ok"}


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """
    Сводка по системе по пути /api/analytics/summary.
    """
    total_restaurants = db.query(func.count(Restaurant.id)).scalar() or 0

    active_restaurants = (
        db.query(func.count(Restaurant.id))
        .filter(Restaurant.is_active == True)  # noqa: E712
        .scalar()
        or 0
    )

    total_ingredients = db.query(func.count(Ingredient.id)).scalar() or 0

    critical_stocks = (
        db.query(func.count(Stock.id))
        .join(Ingredient, Stock.ingredient_id == Ingredient.id)
        .filter(
            Ingredient.min_amount.isnot(None),
            Stock.amount < Ingredient.min_amount,
        )
        .scalar()
        or 0
    )

    today = date.today()
    expired_stocks = (
        db.query(func.count(Stock.id))
        .filter(Stock.expiration_date.isnot(None))
        .filter(Stock.expiration_date < today)
        .scalar()
        or 0
    )

    return {
        "total_restaurants": total_restaurants,
        "active_restaurants": active_restaurants,
        "total_ingredients": total_ingredients,
        "critical_stocks": critical_stocks,
        "expired_stocks": expired_stocks,
    }
