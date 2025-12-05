from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    is_active = Column(Boolean, default=True)

    stocks = relationship("Stock", back_populates="restaurant")
    operations = relationship("Operation", back_populates="restaurant")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    unit = Column(String)  # например: кг, литры, шт
    min_amount = Column(Float, default=0.0)

    stocks = relationship("Stock", back_populates="ingredient")
    operations = relationship("Operation", back_populates="ingredient")


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    amount = Column(Float, nullable=False)
    expiration_date = Column(Date)

    restaurant = relationship("Restaurant", back_populates="stocks")
    ingredient = relationship("Ingredient", back_populates="stocks")


class OperationType(str, enum.Enum):
    IN = "IN"    # приход
    OUT = "OUT"  # расход


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)

    op_type = Column(Enum(OperationType), nullable=False)  # IN / OUT
    amount = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    comment = Column(String, nullable=True)

    restaurant = relationship("Restaurant", back_populates="operations")
    ingredient = relationship("Ingredient", back_populates="operations")
