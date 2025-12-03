from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Restaurant, Stock
from app.schemas import RestaurantOut

router = APIRouter()


@router.get("/", response_model=list[RestaurantOut])
def get_restaurants(db: Session = Depends(get_db)):
    """
    Возвращает список всех ресторанов и агрегированную информацию по каждому.
    """
    restaurants = db.query(Restaurant).all()
    if not restaurants:
        raise HTTPException(status_code=404, detail="Нет ресторанов в системе")

    result = []

    for r in restaurants:
        stock_count = (
            db.query(Stock)
            .filter(Stock.restaurant_id == r.id)
            .count()
        )

        latest_delivery = (
            db.query(Stock.expiration_date)
            .filter(Stock.restaurant_id == r.id)
            .order_by(Stock.expiration_date.desc())
            .first()
        )

        result.append(
            RestaurantOut(
                id=r.id,
                name=r.name,
                address=r.address,
                is_active=r.is_active,
                stock_count=stock_count,
                last_delivery_date=latest_delivery[0] if latest_delivery else None
            )
        )

    return result
