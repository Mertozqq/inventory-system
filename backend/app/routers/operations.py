from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Operation, OperationType, Stock, Restaurant, Ingredient
from app.schemas import OperationCreate, OperationOut

router = APIRouter(
    prefix="/operations",
    tags=["operations"],
)


@router.post("/", response_model=OperationOut)
def create_operation(data: OperationCreate, db: Session = Depends(get_db)):
    # Проверяем ресторан и ингредиент
    restaurant = db.query(Restaurant).get(data.restaurant_id)
    ingredient = db.query(Ingredient).get(data.ingredient_id)

    if not restaurant or not ingredient:
        raise HTTPException(status_code=404, detail="Restaurant or ingredient not found")

    # Находим/создаем строку склада
    stock = (
        db.query(Stock)
        .filter(
            Stock.restaurant_id == data.restaurant_id,
            Stock.ingredient_id == data.ingredient_id,
        )
        .first()
    )

    if not stock:
        stock = Stock(
            restaurant_id=data.restaurant_id,
            ingredient_id=data.ingredient_id,
            amount=0,
        )
        db.add(stock)
        db.flush()

    # Приход / расход
    if data.op_type == OperationType.IN:
        stock.amount += data.amount
    elif data.op_type == OperationType.OUT:
        if stock.amount < data.amount:
            raise HTTPException(status_code=400, detail="Not enough stock")
        stock.amount -= data.amount

    # Записываем операцию в журнал
    op = Operation(
        restaurant_id=data.restaurant_id,
        ingredient_id=data.ingredient_id,
        op_type=data.op_type,
        amount=data.amount,
        comment=data.comment,
    )

    db.add(op)
    db.commit()
    db.refresh(op)

    return op


@router.get("/", response_model=list[OperationOut])
def list_operations(db: Session = Depends(get_db)):
    return (
        db.query(Operation)
        .order_by(Operation.created_at.desc())
        .all()
    )
