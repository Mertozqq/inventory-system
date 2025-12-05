from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum


class InventoryResponse(BaseModel):
    ingredient_id: int          # 👈 добавили id ингредиента
    name: str
    category: Optional[str]
    amount: float
    unit: Optional[str]
    min_amount: Optional[float]
    expiration_date: Optional[date]

    class Config:
        orm_mode = True


class SummaryStats(BaseModel):
    total_items: int
    critical_items: int
    active_restaurants: int


class ExpiringItem(BaseModel):
    name: str
    expiration_date: Optional[date]
    restaurant_id: int

    class Config:
        orm_mode = True


class RestaurantOut(BaseModel):
    id: int
    name: str
    address: Optional[str]
    is_active: bool
    stock_count: int
    last_delivery_date: Optional[date]

    class Config:
        orm_mode = True


# ---------- ОПЕРАЦИИ (ПРИХОД / РАСХОД) ----------

class OperationType(str, Enum):
    IN = "IN"
    OUT = "OUT"


class OperationCreate(BaseModel):
    restaurant_id: int
    ingredient_id: int
    op_type: OperationType
    amount: float
    comment: Optional[str] = None


class OperationOut(BaseModel):
    id: int
    restaurant_id: int
    ingredient_id: int
    op_type: OperationType
    amount: float
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
