from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Ingredient, Stock
from app.schemas import InventoryResponse

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)


@router.get("/ping")
def ping():
    return {"status": "ok"}


@router.get("/{restaurant_id}", response_model=list[InventoryResponse])
def get_inventory(restaurant_id: int, db: Session = Depends(get_db)):
    """
    Возвращает список ингредиентов и складских остатков
    для указанного ресторана.
    """
    rows = (
        db.query(
            Ingredient.id,           # 👈 важно: теперь берём id
            Ingredient.name,
            Ingredient.category,
            Stock.amount,
            Ingredient.unit,
            Ingredient.min_amount,
            Stock.expiration_date,
        )
        .join(Stock, Stock.ingredient_id == Ingredient.id)
        .filter(Stock.restaurant_id == restaurant_id)
        .all()
    )

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Ресторан не найден или склад пуст",
        )

    return [
        InventoryResponse(
            ingredient_id=r[0],
            name=r[1],
            category=r[2],
            amount=r[3],
            unit=r[4],
            min_amount=r[5],
            expiration_date=r[6],
        )
        for r in rows
    ]
